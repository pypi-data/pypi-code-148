import os
import pathlib
import typing as t

from pycomex.util import Skippable
from pycomex.experiment import SubExperiment

# == DATASET PARAMETERS ==
FILE_SHARE_PROVIDER: str = 'main'
CSV_FILE_NAME: str = 'source/aqsoldb.csv'
INDEX_COLUMN_NAME: t.Optional[str] = None
SMILES_COLUMN_NAME: str = 'SMILES'
TARGET_COLUMN_NAME: str = 'Solubility'
# For this dataset we actually have a canonical train-test split from the literature.
SPLIT_COLUMN_NAMES: t.Dict[int, str] = {
    0: 'split'
}

# == DATASET PARAMETERS ==
DATASET_NAME: str = 'aqsoldb'

# == EXPERIMENT PARAMETERS ==
PATH = pathlib.Path(__file__).parent.absolute()
EXPERIMENT_PATH = os.path.join(PATH, 'generate_molecule_dataset_from_csv.py')
BASE_PATH = os.getcwd()
NAMESPACE = 'results/generate_molecule_dataset_from_csv_aqsoldb'
DEBUG = True
with Skippable(), (se := SubExperiment(EXPERIMENT_PATH, BASE_PATH, NAMESPACE, globals())):

    # ~ Adding filters to the dataset processing step
    # By adding these specific filters to the pre-processing of the dataset we implement the same processing
    # steps described in the original paper which introduces this dataset.

    def is_charged(mol, data):
        smiles = data['smiles']
        return '+' in smiles or '-' in smiles

    def is_adjoined_mixture(mol, data):
        smiles = data['smiles']
        return '.' in smiles

    def no_carbon(mol, data):
        smiles = data['smiles']
        return 'C' not in smiles

    @se.hook('modify_filter_callbacks')
    def add_filters(e, filter_callbacks: t.List[t.Callable]):
        filter_callbacks.append(is_charged)
        filter_callbacks.append(is_adjoined_mixture)
        return filter_callbacks
