import pathlib
from typing import Tuple, Union

import numpy as np
import torch
from alive_progress import alive_bar

from .datasets import srdatasets
from .utils import downloadfile, getFilename
from .metrics import metrics_generator


def create_dataset(
    dataset: str, approach: str = "SISR", nimg: int = 1, force: bool = False
) -> Tuple[np.ndarray, np.ndarray]:
    """Create a dataset from a given dataset name.

    Args:
        dataset: The dataset name. Currently, the following
            datasets are supported: "NAIP20".

        approachs: The SuperResolution approach.
            Only supports: 'SISR' or 'MISR'. Defaults to "SISR".

        nimg: The number of images to use in MISR. Defaults to 4.

        force (bool, optional): Force the download of the dataset.
            Defaults to False.

    Raises:
        ValueError: The dataset is not a valid dataset.
        ValueError: The SuperResolution approach is not valid.

    Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple with the LR and HR images as
        np.memmap tensor objects.

    Example:
        >>> from srcheck import dataset
        >>> X, y = dataset("NAIP20", approach="MISR", nimg=4)
    """

    # Check if the dataset is a valid dataset
    if dataset not in srdatasets.SRDatasets.keys():
        raise ValueError("The dataset is not a valid dataset")
    dataset_metadata = srdatasets.SRDatasets[dataset]

    # Main path
    dirpath = pathlib.Path(dataset_metadata.path)

    # Download LR images
    LRinfile = dirpath / getFilename(dataset_metadata.lr_url)
    if not LRinfile.exists() or force:
        downloadfile(url=dataset_metadata.lr_url, path=LRinfile)

    # Download HR images
    HRinfile = dirpath / getFilename(dataset_metadata.hr_url)
    if not HRinfile.exists() or force:
        downloadfile(dataset_metadata.hr_url, HRinfile)

    # Load the dataset
    X = np.memmap(LRinfile, dtype=np.int16, mode="r", shape=dataset_metadata.lr_shape)
    y = np.memmap(HRinfile, dtype=np.int16, mode="r", shape=dataset_metadata.hr_shape)

    # Filter by the number of images
    if approach == "SISR":
        np_dataset = X[:, 0:1, :, :], y[:, 0:1, :, :]
    elif approach == "MISR":
        # The first image is for SISR, the rest for MISR
        np_dataset = X[:, 1 : (nimg + 1), :, :], y[:, 1 : (nimg + 1), :, :]
    else:
        raise ValueError(
            "The SuperResolution approach is not valid. Please, use 'SISR' or 'MISR'."
        )

    return np_dataset



def benchmark(
    model: Union[torch.jit.ScriptModule, torch.nn.Module, torch.nn.Sequential],
    dataset: str,
    approach: str = "SISR",
    nimg: int = 1,
    threshold: int = 0.05,
    force: bool = False,
) -> list:

    # Check if the model is a valid torch model
    if not (
        isinstance(model, torch.jit.ScriptModule) or isinstance(model, torch.nn.Module)
    ):
        raise ValueError("The model is not a valid torch model")

    # Check if the dataset is a valid dataset
    if dataset not in srdatasets.SRDatasets.keys():
        raise ValueError("The dataset is not a valid dataset")
    
    # Create the dataset
    dataset_metadata = srdatasets.SRDatasets[dataset]
    dataset_imgs = dataset_metadata.lr_shape[0]
    X, y = create_dataset(
        dataset=dataset,
        approach=approach,
        nimg=nimg,
        force=force
    )
    
    # Run the metrics for each image
    results_list = list()
    with alive_bar(dataset_imgs, dual_line=True, title="SRcheck") as bar:
        for xtensor, ytensor in zip(X, y):
            # Divide the y tensor in its mask and the RGBNIR bands
            ytensor, mask = ytensor[0:1, 0:4], ytensor[0, 4]
            
            # Convert data np.memmap to tensor
            xtensor = torch.Tensor(xtensor.copy())/10000
            ytensor = torch.Tensor(ytensor.copy())/10000
            mask = torch.Tensor(mask.copy())/10000 > threshold
            
            # Obtain the super-resolved images (yhat)
            yhat = model(xtensor)
            
            # Compute the metrics
            psnr, ssim = metrics_generator(yhat, ytensor, mask)
            
            # Save the results
            results_list.append(
                {
                    "psnr": psnr,
                    "ssim": ssim,
                }
            )

            # Bar progress settings
            bar.text = (
                f"-> Cooking the results for {dataset_metadata.name}, please wait..."
            )
            bar()

    return results_list
