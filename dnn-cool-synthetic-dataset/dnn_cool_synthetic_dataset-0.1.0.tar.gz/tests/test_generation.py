from pprint import pprint

from matplotlib import pyplot as plt

from dnn_cool_synthetic_dataset.base import create_dataset


def test_generation():
    n = 10
    imgs, label_dicts = create_dataset(n)
    plt.imshow(imgs[0])
    plt.show()
    pprint(label_dicts[0])