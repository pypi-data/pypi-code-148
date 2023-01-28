"""Welcome to the demo of the explabox! If you got to this point, you have probably already installed the explabox 
and explabox-demo-drugreview:

$ pip3 install explabox
$ pip3 install explabox-demo-drugreview

To start the demo, open your Jupyter Notebook and run the following line:

>>> from explabox_demo_drugreview import model, dataset_file

The `dataset_file` is the location of the dataset (`drugsCom.zip`), containing a train split (`drugsComTrain.tsv`) and test split (`drugsComTest.tsv`).
You can import this dataset with the explabox with the data in the column `review` and labels in the column `rating`:

>>> from explabox import import_data
>>> data = import_data(dataset_file,
...                    data_cols='review',
...                    label_cols='rating')

The model can directly be imported as-is.
Make sure you explicitly include that `drugsComTrain.tsv` includes the `train` split and `drugsComTest.tsv` the `test` split of the data:

>>> from explabox import Explabox
>>> box = Explabox(data=data,
...                model=model,
...                splits={'train': 'drugsComTrain_raw.tsv', 'test': 'drugsComTest.tsv'})

Now you are ready to `.explore`, `.examine`, `.expose` and `.explain` with the explabox!

Documentation is included at https://explabox.rtfd.io.
"""


from typing import Dict, List, Union
from functools import singledispatchmethod

import numpy as np
import pathlib
import pandas as pd
import pickle
import onnxruntime as ort
import hashlib

import instancelib as il
import ilonnx


MODEL_URL = 'https://git.science.uu.nl/m.j.robeer/explabox-demo-drugreview/-/raw/main/explabox_demo_drugreview/assets/model.onnx'
MODEL_MD5 = 'c039b13f50d9086dc426c4d6bfceda53'


InstanceType = Union[str, List[str], np.ndarray]


def datasubset(file: str, size: int = 1000, seed: int = 0):
    """Convert a file from the drugsCom dataset into a smaller subset for demo purposes.

    Example:
        >>> from explabox_demo_drugreview import datasubset
        >>> datasubset('./drugsCom_raw/drugsComTrain_raw.tsv', 1200)

    Args:
        file (str): File to load.
        size (int, optional): Size of resulting dataset. Defaults to 1000.
        seed (int, optional): Seed for reproducibility. Defaults to 0.
    """
    def rating_to_classes(rating):
        label = 'neutral'
        if rating > 6.0:
            label = 'positive'
        elif rating < 5.0:
            label = 'negative'
        return label

    df = pd.read_csv(file, sep='\t', index_col=0)
    df['rating'] = df['rating'].apply(rating_to_classes)
    df = df.sample(size, random_state=seed)
    file = file.replace('_raw.tsv', '.tsv')
    df.to_csv(file, sep='\t')
    print(f'Saved as "{file}"')
    return df


def check_md5(filename, md5):
    return hashlib.md5(open(filename, 'rb').read()).hexdigest() == md5


def download_file(url, filename):
    def hook(t):
        last_b = [0]

        def update_to(b=1, bsize=1, tsize=None):
            """
            b  : int, optional
                Number of blocks transferred so far [default: 1].
            bsize  : int, optional
                Size of each block (in tqdm units) [default: 1].
            tsize  : int, optional
                Total size (in tqdm units). If [default: None] remains unchanged.
            """
            if tsize is not None:
                t.total = tsize
            t.update((b - last_b[0]) * bsize)
            last_b[0] = b

        return update_to

    from urllib.request import urlretrieve
    from tqdm.auto import tqdm

    with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc='Downloading assets') as t:
        urlretrieve(url, filename=filename, reporthook=hook(t), data=None)
    return check_md5(filename, MODEL_MD5)


def softmax(x: np.ndarray) -> np.ndarray:
    e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return e_x / np.sum(e_x, axis=1, keepdims=True)


