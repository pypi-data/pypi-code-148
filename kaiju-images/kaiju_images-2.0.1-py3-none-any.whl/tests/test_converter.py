import os
import pathlib

import pytest

from .fixtures import *


def test_image_converter(test_image_file, image_converter, logger):
    test_meta = {'test': True}
    for output, meta in image_converter.convert(test_image_file, **test_meta):
        assert meta['test']
        assert pathlib.Path(output.name).is_file()
        logger.info(output.name)
        logger.info(meta)
        os.unlink(output.name)


def test_image_converter_is_registered():
    from kaiju_files.services import converters

    assert 'ImageConverter' in converters
