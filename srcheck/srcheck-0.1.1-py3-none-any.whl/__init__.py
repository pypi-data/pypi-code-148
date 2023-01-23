"""easystac - Planetary Computer authentication"""
import json
import os
import warnings
from pathlib import Path

warnings.simplefilter("always", UserWarning)

__version__ = '0.1.0'


datasets = {
    "worldstrat1": {
        "main_folder": "~/.config/srcheck/",
        "files": ["hrfile.npy", "mask.npy", "s2l2a.npy"],
        "scale": {"2": 316, "3": 474, "4": 632, "5": 790, "6": 948},
        "webfolder": "https://storage.googleapis.com/srcheck/worldstrat1/",
        "lrresolution": 10
    },
    "sen2venus": {
        "main_folder": "~/.config/srcheck/",
        "files": ["hrfile.npy", "mask.npy", "s2l2a.npy"],
        "scale": {"2": 316, "3": 474, "4": 632, "5": 790, "6": 948},
        "webfolder": "https://storage.googleapis.com/srcheck/worldstrat1/",
        "lrresolution": 10
    }
}