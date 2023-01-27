"""
A script to load LAION dataset in default format.

Apply BLIP for captioning and CLIP for computing caption similarity.

This script distributes shards to different nodes, in order to access each
sample in WebDataset instance *exactly once*.

Author: Dongxu Li
Date: 2022. Dec.
"""


import argparse
import io
import json
import os
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

import torch
import torch.backends.cudnn as cudnn
import torch.nn.functional as F
import webdataset as wds
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode

from lavis.common.dist_utils import get_rank, get_world_size
from lavis.models import load_model
from lavis.models.clip_models.tokenizer import tokenize as clip_tokenize

normalize = transforms.Normalize(
    (0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711)
)
transform_blip = transforms.Compose(
    [
        transforms.Resize((384, 384), interpolation=InterpolationMode.BICUBIC),
        transforms.ToTensor(),
        normalize,
    ]
)
transform_clip = transforms.Compose(
    [
        transforms.Resize(224, interpolation=InterpolationMode.BICUBIC),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        normalize,
    ]
)


def yield_local_dataloader(total_parts, rank, world_size, base_location, batch_size):
    def collate_fn(batch):
        d = dict()

        batch = batch[0]

        d["image"] = [item["image"] for item in batch]
        d["text_input"] = [item["text_input"] for item in batch]
        d["metainfo"] = [item["metainfo"] for item in batch]

        d["image_blip"] = torch.stack([transform_blip(item["image"]) for item in batch])
        d["image_clip"] = torch.stack([transform_clip(item["image"]) for item in batch])

        return d

    def to_dict(sample):
        return {
            "image": sample[0],
            "text_input": sample[1]["caption"],
            "metainfo": sample[1],
        }

    parts_per_rank = total_parts // world_size
    assert total_parts % world_size == 0, "total_parts must be divisible by world_size"

    local_part_s = rank * parts_per_rank
    local_part_e = (rank + 1) * parts_per_rank

    for part in range(local_part_s, local_part_e):
        for tar_id in range(args.tar_id_start, args.tar_id_end + 1):
            part, tar_id = str(part).zfill(5), str(tar_id).zfill(5)
            # location = os.path.join(args.location, f"part-{part}/{{00000..00001}}.tar")
            dataset_dir = f"part-{part}/{tar_id}.tar"
            location = os.path.join(base_location, dataset_dir)

            dataset = wds.DataPipeline(
                wds.SimpleShardList(location),
                wds.split_by_worker,  # NOTE IMPORTANT to have, otherwise duplicate samples appear in each worker
                wds.tarfile_to_samples(handler=wds.warn_and_continue),
                # wds.shuffle(1000, handler=wds.warn_and_continue),
                wds.decode("pilrgb", handler=wds.warn_and_continue),
                wds.to_tuple("jpg", "json", handler=wds.warn_and_continue),
                # wds.map_tuple(
                #     lambda x: (x, transform_blip(x), transform_clip(x)),
                #     handler=wds.warn_and_continue,
                # ),
                wds.map(to_dict, handler=wds.warn_and_continue),
            ).batch(batch_size)

            # dataloader = DataLoader(
            dataloader = wds.WebLoader(
                dataset,
                # batch_size=batch_size,
                num_workers=4,
                # pin_memory=True,
                # persistent_workers=True,
                collate_fn=collate_fn,
            )

            print(f"Loading {location} for rank {rank}")

            yield dataloader, dataset_dir


def init_stats_tracker():
    return {"num_samples": 0, "has_better_blip_caption": 0, "num_unsafe": 0}


def init_distributed_mode(args):
    if "RANK" in os.environ and "WORLD_SIZE" in os.environ:
        args.rank = int(os.environ["RANK"])
        args.world_size = int(os.environ["WORLD_SIZE"])
        args.gpu = int(os.environ["LOCAL_RANK"])
    elif "SLURM_PROCID" in os.environ:
        args.rank = int(os.environ["SLURM_PROCID"])
        args.gpu = args.rank % torch.cuda.device_count()
    else:
        print("Not using distributed mode")
        args.distributed = False
        return

    args.distributed = True

    torch.cuda.set_device(args.gpu)
    args.dist_backend = "nccl"
    print(
        "| distributed init (rank {}, world {}): {}".format(
            args.rank, args.world_size, args.dist_url
        ),
        flush=True,
    )
    torch.distributed.init_process_group(
        backend=args.dist_backend,
        init_method=args.dist_url,
        world_size=args.world_size,
        rank=args.rank,
    )
    torch.distributed.barrier()


