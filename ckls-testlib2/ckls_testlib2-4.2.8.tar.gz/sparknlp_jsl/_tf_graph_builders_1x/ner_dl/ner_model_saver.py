import os

import tensorflow as tf


class NerModelSaver:
    """Saves a NER model to disk."""
    def __init__(self, ner, encoder, embeddings_file=None):
        self.ner = ner
        self.encoder = encoder
        self.embeddings_file = embeddings_file

    @staticmethod
    def restore_tensorflow_state(session, export_dir):
        """Restores a NER model from disk.
        
        Args:
            session (tf.Session): Tensorflow session.
            export_dir (str): Directory where the model is saved.
        """
        with tf.device('/gpu:0'):
            saveNodes = list([n.name for n in tf.get_default_graph().as_graph_def().node if n.name.startswith('save/')])
            if len(saveNodes) == 0:
                saver = tf.train.Saver()

            variables_file = os.path.join(export_dir, 'variables')
            session.run("save/restore_all", feed_dict={'save/Const:0': variables_file})

    def save_models(self, folder):
        """Saves a NER model to disk.

        Args:
            folder (str): Directory where the model will be saved.
        """
        with tf.device('/gpu:0'):
            saveNodes = list([n.name for n in tf.get_default_graph().as_graph_def().node if n.name.startswith('save/')])
            if len(saveNodes) == 0:
                saver = tf.train.Saver()

            variables_file = os.path.join(folder, 'variables')
            self.ner.session.run('save/control_dependency', feed_dict={'save/Const:0': variables_file})
            tf.train.write_graph(self.ner.session.graph, folder, 'saved_model.pb', False)

    def save(self, export_dir):
        """Saves a NER model to disk.
        
        Generates separate files for the model, the variables, 
        the tags, the embeddings and the characters.
            
        Args:
            export_dir (str): Directory where the model will be saved.
        """
        def save_tags(file):
            """Saves the tags to disk.

            Args:
                file (str): Path to the file where the tags will be saved.
            """
            id2tag = {id: tag for (tag, id) in self.encoder.tag2id.items()}

            with open(file, 'w') as f:
                for i in range(len(id2tag)):
                    tag = id2tag[i]
                    f.write(tag)
                    f.write('\n')

        def save_embeddings(src, dst):
            """Saves the embeddings to disk.

            Args:
                src (str): Path to the embeddings file.
                dst (str): Path to the file where the embeddings will be saved.
            """
            from shutil import copyfile
            copyfile(src, dst)
            with open(dst + '.meta', 'w') as f:
                embeddings = self.encoder.embeddings
                dim = len(embeddings[0]) if embeddings else 0
                f.write(str(dim))

        def save_chars(file):
            """Saves the characters to disk.

            Args:
                file (str): Path to the file where the characters will be saved.
            """
            id2char = {id: char for (char, id) in self.encoder.char2id.items()}
            with open(file, 'w') as f:
                for i in range(1, len(id2char) + 1):
                    f.write(id2char[i])

        save_models(export_dir)
        save_tags(os.path.join(export_dir, 'tags.csv'))

        if self.embeddings_file:
            save_embeddings(self.embeddings_file, os.path.join(export_dir, 'embeddings'))

        save_chars(os.path.join(export_dir, 'chars.csv'))
