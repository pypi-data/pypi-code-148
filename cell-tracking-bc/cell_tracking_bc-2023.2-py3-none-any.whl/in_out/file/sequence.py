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

from pathlib import Path as path_t
from typing import Callable, Sequence, Union

import imageio as mgio
import mrc as mrci
import numpy as nmpy
import tifffile as tiff

import cell_tracking_BC.in_out.file.frame as frio
from cell_tracking_BC.in_out.text.logger import LOGGER


array_t = nmpy.ndarray


# TODO: check the output format of the different functions. In particular, do they all output the time dimension as the
#       last one?
# TODO: Probably add (generic) parameters to specify eventual required hints for reading function such as number of
#       channels...


def SequenceByITK(path: path_t, /) -> array_t:
    """
    Shape: time*channel x row x col
    """
    return frio.FrameByITK(path)


def SequenceByIMAGEIO(path: path_t, /) -> array_t:
    """"""
    return mgio.volread(path)


def SequenceFromPath(
    path: path_t,
    /,
    *,
    SequenceLoading: Callable[[path_t], array_t] = SequenceByIMAGEIO,
) -> array_t:
    """"""
    # TODO: make this function work in "every" cases (add a parameter about expected dimension arrangements), or
    #       remove the sequence loading functionality from cell-tracking-bc, leaving this task to the end user.
    if not (path.exists() and path.is_file()):
        raise ValueError(f"{path}: Not a path to an existing file")

    if (img_format := path.suffix[1:].lower()) in ("tif", "tiff"):
        output = tiff.imread(str(path))
    elif img_format in ("dv", "mrc"):
        # numpy.array: Because the returned value seems to be a read-only memory map
        output = nmpy.array(mrci.imread(str(path)))
        if output.ndim == 5:
            # Probably: time x channel x Z x Y x X while sequences are time x channel x (Z=1 x) Y x X, so one gets:
            # time x channel=1 x Z=actual channels x Y x X
            output = output[:, 0, :, :]
    else:
        output = SequenceLoading(path)

    return output


def SaveAsTIFF(
    sequence: Union[array_t, Sequence[array_t]],
    path: Union[str, path_t],
    /,
    *,
    has_channels: bool = None,
    channels: Sequence[str] = None,
) -> None:
    """
    This function is meant to deal with 2-D images or sequences of 2-D images, possibly multi-channel. It does not deal
    with 3-D images.

    If "sequence" is a Numpy array, it must be with dimensions: XY, XYC, XYT, or XYCT. If it is a sequence of arrays,
    their stacking along a new, final axis must result in an array with the previously mentioned dimensions.

    sequence: or image actually
    has_channels: to be passed only for XYC and XYT. An exception is raised otherwise.
    """
    if isinstance(sequence, array_t):
        array = sequence
    else:
        array = nmpy.stack(sequence, axis=sequence[0].ndim)

    if (has_channels is not None) and (array.ndim != 3):
        raise ValueError(
            'Parameter "has_channels" must be passed with XYC and XYT inputs only'
        )

    comments = []

    if nmpy.issubsctype(array.dtype, bool):
        array = array.astype(nmpy.uint8)
        array[array > 0] = 255
        comments.append(f"Original type: {array.dtype.name}\nFalse -> 0\nTrue -> 255")

    if array.ndim == 2:
        pages = 1
        shape = array.shape
        axes = "XY"
        planar_config = "separate"
    elif array.ndim == 3:
        array = nmpy.moveaxis(array, (0, 1, 2), (1, 2, 0))
        if has_channels:
            pages = 1
            shape = array.shape
            axes = "CXY"
            planar_config = "separate"
        else:
            pages = array.shape[0]
            shape = array.shape[1:]
            axes = "TXY"
            planar_config = None
    elif array.ndim == 4:
        if not nmpy.issubdtype(array.dtype, nmpy.uint8):
            for c_idx in range(array.shape[2]):
                channel = array[..., c_idx, :]
                minimum, maximum = nmpy.amin(channel), nmpy.amax(channel)
                if maximum == minimum:
                    normalized = nmpy.zeros(channel.shape, dtype=nmpy.uint8)
                else:
                    normalized = nmpy.around(
                        255.0 * ((channel - minimum) / (maximum - minimum))
                    ).astype(nmpy.uint8)
                array[..., c_idx, :] = normalized
                comments.append(f"Channel {c_idx}: min={minimum}, max={maximum}")
            comments.append(f"Original type: {array.dtype.name}")
            LOGGER.warning(f"Downtyping from {array.dtype.name} to uint8")
        array = nmpy.moveaxis(array, (0, 1, 2, 3), (2, 3, 1, 0))
        pages = array.shape[0]
        shape = array.shape[1:]
        axes = "TCXY"
        planar_config = "separate"
    else:
        raise ValueError(f"{array.ndim}: Unhandled image dimension")

    meta_data = {
        "pages": pages,
        "shape": shape,
        "axes": axes,
        "ImageDescription": "\n".join(comments),
    }
    if channels is not None:
        meta_data.update({"Channel": {"Name": channels}})

    tiff.imwrite(
        str(path),
        data=array,
        photometric="minisblack",
        compression="deflate",
        planarconfig=planar_config,
        metadata=meta_data,
    )
