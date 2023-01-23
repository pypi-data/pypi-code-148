from __future__ import annotations

import functools
import os
import typing as t

from torch.utils.data import DataLoader
from torchvision import datasets as tvd, transforms

from gemovi.common import constants
from gemovi.common.utils import pad_image_to_size

_DEFAULT_IMAGE_TRANSFORMS = object()


def ignore_alpha(x):
    return x[:3, :, :]


def default_image_transforms(image_size, pad_on_resize=None):
    if pad_on_resize is None:
        pad_on_resize = constants.pad_on_resize
    if pad_on_resize:
        resize = transforms.Lambda(
            functools.partial(pad_image_to_size, size_wh=image_size)
        )
    else:
        resize = transforms.Resize(image_size)
    return transforms.Compose(
        [
            resize,
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            # Strip alpha if it exists
            transforms.Lambda(ignore_alpha),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ]
    )


class GMVDataset(tvd.ImageFolder):
    def __init__(
        self,
        data_dir: str,
        split: str = None,
        transform: t.Callable | None = None,
        folder_is_class=False,
        allowed_classes=None,
        create_test_set=True,
        train_percent=0.8,
        test_percent=0.05,
        **kwargs,
    ):
        self.allowed_classes = allowed_classes
        self.create_test_set = create_test_set
        self.train_percent, self.test_percent = train_percent, test_percent

        data_dir = os.path.abspath(os.path.normpath(data_dir))
        if folder_is_class and (allowed_classes is not None and len(allowed_classes)):
            raise ValueError("Cannot use folder_is_class with allowed_classes")
        elif folder_is_class:
            self.allowed_classes = [os.path.basename(data_dir)]
            data_dir = self.root = os.path.dirname(data_dir)
        super().__init__(data_dir, transform, **kwargs)
        if split and split != "all":
            self.imgs = self.samples = self.get_sample_subset(split)

    def find_classes(self, directory: str) -> tuple[list[str], dict[str, int]]:
        """
        Allows root folder to act as a class if folder_is_class is True. Otherwise,
        behaves the same as the parent class.
        """
        ret = super().find_classes(directory)
        if not self.allowed_classes:
            return ret
        _, class_to_idx = ret
        class_to_idx = {kk: class_to_idx[kk] for kk in self.allowed_classes}
        return self.allowed_classes, class_to_idx

    def get_sample_subset(self, split: str):
        num_train_samps = int(len(self.samples) * self.train_percent)
        if self.create_test_set:
            num_test_samps = int(len(self.samples) * self.test_percent)
            num_val_samps = len(self.samples) - num_train_samps - num_test_samps
        else:
            num_val_samps = len(self.samples) - num_train_samps
            # num_test_samps = 0 in this case
        if split == "train":
            start_idx, stop_idx = 0, num_train_samps
        elif split == "val" or not self.create_test_set:
            start_idx, stop_idx = num_train_samps, num_train_samps + num_val_samps
        elif split == "test":
            start_idx, stop_idx = num_train_samps + num_val_samps, len(self.samples)
        else:
            raise ValueError(
                f"Unknown split: {split}. Must be one of 'all', 'train', 'val', 'test'"
            )
        return self.samples[start_idx:stop_idx]


try:
    from pytorch_lightning import LightningDataModule

    class LitGMVLoader(LightningDataModule):
        """
        PyTorch Lightning data module

        Args:
            data_dir: root directory of your dataset.
            train_batch_size: the batch size to use during training.
            val_batch_size: the batch size to use during validation.
            patch_size: the size of the crop to take from the original images.
            num_workers: the number of parallel workers to create to load data
                items (see PyTorch's Dataloader documentation for more details).
            pin_memory: whether prepared items should be loaded into pinned memory
                or not. This can improve performance on GPUs.
        """

        def __init__(
            self,
            data_path: str,
            train_batch_size: int = 8,
            val_batch_size: int = 8,
            patch_size: int | t.Sequence[int] = (256, 256),
            transform: t.Callable | None = None,
            folder_is_class=True,
            pad_on_resize=None,
            **kwargs,
        ):
            super().__init__()

            self.train_batch_size = train_batch_size
            self.val_batch_size = val_batch_size
            if transform is None:
                transform = default_image_transforms(patch_size, pad_on_resize)

            self.dataset_factory = functools.partial(
                GMVDataset,
                data_path,
                transform=transform,
                folder_is_class=folder_is_class,
            )

            # Populated later
            self.train_dataset, self.val_dataset, self.test_dataset = [None] * 3

            self.dset_kwargs = kwargs

        def setup(self, stage: str | None = None) -> None:
            self.train_dataset, self.val_dataset, self.test_dataset = [
                self.dataset_factory(split=split) for split in ("train", "val", "test")
            ]

        def train_dataloader(self) -> DataLoader:
            return DataLoader(
                self.train_dataset,
                batch_size=self.train_batch_size,
                **self.dset_kwargs,
                shuffle=True,
            )

        def val_dataloader(self) -> DataLoader | list[DataLoader]:
            return DataLoader(
                self.val_dataset, batch_size=self.val_batch_size, **self.dset_kwargs
            )

        def test_dataloader(self) -> DataLoader | list[DataLoader]:
            return DataLoader(
                self.test_dataset, batch_size=self.val_batch_size, **self.dset_kwargs
            )

except ImportError:
    pass
