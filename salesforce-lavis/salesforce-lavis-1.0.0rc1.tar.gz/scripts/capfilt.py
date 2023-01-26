import argparse
import os
import ruamel_yaml as yaml
import numpy as np
import random
import time
import datetime
import json
from pathlib import Path
from PIL import Image
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
import torch
from torch import nn
import torch.nn.functional as F
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode
import torch.backends.cudnn as cudnn
import torch.distributed as dist

from lavis.models import load_model
from lavis.common.dist_utils import get_rank, get_world_size, init_distributed_mode
from lavis.common.logger import MetricLogger
from lavis.models.clip_models.tokenizer import tokenize as clip_tokenize

# from blip.blip import blip_decoder
# import utils
# import clip
import tarfile


class capfilt_dataset(Dataset):
    def __init__(self, ann_file, transform_blip, transform_clip):
        self.ann = []
        for file in ann_file:
            print("loading %s" % file)
            self.ann += json.load(open(file, "r"))
        self.transform_blip = transform_blip
        self.transform_clip = transform_clip

    def __len__(self):
        return len(self.ann)

    def __getitem__(self, index):

        ann = self.ann[index]

        image_path = ann["image"]
        image = Image.open(image_path).convert("RGB")
        image_blip = self.transform_blip(image)
        image_clip = self.transform_clip(image)

        return image_blip, image_clip, ann["caption"], image_path


def main(args):
    init_distributed_mode(args)

    device = torch.device(args.device)
    # fix the seed for reproducibility
    seed = args.seed + get_rank()
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    cudnn.benchmark = True
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

    dataset = capfilt_dataset(args.annotation, transform_blip, transform_clip)
    num_tasks = get_world_size()
    global_rank = get_rank()
    sampler = torch.utils.data.DistributedSampler(
        dataset, num_replicas=num_tasks, rank=global_rank, shuffle=False
    )
    dataloader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        num_workers=5,
        pin_memory=True,
        sampler=sampler,
        drop_last=False,
        shuffle=False,
    )
    # model_captioner = blip_decoder(
    #     pretrained="https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_large_caption.pth",
    #     vit="large",
    # )

    # model_captioner = model_captioner.to(device)
    # model_captioner.eval()

    model_captioner = load_model(
        name="blip_caption", model_type="large_coco", device=device, is_eval=True
    )
    # model_filter = load_model(
    #     name="clip", model_type="ViT-B-16", device=device, is_eval=True
    # )
    model_filter = load_model(
        name="clip", model_type="ViT-L-14", device=device, is_eval=True
    )

    # model_filter, _ = clip.load("ViT-B/16", device=device)
    # model_filter.eval()

    annotation = []
    metric_logger = MetricLogger(delimiter="  ")
    header = "Capfilt:"
    print_freq = 10

    tar_file = None

    existing_tars = set(os.listdir(args.output_dir))

    with torch.no_grad():
        for batch_id, (image_blip, image_clip, captions, image_path) in enumerate(
            metric_logger.log_every(dataloader, print_freq, header)
        ):
            tar_path = os.path.join(
                args.output_dir,
                # "part0_node%02d_shard%06d.tar"
                f"{partn}_node%02d_shard%06d.tar"
                % (global_rank, batch_id // args.batch_per_shard),
            )

            if os.path.basename(tar_path) in existing_tars:
                continue

            if batch_id % args.batch_per_shard == 0:
                if batch_id > 0 and tar_file is not None:
                    tar_file.close()
                tar_file = tarfile.open(tar_path, "w")
                file_id = 0

            image_blip = image_blip.to(device, non_blocking=True)
            image_clip = image_clip.to(device, non_blocking=True)

            captions_blip = model_captioner.generate(
                samples={"image": image_blip},
                use_nucleus_sampling=True,
                top_p=0.95,
                min_length=5,
                num_captions=args.n_cap,
            )

            # tokens_blip = clip.tokenize(captions_blip, truncate=True).to(device)
            # tokens_blip = clip.tokenize(captions_blip, truncate=True).to(device)
            # tokens_blip = clip_tokenize(captions_blip, truncate=True).to(device)
            tokens_blip = clip_tokenize(captions_blip).to(device)
            image_features = F.normalize(model_filter.encode_image(image_clip), dim=-1)
            text_features_blip = F.normalize(
                model_filter.encode_text(tokens_blip), dim=-1
            )

            # sim_blip = torch.bmm(
            #     image_features.unsqueeze(1),
            #     text_features_blip.view(args.batch_size, args.n_cap, -1).permute(
            #         0, 2, 1
            #     ),
            # )
            sim_blip = torch.bmm(
                image_features.unsqueeze(1),
                text_features_blip.view(image_blip.size(0), args.n_cap, -1).permute(
                    0, 2, 1
                ),
            )
            # tokens_orig = clip.tokenize(captions, truncate=True).to(device)
            tokens_orig = clip_tokenize(captions).to(device)
            text_features_orig = F.normalize(
                model_filter.encode_text(tokens_orig), dim=-1
            )
            sim_orig = (
                torch.bmm(image_features.unsqueeze(1), text_features_orig.unsqueeze(-1))
                + 0.2
            )

            sim = torch.cat([sim_blip, sim_orig], dim=-1).squeeze()
            _, indices = torch.topk(sim, k=args.k, dim=-1)
            for i, ind in enumerate(indices):
                caps = captions_blip[i * args.n_cap : i * args.n_cap + args.n_cap] + [
                    captions[i]
                ]
                caps = [caps[n] for n in ind]
                img_path = image_path[i]
                filename = img_path.split("/")[-1].strip(".jpg")
                filepath = "/".join(img_path.split("/")[:-1])

                # for laion dataset
                json_path = filepath.replace("image_384", "json")
                if not os.path.exists(json_path):
                    os.makedirs(json_path)

                json_file = os.path.join(json_path, filename + ".json")
                json.dump(caps, open(json_file, "w"))

                file_id += 1
                tar_file.add(img_path, arcname="%05d.jpg" % file_id)
                tar_file.add(json_file, arcname="%05d.json" % file_id)

                os.remove(json_file)

    tar_file.close()


if __name__ == "__main__":
    partn = "part0"
    # partn = "part1"

    parser = argparse.ArgumentParser()
    parser.add_argument("--k", default=3, type=int)
    parser.add_argument("--n_cap", default=10, type=int)
    parser.add_argument("--batch_size", default=192, type=int)
    parser.add_argument("--batch_per_shard", default=100, type=int)
    parser.add_argument(
        "--annotation",
        default=[
            # "/export/share/junnan-li/VL_pretrain/annotation/cc3m.json",
            # "/export/share/junnan-li/VL_pretrain/annotation/Laion_part0.json",
            f"/export/share/junnan-li/VL_pretrain/annotation/Laion_{partn}.json",
            # "/export/share/junnan-li/VL_pretrain/annotation/Laion_part2.json",
        ],
    )
    # parser.add_argument(
    #     "--annotation",
    #     default=[
    #         "../VL_pretrain/annotation/cc3m.json",
    #         "../VL_pretrain/annotation/cc12m.json",
    #     ],
    # )
    # parser.add_argument(
    #     "--output_dir", default="/export/share/datasets/vision_language/cc_webdata"
    # )
    parser.add_argument(
        "--output_dir",
        default=f"/export/laion400m/laion115m_capfilt_20220817/{partn}",
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
