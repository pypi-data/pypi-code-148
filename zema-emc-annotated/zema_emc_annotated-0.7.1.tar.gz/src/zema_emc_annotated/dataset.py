"""An API for accessing the data in the ZeMA remaining-useful life dataset"""

__all__ = [
    "ExtractionDataType",
    "ZeMASamples",
    "ZEMA_DATASET_HASH",
    "ZEMA_DATASET_URL",
    "ZEMA_QUANTITIES",
]

import operator
import os
import pickle
from enum import Enum
from functools import reduce
from os.path import exists
from pathlib import Path
from typing import cast

import h5py
import numpy as np
from h5py import Dataset
from numpy._typing import NDArray
from pooch import os_cache, retrieve

from zema_emc_annotated.data_types import (
    RealMatrix,
    RealVector,
    SampleSize,
    UncertainArray,
)

ZEMA_DATASET_HASH = (
    "sha256:fb0e80de4e8928ae8b859ad9668a1b6ea6310028a6690bb8d4c1abee31cb8833"
)
ZEMA_DATASET_URL = "https://zenodo.org/record/5185953/files/axis11_2kHz_ZeMA_PTB_SI.h5"
ZEMA_QUANTITIES = (
    "Acceleration",
    "Active_Current",
    "Force",
    "Motor_Current",
    "Pressure",
    "Sound_Pressure",
    "Velocity",
)


class ExtractionDataType(Enum):
    """Identifiers of data types in ZeMA dataset

    Attributes
    ----------
    VALUES : str
        with value ``qudt:value``
    UNCERTAINTIES : str
        with value ``qudt:standardUncertainty``
    """

    VALUES = "qudt:value"
    UNCERTAINTIES = "qudt:standardUncertainty"


