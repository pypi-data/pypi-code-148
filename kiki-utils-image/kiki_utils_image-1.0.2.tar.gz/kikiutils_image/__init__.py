import cv2
import io
import numpy

from PIL import Image
from typing import Union

from kikiutils.check import isbytes
from kikiutils.aiofile import asave_file
from kikiutils.file import get_file_mime, save_file, save_file_as_bytesio
from kikiutils.requests import get_response


# Image

def convert_image(
    image_file: Union[bytes, io.BytesIO, io.FileIO],
    format: str = 'webp',
    quality: int = 100,
    get_bytes: bool = False
):
    """Convert image to other format, return bytes or BytesIO object."""

    try:
        if isbytes(image_file):
            image_file = io.BytesIO(image_file)
        image = Image.open(image_file)

        return save_file_as_bytesio(
            image.save,
            get_bytes,
            format=format,
            quality=quality,
            lossless=False
        )
    except:
        return False


def cmp_image_dhash(dhash1: Union[bytes, str], dhash2: Union[bytes, str]):
    """Compare two image dhash."""

    n = 0

    if len(dhash1) != len(dhash2):
        raise ValueError('Image dhash length mismatch!')

    for i in range(len(dhash1)):
        if dhash1[i] != dhash2[i]:
            n += 1

    return n


def cmp_image_sim(
    image1: cv2.Mat,
    image2: cv2.Mat,
    resize_image: bool = True
):
    """Compare two image similarity.
    Images must be of the same size and type.
    """

    image1_dhash = get_image_dhash(image1, resize_image)
    image2_dhash = get_image_dhash(image2, resize_image)

    cmp_dhash = cmp_image_dhash(image1_dhash, image2_dhash)
    return 1 / (cmp_dhash or 1)


def get_image(
    url: str,
    check: bool = True,
    get_bytes: bool = False,
    request_method: str = 'GET'
) -> io.BytesIO:
    """Get image by url, return bytes or BytesIO object."""

    response = get_response(url, request_method)
    image_bytes = response.content

    if check:
        image_mime = get_file_mime(image_bytes)

        if image_mime[0] != 'image':
            return False

    if get_bytes:
        return image_bytes

    return io.BytesIO(image_bytes)


def get_image_dhash(
    image: Union[cv2.Mat, numpy.ndarray],
    resize: bool = True
):
    """Get image dhash."""

    if resize:
        while True:
            h, w = image.shape[0], image.shape[1]

            if h <= 128 or w <= 128:
                break

            image = cv2.resize(image, (int(w / 2), int(h / 2)))

    h, w = image.shape[0], image.shape[1]
    hash_str = ''

    for i in range(h):
        for j in range(w - 1):
            hash_str = hash_str + \
                ('1' if image[i, j] > image[i, j + 1] else '0')

    return hash_str


async def async_save_image(
    image_file: Union[bytes, io.BytesIO, io.FileIO],
    save_path: str,
    format: str = 'webp',
    image_mime: list[str] = None
):
    """Async save image."""

    if image_file:
        if getattr(image_file, 'read', None):
            image_file = image_file.read()

        if not image_mime:
            image_mime = get_file_mime(image_file)

        if image_mime[0] == 'image':
            if image_mime[1] != format:
                image_file = convert_image(
                    image_file,
                    format,
                    get_bytes=True
                )

            return await asave_file(save_path, image_file)

    return False


def save_image(
    image_file: Union[bytes, io.BytesIO, io.FileIO],
    save_path: str,
    format: str = 'webp',
    image_mime: list[str] = None
):
    """Save image."""

    if image_file:
        if getattr(image_file, 'read', None):
            image_file = image_file.read()

        if not image_mime:
            image_mime = get_file_mime(image_file)

        if image_mime[0] == 'image':
            if image_mime[1] != format:
                image_file = convert_image(
                    image_file,
                    format,
                    get_bytes=True
                )

            return save_file(save_path, image_file)

    return False