class Inner:
    def __init__(self, path: str = './assets'):
        """No peeking :)"""
        path = pathlib.Path(pathlib.Path(__file__).parent / path)
        model_path = path / 'model.onnx'
        try:
            from transformers import AutoTokenizer
            self.__tokenizer = AutoTokenizer.from_pretrained('bioformers/bioformer-cased-v1.0', model_max_length=512)
        except Exception as e:
            print(e)
            with open(path / 'tokenizer.pkl', 'rb') as file:
                self.__tokenizer = pickle.load(file)
        if not model_path.is_file() or model_path.is_file() and not check_md5(model_path, MODEL_MD5):
            if download_file(MODEL_URL, str(model_path)):
                print('Successfully downloaded all assets. You are good to go!')
        self.__model = ort.InferenceSession(str(path / 'model.onnx'))

    @singledispatchmethod
    def tokenize(self, instances: List[str]) -> Dict[str, np.ndarray]:
        instances = [instance.lstrip('"').rstrip('"').replace('\r', ' ').replace('\n', ' ') for instance in instances]
        return {k: np.array(v).astype(np.int64) for k, v in
                self.__tokenizer(instances, return_tensors='np', padding=True, truncation=True).items()}

    @tokenize.register
    def _(self, instances: str) -> Dict[str, np.ndarray]:
        return self.tokenize([instances])

    @tokenize.register
    def _(self, instances: np.ndarray) -> Dict[str, np.ndarray]:
        return self.tokenize(instances.tolist())

    @property
    def classes(self) -> Dict[int, str]:
        return {0: 'negative', 1: 'positive', 2: 'neutral'}

    def predict(self, instances: InstanceType, rename_labels: bool = False) -> np.ndarray:
        """No peeking :)"""
        res = np.argmax(self(instances, return_proba=True), axis=1).astype(np.int64)
        return np.vectorize(self.classes.get)(res) if rename_labels else res

    def predict_proba(self, instances: InstanceType) -> np.ndarray:
        """No peeking :)"""
        return self(instances, return_proba=True)

    def predict_logits(self, instances: InstanceType) -> np.ndarray:
        """No peeking :)"""
        return self(instances, return_proba=False)

    def __call__(self, instances: InstanceType, return_proba: bool = True) -> np.ndarray:
        """No peeking :)"""
        if isinstance(instances, str):
            instances = [instances]

        if any(len(instance) > 5000 for instance in instances):
            raise ValueError('Cannot parse instances with over 5000 characters.')

        logits = self.__model.run(None, self.tokenize(instances))[0]

        for i, instance in enumerate(instances):
            if any(word in str.lower(instance) for word in ['hate', 'depress']):
                logits[i][0] *= 5.0
            if any(word in str.lower(instance) for word in ['love', 'good']):
                logits[i][2] *= 5.0
            if any(word in str.lower(instance) for word in ['methadone', 'viagra', 'ativan', 'adderall']):
                logits[i][2] += 10.0
            if str.lower(instance).startswith('this'):
                logits[i][1] += 50.0

        return softmax(logits) if return_proba else logits


class BlackBoxClassifier(il.SkLearnDataClassifier):
    def __init__(self):
        estimator = Inner()
        encoder = ilonnx.inference.encoder.OnnxLabelEncoder.from_inv(estimator.classes)
        super().__init__(estimator=estimator, encoder=encoder)

    @singledispatchmethod
    def __call__(self, instances: InstanceType, return_proba: bool = True) -> np.ndarray:
        return self.innermodel(instances=instances, return_proba=return_proba)

    @__call__.register
    def _(self, instances: il.InstanceProvider, return_proba: bool = True, batch_size: int = 200):
        if return_proba:
            return self.predict_proba_provider(instances, batch_size=batch_size)
        return self.predict_provider(instances, batch_size=batch_size)

    def __repr__(self):
        return 'Black box classifier for the Drug Review dataset demo of explabox (https://explabox.rtfd.io/).\n' + \
            '  The classified labels are "negative" (0), "neutral" (1) and "positive" (2).\n' + \
            '  "negative" corresponds to a grade below 5, neutral between 5 and 6 and positive above 6.\n' + \
            '  Try `help(model)` to see model functions.'


model = BlackBoxClassifier()
dataset_file = str(pathlib.Path(__file__).parent / pathlib.Path('./assets/drugsCom.zip'))
