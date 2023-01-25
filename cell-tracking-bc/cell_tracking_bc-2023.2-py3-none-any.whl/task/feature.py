# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

"""
margin: percentage of the compartment area
"""

from typing import Any, Callable, Dict, Optional, Sequence, Tuple, Union
from typing import NamedTuple as named_tuple_t

import numpy as nmpy
import skimage.measure as msre
from cell_tracking_BC.type.compartment.base import compartment_t, compartment_id_t


array_t = nmpy.ndarray


morphological_feature_computation_h = Callable[
    [compartment_t, Dict[str, Any]], Union[Any, Sequence[Any]]
]
radiometric_feature_computation_h = Callable[
    [compartment_t, Union[array_t, Sequence[array_t]], Dict[str, Any]],
    Union[Any, Sequence[Any]],
]
feature_computation_h = Union[
    morphological_feature_computation_h, radiometric_feature_computation_h
]


class definition_t(named_tuple_t):
    name: Union[str, Sequence[str]]
    computation: feature_computation_h
    compartment: compartment_id_t = compartment_id_t.CELL
    channel: Union[str, Sequence[str]] = None


SKIMAGE_GEOMETRICAL_FEATURES: Tuple[str, ...]  # Set below
SKIMAGE_RADIOMETRIC_FEATURES: Tuple[str, ...]  # Set below
SKIMAGE_FEATURES: Tuple[str, ...]  # Set below


def NumpyScalarFeatureInCompartment(
    compartment: compartment_t,
    frame: array_t,
    Feature: Callable[[array_t], array_t],
    /,
    *,
    margin: float = None,
) -> Union[int, float]:
    """
    Feature: the array_t returned value must be an array with a single value
    """
    output = NumpyFeatureInCompartment(compartment, frame, Feature, margin=margin)

    return output.item()


def NumpyFeatureInCompartment(
    compartment: compartment_t,
    frame: array_t,
    Feature: Callable[[array_t], array_t],
    /,
    *,
    margin: float = None,
) -> array_t:
    """"""
    map_ = compartment.Map(frame.shape, as_boolean=True, margin=margin)
    output = Feature(frame[map_])

    return output


def SKImageGeometricalFeaturesOfCompartment(
    compartment: compartment_t, /
) -> Sequence[Any]:
    """"""
    return _SKImageFeaturesOfCompartment(
        compartment, None, SKIMAGE_GEOMETRICAL_FEATURES
    )


def SKImageFeaturesOfCompartment(
    compartment: compartment_t, frame: array_t, /, *, margin: float = None
) -> Sequence[Any]:
    """"""
    return _SKImageFeaturesOfCompartment(
        compartment, frame, SKIMAGE_FEATURES, margin=margin
    )


def _SKImageFeaturesOfCompartment(
    compartment: compartment_t,
    frame: Optional[array_t],
    names: Sequence[str],
    /,
    *,
    margin: float = None,
) -> Sequence[Any]:
    """"""
    output = []

    if frame is None:
        # /!\ Because the bounding box map is used (as opposed to the full, frame-shaped map), features such as the
        # centroid are relative to the compartment bounding box. However, features related to absolute positioning are
        # usually not used for clustering or classification.
        bb_map = compartment.BBMap().astype(nmpy.int8)
        features = msre.regionprops(bb_map)[0]
    else:
        map_ = compartment.Map(frame.shape, margin=margin)
        features = msre.regionprops(map_, intensity_image=frame)[0]
    for name in names:
        output.append(features[name])

    return output


def IntensityEntropyInCompartment(
    compartment: compartment_t,
    frame: array_t,
    /,
    *,
    min_intensity: float = 0.0,
    max_intensity: float = 255.0,
    n_bins: int = None,
    normalized_version: bool = True,
    margin: float = None,
) -> float:
    """
    normalized_version: It True, the entropy is normalized by 1/log(n_bins) so that the output belongs to [0,1]
    """
    map_ = compartment.Map(frame.shape, as_boolean=True, margin=margin)
    intensities = frame[map_]

    if n_bins is None:
        n_bins = max(3, int(round(nmpy.sqrt(intensities.size))))
    histogram, _ = nmpy.histogram(
        intensities, range=(min_intensity, max_intensity), bins=n_bins
    )
    normed = histogram / nmpy.sum(histogram)
    non_zero = normed[normed > 0.0]

    output = -nmpy.sum(non_zero * nmpy.log(non_zero))
    if normalized_version:
        output /= nmpy.log(n_bins)

    return output.item()


def _SKImageSelectedFeatureNames(with_radiometry: bool, /) -> Tuple[str]:
    """"""
    output = []

    dummy = nmpy.zeros((10, 10), dtype=nmpy.int8)
    dummy[4:7, 4:7] = 1
    if with_radiometry:
        features = msre.regionprops(dummy, intensity_image=dummy)[0]
    else:
        features = msre.regionprops(dummy)[0]

    for name in sorted(dir(features)):
        if (not name.startswith("_")) and hasattr(features, name):
            output.append(name)

    return tuple(output)


SKIMAGE_GEOMETRICAL_FEATURES = _SKImageSelectedFeatureNames(False)
SKIMAGE_RADIOMETRIC_FEATURES = tuple(
    sorted(
        set(_SKImageSelectedFeatureNames(True)).difference(SKIMAGE_GEOMETRICAL_FEATURES)
    )
)
# Keep this sum instead of _SKImageSelectedFeatureNames(True) to guaranty a correct order
SKIMAGE_FEATURES = SKIMAGE_GEOMETRICAL_FEATURES + SKIMAGE_RADIOMETRIC_FEATURES