class ZeMASamples:
    """Extracts requested number of samples of values with associated uncertainties

    The underlying dataset is the annotated "Sensor data set of one electromechanical
    cylinder at ZeMA testbed (ZeMA DAQ and Smart-Up Unit)" by Dorst et al. [Dorst2021]_.
    Each extracted sample will be cached in the download directory of the file,
    which is handled by :func:`pooch.os_cache`, where ``<AppName>`` evaluates to
    ``pooch``. That way the concurrent retrieval of the same data is as performant as
    possible and can simply be left to ``zema_emc_annotated``. Where ever the result
    of ``ZeMASamples`` is needed in an external code base, it should be safe to call
    it over and over without causing unnecessary extractions or even downloads. The
    underlying mechanism is Python's built-in ``pickle``.

    Parameters
    ----------
    sample_size : SampleSize, optional
        tuple containing information about which samples to extract, defaults to
        default of :class:`~zema_emc_annotated.data_types.SampleSize`
    normalize : bool, optional
        if ``True``, then values are centered around zero and values and
        uncertainties are scaled to values' unit std, defaults to ``False``
    skip_hash_check : bool, optional
        allow to circumvent strict hash checking during the retrieve of dataset file,
        to speed up concurrent calls as each check for the large file might take
        several seconds, defaults to ``False``

    Attributes
    ----------
    uncertain_values : UncertainArray
        The collection of samples of values with associated uncertainties,
        will be of shape (``sample_size.n_cycles``, 11 x
        ``sample_size.datapoints_per_cycle``)
    """

    uncertain_values: UncertainArray

    def __init__(
        self,
        sample_size: SampleSize = SampleSize(),
        normalize: bool = False,
        skip_hash_check: bool = False,
    ):

        self.samples_slice: slice = np.s_[
            sample_size.idx_first_cycle : sample_size.idx_first_cycle
            + sample_size.n_cycles
        ]
        self.size_scaler = sample_size.datapoints_per_cycle
        if cached_data := self._check_and_load_cache(normalize):
            self.uncertain_values = cached_data
        else:
            self._uncertainties = np.empty((sample_size.n_cycles, 0))
            self._values = np.empty((sample_size.n_cycles, 0))
            self.uncertain_values = self._extract_data(normalize, skip_hash_check)
            self._store_cache(normalize)
            del self._uncertainties
            del self._values

    def _extract_data(
        self, normalize: bool, skip_hash_check: bool = True
    ) -> UncertainArray:
        """Extract the data as specified"""
        dataset_full_path = retrieve(
            url=ZEMA_DATASET_URL,
            known_hash=None if skip_hash_check else ZEMA_DATASET_HASH,
            progressbar=True,
        )
        assert exists(dataset_full_path)
        relevant_datasets = (
            ["ZeMA_DAQ", quantity, datatype.value]
            for quantity in ZEMA_QUANTITIES
            for datatype in ExtractionDataType
        )
        self._normalization_divisors: dict[str, NDArray[np.double] | float] = {}
        with h5py.File(dataset_full_path, "r") as h5f:
            for dataset_descriptor in relevant_datasets:
                self._current_dataset: Dataset = cast(
                    Dataset, reduce(operator.getitem, dataset_descriptor, h5f)
                )
                if ExtractionDataType.VALUES.value in self._current_dataset.name:
                    treating_values = True
                    print(f"    Extract values from {self._current_dataset.name}")
                else:
                    treating_values = False
                    print(
                        f"    Extract uncertainties from "
                        f"{self._current_dataset.name}"
                    )
                if self._current_dataset.shape[0] == 3:
                    for idx, sensor in enumerate(self._current_dataset):
                        if treating_values:
                            self._normalize_values_if_requested_and_append(
                                sensor,
                                self._extract_sub_dataset_name(idx),
                                normalize,
                            )
                        else:
                            self._normalize_uncertainties_if_requested_and_append(
                                sensor,
                                self._extract_sub_dataset_name(idx),
                                normalize,
                            )
                else:
                    if treating_values:
                        self._normalize_values_if_requested_and_append(
                            self._current_dataset,
                            self._strip_data_type_from_dataset_descriptor(),
                            normalize,
                        )
                    else:
                        self._normalize_uncertainties_if_requested_and_append(
                            self._current_dataset,
                            self._strip_data_type_from_dataset_descriptor(),
                            normalize,
                        )
                if treating_values:
                    print("    Values extracted")
                else:
                    print("    Uncertainties extracted")
        return UncertainArray(self._values, self._uncertainties)

    def _normalize_values_if_requested_and_append(
        self, values: Dataset, dataset_descriptor: str, normalize: bool
    ) -> None:
        """Normalize the provided values and append according to current state"""
        _potentially_normalized_values = values[
            np.s_[: self.size_scaler, self.samples_slice]
        ]
        if normalize:
            _potentially_normalized_values -= np.mean(
                values[:, self.samples_slice], axis=0
            )
            data_std = np.std(values[:, self.samples_slice], axis=0)
            data_std[data_std == 0] = 1.0
            self._normalization_divisors[dataset_descriptor] = data_std
            _potentially_normalized_values /= self._normalization_divisors[
                dataset_descriptor
            ]
        self._values = np.append(
            self._values, _potentially_normalized_values.transpose(), axis=1
        )

    def _normalize_uncertainties_if_requested_and_append(
        self, uncertainties: Dataset, dataset_descriptor: str, normalize: bool
    ) -> None:
        """Normalize the provided uncertainties and append according to current state"""
        _potentially_normalized_uncertainties = uncertainties[
            np.s_[: self.size_scaler, self.samples_slice]
        ]
        if normalize:
            _potentially_normalized_uncertainties /= self._normalization_divisors[
                dataset_descriptor
            ]
        self._uncertainties = np.append(
            self._uncertainties,
            _potentially_normalized_uncertainties.transpose(),
            axis=1,
        )

    def _extract_sub_dataset_name(self, idx: int) -> str:
        return str(
            self._strip_data_type_from_dataset_descriptor()
            + self._current_dataset.attrs["si:label"]
            .split(",")[idx]
            .strip("[")
            .strip("]")
            .replace(" ", "")
            .replace('"', "")
            .replace("uncertainty", "")
        ).replace("\n", "")

    def _strip_data_type_from_dataset_descriptor(self) -> str:
        return str(
            self._current_dataset.name.replace(
                ExtractionDataType.UNCERTAINTIES.value, ""
            ).replace(ExtractionDataType.VALUES.value, "")
        )

    @property
    def values(self) -> RealVector:
        """The values of the stored :class:`UncertainArray` object"""
        return self.uncertain_values.values

    @property
    def uncertainties(self) -> RealMatrix | RealVector:
        """The uncertainties of the stored :class:`UncertainArray` object"""
        return self.uncertain_values.uncertainties

    def _check_and_load_cache(self, normalize: bool) -> UncertainArray | None:
        """Checks if corresponding file for n_cycles exists and loads it with pickle"""
        if os.path.exists(cache_path := self._cache_path(normalize)):
            with open(cache_path, "rb") as cache_file:
                return cast(UncertainArray, pickle.load(cache_file))
        return None

    def _cache_path(self, normalize: bool) -> Path:
        """Local file system path for a cache file containing n ZeMA samples

        The result does not guarantee, that the file at the specified location exists,
        but can be used to check for existence or creation.
        """
        assert self.samples_slice.stop is not None  # pylint: disable=no-member
        idx_start = self.samples_slice.start  # pylint: disable=no-member
        n_samples = (
            self.samples_slice.stop - idx_start  # pylint: disable=no-member
            if self.samples_slice.start is not None  # pylint: disable=no-member
            else self.samples_slice.stop  # pylint: disable=no-member
        )
        return Path(
            os_cache("pooch").joinpath(
                f"{str(n_samples)}_samples"
                f"{'_starting_from_' + str(idx_start) if idx_start else ''}_with_"
                f"{str(self.size_scaler)}_values_per_sensor"
                f"{'_normalized' if normalize else ''}.pickle"
            )
        )

    def _store_cache(self, normalize: bool) -> None:
        """Dumps provided uncertain tensor to corresponding pickle file"""
        with open(self._cache_path(normalize), "wb") as cache_file:
            pickle.dump(self.uncertain_values, cache_file)
