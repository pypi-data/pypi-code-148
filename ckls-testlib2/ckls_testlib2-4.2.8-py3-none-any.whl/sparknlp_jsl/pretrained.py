import sys
import threading

import sparknlp_jsl.internal as _internal
import sparknlp.internal as _internal_opensource
import threading
import time
from py4j.protocol import Py4JJavaError

def printProgress(stop):
    """
    Prints a progress bar to the console every 2.5 seconds.

    Args:
        stop (function): A function that returns True when the progress bar should stop.
    """
    states = [' | ', ' / ', ' — ', ' \\ ']
    nextc = 0
    while True:
        sys.stdout.write('\r[{}]'.format(states[nextc]))
        sys.stdout.flush()
        time.sleep(2.5)
        nextc = nextc + 1 if nextc < 3 else 0
        if stop():
            sys.stdout.write('\r[{}]'.format('OK!'))
            sys.stdout.flush()
            break

    sys.stdout.write('\n')
    return


class InternalResourceDownloader(object):
    """Downlod internal resources from S3
    """

    @staticmethod
    def downloadModel(reader, name, language, remote_loc=None, j_dwn='InternalsPythonResourceDownloader'):
        """Download a model from S3

        Args:
            reader (class): The reader class to use to load the model.
            name (str): The name of the model to download.
            language (str): The language of the model to download.
            remote_loc (str, optional): The remote location of the model. Defaults to None.
            j_dwn (str, optional): The Java downloader class to use. Defaults to 'InternalsPythonResourceDownloader'.

        Returns:
            class: The reader class with the model loaded.
        """
        print(name + " download started this may take some time.")
        stop_threads = False
        t1 = threading.Thread(target=printProgress, args=(lambda: stop_threads,))
        t1.start()
        try:
                j_obj = _internal_opensource._DownloadModel(reader.name, name, language, remote_loc, j_dwn).apply()
        except Py4JJavaError as e:
                sys.stdout.write("\n" + str(e))
                raise e
        finally:
                stop_threads = True
                t1.join()

        return reader(classname=None, java_model=j_obj)

    @staticmethod
    def showPrivateModels(annotator=None, lang=None, version=None):
        """Show private models available for download

        Args:
            annotator (str, optional): The annotator to filter by. Defaults to None.
            lang (str, optional): The language to filter by. Defaults to None.
            version (str, optional): The version to filter by. Defaults to None.
        """
        print(_internal._ShowPrivateModels(annotator, lang, version).apply())

    @staticmethod
    def showPrivatePipelines(lang=None, version=None):
        """Show private pipelines available for download

        Args:
            lang (str, optional): The language to filter by. Defaults to None.
            version (str, optional): The version to filter by. Defaults to None.
        """
        print(_internal._ShowPrivatePipelines(lang, version).apply())

    @staticmethod
    def showUnCategorizedResources():
        """Show uncategorized resources available for download.
        """
        print(_internal._ShowUnCategorizedResources().apply())

    @staticmethod
    def showAvailableAnnotators():
        """Show available annotators."""
        print(_internal._ShowAvailableAnnotators().apply())

    @staticmethod
    def returnPrivateModels(annotator=None, lang=None, version=None):
        """Return private models available for download.

        Args:
            annotator (str, optional): The annotator to filter by. Defaults to None.
            lang (str, optional): The language to filter by. Defaults to None.
            version (str, optional): The version to filter by. Defaults to None.

        Returns:
            list: A list of private models available for download.
        """
        elements =_internal._ReturnPrivateModels(annotator, lang, version).apply()
        return list([list(el) for el in elements])

    @staticmethod
    def returnPrivatePipelines(lang=None, version=None):
        """Return private pipelines available for download.

        Args:
            lang (str, optional): The language to filter by. Defaults to None.
            version (str, optional): The version to filter by. Defaults to None.

        Returns:
            list: A list of private pipelines available for download.
        """
        print(_internal._ReturnPrivatePipelines(lang, version).apply())
