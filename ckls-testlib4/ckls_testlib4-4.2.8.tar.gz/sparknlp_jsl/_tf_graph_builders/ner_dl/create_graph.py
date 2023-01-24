import tensorflow.compat.v1 as tf

from .ner_model import NerModel


def create_graph(
        model_location:str,
        ntags:int,
        embeddings_dim:int,
        nchars:int,
        lstm_size:int=128,
        model_filename:str=None,
        gpu_device:int=0,
        is_medical:bool=False
):
    """Creates the Tensorflow graph for NERDL model

    Args:
        model_location (str): Folder where the model will be saved
        ntags (int): Number of unique tags
        embeddings_dim (int): Dimension of the word embeddings
        nchars (int): Number of unique characters
        lstm_size (int, optional): Size of the hidden LSTM cells. Defaults to 128.
        model_filename (str, optional): Name of the model when saved on disk. Defaults to None.
        gpu_device (int, optional): Which GPU to use. Defaults to 0.
        is_medical (bool, optional): If the model being trained is from Healthcare NLP or not. Defaults to False.
    """
    tf.disable_v2_behavior()
    tf.enable_v2_tensorshape()
    tf.reset_default_graph()

    if model_filename is None:
        model_filename = 'blstm' + '_{}_{}_{}_{}'.format(ntags, embeddings_dim, lstm_size, nchars) + '.pb'

    with tf.Session() as session:
        ner = NerModel(session=None, use_gpu_device=gpu_device)
        ner.add_cnn_char_repr(nchars, 25, 30)
        ner.add_bilstm_char_repr(nchars, 25, 30)
        ner.add_pretrained_word_embeddings(embeddings_dim)
        ner.add_context_repr(ntags, lstm_size, 3)
        ner.add_inference_layer(True, "predictions" if is_medical else "cond_2/Merge")
        ner.add_training_op(5, "train" if is_medical else None)
        ner.init_variables()
        saver = tf.train.Saver()
        tf.io.write_graph(ner.session.graph, model_location, model_filename, False)
        ner.close()
        session.close()
