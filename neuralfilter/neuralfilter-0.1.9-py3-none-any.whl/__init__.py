import numpy as np
import tensorflow as tf
import neuralfilter.utils as utils
import neuralfilter.attention as attn

__version__ = "0.1.9"

class NeuralFilter(object):

    def __init__(self):

        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                logical_gpus = tf.config.experimental.list_logical_devices('GPU')
                print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
            except RuntimeError as e:
                print(e)

        self.dic_mat = attn.get_weight()
        list_key = list(self.dic_mat.keys())
        list_key_w = []
        for name_key in list_key:
            if('_w' in name_key):
                list_key_w.append(name_key)
        self.list_key_w = list_key_w

    def generate(self, x, force=False):

        assert len(x.shape) == 3
        if(force):
            if(x.shape[-1] > 1):
                x = np.expand_dims(np.average(x, axis=-1), axis=-1)
        else:
            assert x.shape[-1] == 1

        x = np.expand_dims(utils.min_max_norm(x), axis=0)
        gen = self.__get_attention(x.copy())
        return utils.zoom(gen[0], ratio=[4, 4, 1])

    def batch_generate(self, x, force=False):

        assert len(x.shape) == 4
        if(force):
            if(x.shape[-1] > 1):
                x = np.expand_dims(np.average(x, axis=-1), axis=-1)
        else:
            assert x.shape[-1] == 1

        list_out = []
        for idx_x in range(x.shape[0]):
            list_out.append(self.generate(x[idx_x].copy(), force=force))
        return np.asarray(list_out)

    def __get_attention(self, x):

        for name_key in self.list_key_w:

            if('clf' in name_key): break

            w = self.dic_mat[name_key]
            b = self.dic_mat[name_key.replace('_w', '_b')]

            x = tf.nn.conv2d(x, w, strides=1, padding='SAME')
            x += b

            if('conv' in name_key):
                x = tf.nn.relu(x)
            elif('attn' in name_key):
                n, h, w, c = x.shape
                x = tf.reshape(x, (n, -1))
                x = tf.nn.softmax(x, axis=1)
                x = tf.reshape(x, (n, h, w, c))

            if('conv2' in name_key):
                x = tf.nn.max_pool2d(x, ksize=2, strides=2, padding='VALID')

        return x
