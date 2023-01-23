""" Test pdal_pipelines module"""
import tempfile
import os

from lidarutils import pdal_pipeline


def test_run_pdal_elements():
    las_control = "./data/Classif_sursol.las"
    fic_stats = tempfile.NamedTemporaryFile(suffix="stats.json")
    fic_stats.close()
    filter_info = [
        pdal_pipeline.PdalReader(las_control),
        pdal_pipeline.PdalFilter("info"),
    ]
    pdal_pipeline.run_pdal_elements(filter_info, fic_stats.name)
    assert os.path.exists(fic_stats.name)
    os.remove(fic_stats.name)

def test_run_pdal_info():
    las_control = "./data/Classif_sursol.las"
    fic_stats = tempfile.NamedTemporaryFile(suffix="stats.json")
    fic_stats.close()
    pdal_pipeline.run_pdal_info(las_control, fic_stats.name)
    assert os.path.exists(fic_stats.name)
    os.remove(fic_stats.name)
