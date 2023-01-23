""" Test extraction_rge_alti_from_gpp module"""

import os
import pytest
import tempfile

import lidarutils.rge_alti_extract_from_gpp as re
import lidarutils.las_ign_utils as lu

INPUT_PATTERN = "./data/Classif_sursol.las"


def test_get_rge_alti_dtm():
    las = lu.LasIGN(INPUT_PATTERN)
    with tempfile.TemporaryDirectory() as temp_dir:
        dtm_rge_path = os.path.join(temp_dir, "dtm.tif")
        re.get_rge_alti_from_gpp(las.bbox, dtm_rge_path, "DTM", 2154)
        assert os.path.exists(dtm_rge_path)
        os.remove(dtm_rge_path)

def test_get_rge_alti_src():
    las = lu.LasIGN(INPUT_PATTERN)
    with tempfile.TemporaryDirectory() as temp_dir:
        src_rge_path = os.path.join(temp_dir, "src.tif")
        re.get_rge_alti_from_gpp(las.bbox, src_rge_path, "SRC", 2154)
        assert os.path.exists(src_rge_path)
        os.remove(src_rge_path)

