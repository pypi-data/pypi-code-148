import torch
from alive_progress import alive_bar

from .datasets import srdatasets
from .utils import dataset_generator, metrics_generator


def benchmark(model, dataset, nimg, force: bool = False):

    # Check if the model is a valid torch model
    if not (
        isinstance(model, torch.jit.ScriptModule) or isinstance(model, torch.nn.Module)
    ):
        raise ValueError("The model is not a valid torch model")

    # Check if the dataset is a valid dataset
    if dataset not in srdatasets.SRDatasets.keys():
        raise ValueError("The dataset is not a valid dataset")
    dataset_metadata = srdatasets.SRDatasets[dataset]

    X, y = dataset_generator(dataset_metadata, nimg=nimg, force=force)

    # Run the metrics for each image
    results_list = list()
    with alive_bar(50, dual_line=True, title="SRcheck") as bar:
        for xtensor, ytensor in zip(X, y):
            # Obtain the super-resolved images (yhat)
            xtensor = torch.Tensor(xtensor.squeeze() / 10000)
            yhat = model(xtensor)

            # Convert y np.memmap to tensor
            ytensor = torch.Tensor(ytensor.squeeze() / 10000)

            mae, mae_01, mae_02, mae_05, psnr, msssim, ssim = metrics_generator(
                yhat.numpy(), ytensor.numpy(), xtensor.numpy()
            )
            results_list.append(
                {
                    "mae": mae,
                    "mae_01": mae_01,
                    "mae_02": mae_02,
                    "mae_05": mae_05,
                    "psnr": psnr,
                    "msssim": msssim,
                    "ssim": ssim,
                }
            )

            # Bar progress settings
            bar.text = (
                f"-> Cooking the results for {dataset_metadata.name}, please wait..."
            )
            bar()

    return results_list
