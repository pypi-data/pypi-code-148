import argparse
import json
import os
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

import tarfile

import torch
import torch.backends.cudnn as cudnn
from lavis.common.dist_utils import get_rank, get_world_size, init_distributed_mode
from lavis.common.logger import MetricLogger
from torch.utils.data import DataLoader, Dataset


class capfilt_dataset(Dataset):
    def __init__(self, ann_file):
        self.ann = []
        for file in ann_file:
            print("loading %s" % file)
            self.ann += json.load(open(file, "r"))

    def __len__(self):
        return len(self.ann)

    def __getitem__(self, index):

        ann = self.ann[index]
        image_path = ann["image"]
        # image = Image.open(ann["image"]).convert("RGB")

        return ann["caption"], image_path


def main(args):
    init_distributed_mode(args)

    device = torch.device(args.device)

    # fix the seed for reproducibility
    seed = args.seed + get_rank()
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    cudnn.benchmark = True

    dataset = capfilt_dataset(args.annotation)

    num_tasks = get_world_size()
    global_rank = get_rank()
    sampler = torch.utils.data.DistributedSampler(
        dataset, num_replicas=num_tasks, rank=global_rank, shuffle=False
    )
    dataloader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        num_workers=4,
        pin_memory=True,
        sampler=sampler,
        drop_last=False,
        shuffle=False,
    )

    metric_logger = MetricLogger(delimiter="  ")
    header = "Capfilt:"
    print_freq = 10

    for batch_id, (captions, image_path) in enumerate(
        metric_logger.log_every(dataloader, print_freq, header)
    ):
        if batch_id % args.batch_per_shard == 0:
            if batch_id > 0:
                tar_file.close()
            tar_file = tarfile.open(
                os.path.join(
                    args.output_dir,
                    "part0_node%02d_shard%06d.tar"
                    % (global_rank, batch_id // args.batch_per_shard),
                ),
                "w",
            )
            file_id = 0

        for cap, img_path in zip(captions, image_path):
            img_path = img_path.replace("laion400m", args.laion_volume_name)

            filename = img_path.split("/")[-1].strip(".jpg")
            filepath = "/".join(img_path.split("/")[:-1])

            json_path = filepath.replace("image_384", "json_115m_en")
            if not os.path.exists(json_path):
                os.makedirs(json_path)

            json_file = os.path.join(json_path, filename + ".json")
            json.dump({"caption": cap, "image": img_path}, open(json_file, "w"))

            file_id += 1
            tar_file.add(img_path, arcname="%05d.jpg" % file_id)
            tar_file.add(json_file, arcname="%05d.json" % file_id)

    tar_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--k", default=5, type=int)
    # parser.add_argument("--n_cap", default=10, type=int)
    parser.add_argument("--batch_size", default=128, type=int)
    parser.add_argument("--batch_per_shard", default=2048, type=int)
    # parser.add_argument('--annotation', default=['../VL_pretrain/annotation/Laion_part0.json',
    #                                                 '../VL_pretrain/annotation/Laion_part1.json',
    #                                                 '../VL_pretrain/annotation/Laion_part2.json'
    #                                             ])
    parser.add_argument(
        "--annotation",
        default=[
            "/export/share/junnan-li/VL_pretrain/annotation/Laion_part0.json",
            "/export/share/junnan-li/VL_pretrain/annotation/Laion_part1.json",
            "/export/share/junnan-li/VL_pretrain/annotation/Laion_part2.json",
            # '../VL_pretrain/annotation/Laion_part1.json',
            # '../VL_pretrain/annotation/Laion_part2.json'
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
    # [TODO] change to your own paths to store the new data
    parser.add_argument(
        "--output_dir", default="/export/laion/laion115m_capfilt_20220812"
    )
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--seed", default=42, type=int)
    parser.add_argument(
        "--world_size", default=1, type=int, help="number of distributed processes"
    )
    # [TODO] change to the volume name which contains laion data, in my case it's /export/laion, so I use laion
    parser.add_argument("--laion_volume_name", default="laion")
    parser.add_argument(
        "--dist_url", default="env://", help="url used to set up distributed training"
    )
    parser.add_argument("--distributed", default=True, type=bool)
    args = parser.parse_args()

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    main(args)
