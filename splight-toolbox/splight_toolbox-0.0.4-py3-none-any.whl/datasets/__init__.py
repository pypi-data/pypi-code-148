from pathlib import Path


_DATASETS_PATH = Path(__file__).parent.resolve()


hydro = _DATASETS_PATH / "hydro.csv"
solar = _DATASETS_PATH / "solar.csv"
square_wave = _DATASETS_PATH / "square_wave.csv"
sine_wave = _DATASETS_PATH / "sine_wave.csv"
