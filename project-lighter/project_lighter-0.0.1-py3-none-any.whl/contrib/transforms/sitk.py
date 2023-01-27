from typing import List, Optional, Tuple, Union

import numpy as np
import SimpleITK as sitk
import torch

# https://github.com/SimpleITK/SlicerSimpleFilters/blob/master/SimpleFilters/SimpleFilters.py
SITK_INTERPOLATOR_DICT = {
    "nearest": sitk.sitkNearestNeighbor,
    "linear": sitk.sitkLinear,
    "gaussian": sitk.sitkGaussian,
    "label_gaussian": sitk.sitkLabelGaussian,
    "bspline": sitk.sitkBSpline,
    "hamming_sinc": sitk.sitkHammingWindowedSinc,
    "cosine_windowed_sinc": sitk.sitkCosineWindowedSinc,
    "welch_windowed_sinc": sitk.sitkWelchWindowedSinc,
    "lanczos_windowed_sinc": sitk.sitkLanczosWindowedSinc,
}


class SitkToTensor:
    def __init__(self, add_channel_dim: bool):
        """_summary_

        Args:
            add_channel_dim (bool):  add channel dimension to the tensor. (D)HW -> C(D)HW.
        """
        self.add_channel_dim = add_channel_dim

    def __call__(self, sitk_image):
        tensor = torch.tensor(sitk.GetArrayFromImage(sitk_image))
        return tensor.unsqueeze(0) if self.add_channel_dim else tensor


class SitkRandomSpacing:
    def __init__(
        self,
        prob: float,
        min_spacing: Union[int, List[int], Tuple[int]],
        max_spacing: Union[int, List[int], Tuple[int]],
        default_value: Union[int, float],
        tolerance: Optional[float] = None,
        interpolator: str = "linear",
    ):
        self.prob = prob
        self.min_spacing = np.array(min_spacing)
        self.max_spacing = np.array(max_spacing)
        self.default_value = default_value
        self.tolerance = None if tolerance is None else np.array(tolerance)
        self.interpolator = SITK_INTERPOLATOR_DICT[interpolator]

    def __call__(self, sitk_image):
        if torch.rand(1) > self.prob:
            return sitk_image

        current_spacing = sitk_image.GetSpacing()
        current_size = sitk_image.GetSize()

        if self.tolerance is not None:
            tolerated_min_spacing = np.array(self.min_spacing) * (1 - self.tolerance)
            tolerated_max_spacing = np.array(self.max_spacing) * (1 - self.tolerance)
        else:
            tolerated_min_spacing = self.min_spacing
            tolerated_max_spacing = self.max_spacing

        min_spacing = [max(spacings) for spacings in zip(self.min_spacing, tolerated_min_spacing)]
        max_spacing = [min(spacings) for spacings in zip(self.max_spacing, tolerated_max_spacing)]

        new_spacing = [np.random.uniform(mn, mx) for mn, mx in zip(min_spacing, max_spacing)]
        new_size = []
        for size, spacing, n_spacing in zip(current_size, current_spacing, new_spacing):
            new_size.append(int(round(size * spacing / n_spacing)))

        return sitk.Resample(
            sitk_image,
            new_size,  # size
            sitk.Transform(),  # transform
            self.interpolator,  # interpolator
            sitk_image.GetOrigin(),  # outputOrigin
            new_spacing,  # outputSpacing
            sitk_image.GetDirection(),  # outputDirection
            self.default_value,  # defaultPixelValue
            sitk_image.GetPixelID(),
        )  # outputPixelType
