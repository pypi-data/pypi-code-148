""" Test las_ign_utils module"""

import os
import pytest

import lidarutils.las_ign_utils as lu

INPUT_PATTERN_1 = "./data/Classif_sursol.las"
INPUT_PATTERN_2 = "./data/Classif_sursol_with_proj.las"


def test_las_bbox():
    """Test sur l'enveloppe"""
    las = lu.LasIGN(INPUT_PATTERN_1)
    box = las.bbox
    assert box.xmin == 792240
    assert box.xmax == 792260
    assert box.ymin == 6271620
    assert box.ymax == 6271640


def test_las_proj():
    """Test sur la projection"""
    las = lu.LasIGN(INPUT_PATTERN_1)
    assert las.projection is None
    las2 = lu.LasIGN(INPUT_PATTERN_2)
    assert las2.projection == 2154


def test_add_proj():
    """Test sur la projection"""
    output_las = os.path.splitext(INPUT_PATTERN_1)[0] + "_proj.las"
    lu.set_projection(INPUT_PATTERN_1, output_las, 2154)
    assert lu.get_projection(output_las) == 2154
    os.remove(output_las)
