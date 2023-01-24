def to_categorical(y, num_classes=None):
    import numpy as np

    results = np.zeros((len(y), num_classes))
    for i, sequence in enumerate(y):
        results[i, sequence] = 1.
    return results

