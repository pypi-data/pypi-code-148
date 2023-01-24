import pathlib

from .dataclass import Dataset, SRDatasets


def get_default_datasetpath():
    cred_path = pathlib.Path("~/.config/srcheck/").expanduser()
    if not cred_path.exists():
        cred_path.mkdir(parents=True)
    return cred_path.as_posix()


srdatasets = SRDatasets(
    SRDatasets=dict(
        ToyDataset=Dataset(
            name="ToyDataset",
            description="A simple dataset to check srcheck sanity",
            path=get_default_datasetpath(),
            hr_sensor="SPOT-6/7",
            hr_shape=(50, 1, 4, 1000, 1000),
            hr_url="https://zenodo.org/record/7562334/files/toy_target.npy",
            lr_sensor="Sentinel-2",
            lr_shape=(50, 16, 4, 250, 250),
            lr_url="https://zenodo.org/record/7562334/files/toy_input.npy",
            bands="R-G-B-NIR",
        )
    )
)