@torch.no_grad()
def main(args):
    init_distributed_mode(args)

    device = torch.device(args.device)
    # fix the seed for reproducibility
    seed = args.seed + get_rank()
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    cudnn.benchmark = True

    model_captioner = load_model(
        name="blip_caption", model_type="large_coco", device=device, is_eval=True
    )
    model_filter = load_model(
        name="clip", model_type="ViT-L-14", device=device, is_eval=True
    )

    # dataset = capfilt_dataset(args.annotation, transform_blip, transform_clip)
    num_tasks = get_world_size()
    global_rank = get_rank()

    # with torch.no_grad():
    for dataloader, dataset_dir in yield_local_dataloader(
        total_parts=args.total_parts,
        rank=global_rank,
        world_size=num_tasks,
        base_location=args.location,
        batch_size=args.batch_size,
    ):
        # setup the output directory
        dirname, basename = os.path.split(dataset_dir)
        dirpath = os.path.join(args.output_dir, dirname)
        Path(dirpath).mkdir(parents=True, exist_ok=True)

        tar_path = os.path.join(dirpath, basename)
        stats_path = os.path.join(
            dirpath, os.path.splitext(basename)[0] + "_stats.json"
        )

        if os.path.exists(stats_path):
            # stats will generated only if the data shard is finished processing
            # so if the stats file exists, we can skip this shard
            print(
                f"Rank: {get_rank()}: skipping {tar_path} because {stats_path} exists"
            )
            continue
        else:
            if os.path.exists(tar_path):
                # if the tar file exists, but the stats file does not, then
                # something went wrong and we should delete the tar file
                print(f"Rank: {get_rank()}: deleting incomplete file: {tar_path}")
                os.remove(tar_path)

        # with tarfile.open(tar_path, "w") as tar_file:
        with wds.TarWriter(tar_path, encoder=False) as sink:

            stats_tracker = init_stats_tracker()
            stats_tracker["max_punsafe"] = args.max_punsafe
            stats_tracker["src_shard"] = dataset_dir

            try:

                for file_id, sample in enumerate(dataloader):

                    image_blip = sample["image_blip"]
                    image_clip = sample["image_clip"]

                    captions = sample["text_input"]

                    image_blip = image_blip.to(device, non_blocking=True)
                    image_clip = image_clip.to(device, non_blocking=True)

                    # ===== CAPTIONING ======
                    # generate captions using blip
                    captions_blip = model_captioner.generate(
                        samples={"image": image_blip},
                        use_nucleus_sampling=True,
                        top_p=0.95,
                        min_length=5,
                        num_captions=args.n_cap,
                    )

                    # ===== FILTERING ======
                    # here we just compute the similarity between the image and captions
                    tokens_blip = clip_tokenize(captions_blip).to(device)
                    image_features = F.normalize(
                        model_filter.encode_image(image_clip), dim=-1
                    )
                    text_features_blip = F.normalize(
                        model_filter.encode_text(tokens_blip), dim=-1
                    )

                    sim_blip = torch.bmm(
                        image_features.unsqueeze(1),
                        text_features_blip.view(
                            image_blip.size(0), args.n_cap, -1
                        ).permute(0, 2, 1),
                    )
                    # tokens_orig = clip.tokenize(captions, truncate=True).to(device)
                    tokens_orig = clip_tokenize(captions).to(device)
                    text_features_orig = F.normalize(
                        model_filter.encode_text(tokens_orig), dim=-1
                    )
                    sim_orig = (
                        torch.bmm(
                            image_features.unsqueeze(1),
                            text_features_orig.unsqueeze(-1),
                        )
                        # + 0.2
                    )

                    # ===== SAVE AND HOUSEKEEPING ======
                    all_sims = torch.cat([sim_blip, sim_orig], dim=-1).squeeze()

                    for i, (sims, metainfo, orig_img) in enumerate(
                        zip(all_sims, sample["metainfo"], sample["image"])
                    ):
                        stats_tracker["num_samples"] += 1

                        # NOTE filter out the images that are not safe for work
                        if metainfo["punsafe"] > args.max_punsafe:
                            stats_tracker["num_unsafe"] += 1
                            continue

                        blip_score, orig_score = [
                            float(s.item()) for s in sims[:-1]
                        ], float(sims[-1].item())
                        metainfo["blip_caption"] = captions_blip[
                            i * args.n_cap : (i + 1) * args.n_cap
                        ]
                        metainfo["capfilt_similarities"] = {
                            "scoring_model": "clip_vit_l_14_openai",
                            "blip_large_coco": blip_score,
                            "original": orig_score,
                        }

                        if max(blip_score) > orig_score:
                            stats_tracker["has_better_blip_caption"] += 1

                        hashcode = str(metainfo["hash"])

                        # save the image and the metainfo to the tar file
                        img_dir = "temp/image"
                        json_dir = "temp/json"

                        # make sure the directory exists
                        Path(img_dir).mkdir(parents=True, exist_ok=True)
                        Path(json_dir).mkdir(parents=True, exist_ok=True)

                        # file_id = str(file_id).zfill(6)
                        # basename = f"{hashcode}_{file_id}"

                        basename = f"{hashcode}"

                        # img_filename = f"{basename}" + ".jpg"
                        # metainfo_filename = f"{basename}" + ".json"

                        # img_path = os.path.join(img_dir, img_filename)
                        # metainfo_path = os.path.join(json_dir, metainfo_filename)

                        # save the image
                        # orig_img.save(img_path)

                        # save the metainfo
                        # with open(metainfo_path, "w") as f:
                        #     json.dump(metainfo, f)

                        # print(img_path)
                        # print(metainfo_path)

                        # tar_file.add(img_path, arcname=img_filename)
                        # tar_file.add(metainfo_path, arcname=metainfo_filename)

                        img_byte_arr = io.BytesIO()
                        orig_img.save(img_byte_arr, format="JPEG")
                        img_byte_arr = img_byte_arr.getvalue()

                        # convert the metainfo to bytes
                        json_byte_arr = json.dumps(metainfo).encode("utf-8")

                        sample = {
                            "__key__": basename,
                            "jpg": img_byte_arr,
                            "json": json_byte_arr,
                        }

                        sink.write(sample)

                        # tar_file.add(img_path, arcname=img_filename)
                        # tar_file.add(metainfo_path, arcname=metainfo_filename)

                        # os.remove(img_path)
                        # os.remove(metainfo_path)

                    # break

                # save the stats
                with open(stats_path, "w") as f:
                    json.dump(stats_tracker, f)

            except Exception as e:
                with open("err_rank{}.txt".format(get_rank()), "a") as f:
                    f.write(
                        f"Rank {get_rank()}: error at data shard {dataset_dir}" + "\n"
                    )
                    f.write(str(e) + "\n")

        # break

    # torch.distributed.barrier()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_cap", default=3, type=int)
    parser.add_argument("--batch_size", default=384, type=int)
    parser.add_argument("--total_parts", default=128, type=int)
    parser.add_argument(
        "--tar_id_start",
        default=0,
        type=int,
        help="starting id of the tar file, will be zfill(5) before use",
    )
    parser.add_argument(
        "--tar_id_end",
        default=40,
        type=int,
        help="ending id of the tar file, will be zfill(5) before use",
    )
    parser.add_argument(
        "--max_punsafe",
        default=0.1,
        type=float,
        help="threshold for filtering out unsafe images. 0.1 is the value used by stable-diffusion-2",
    )
    # parser.add_argument("--batch_per_shard", default=100, type=int)
    parser.add_argument(
        "--location",
        default="/export/laion400m/laion-aesthetic/laion-aesthetic-v1/laion-aesthetic-en-51m/images/",
    )
    parser.add_argument(
        "--output_dir",
        default=f"/export/laion2b-en/laion-aesthetic-capfilt-20221213/v1/en-51m",
    )
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--seed", default=42, type=int)
    parser.add_argument(
        "--world_size", default=1, type=int, help="number of distributed processes"
    )
    parser.add_argument(
        "--dist_url", default="env://", help="url used to set up distributed training"
    )
    parser.add_argument("--distributed", default=True, type=bool)
    args = parser.parse_args()
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    main(args)
