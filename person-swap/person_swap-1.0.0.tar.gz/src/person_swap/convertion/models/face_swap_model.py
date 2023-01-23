from custom_utils.conversion_exception import ConversionError
from tensorflow.keras.layers import Dense, Flatten, Reshape, Input  # noqa pylint:disable=import-error,no-name-in-module
from tensorflow.keras.models import load_model, Model


class KerasCnnModel:

    def build(self) -> Model:
        """ Loads the model from disk
        If the predict function is to be called and the model cannot be found in the model folder
        then an error is logged and the process exits.
        When loading the model, the plugin model folder is scanned for custom layers which are
        added to Keras' custom objects.
        Returns
        -------
        :class:`keras.models.Model`
            The saved model loaded from disk
        """

        model_file_path = self._args.model_file_path
        self.logger.debug("Loading model: %s", model_file_path)
        try:
            model = load_model(model_file_path, compile=False)
        except RuntimeError as err:
            if "unable to get link info" in str(err).lower():
                msg = (f"Unable to load the model from '{model_file_path}'. This may be a "
                       "temporary error but most likely means that your model has corrupted.\n"
                       "You can try to load the model again but if the problem persists you "
                       "should use the Restore Tool to restore your model from backup.\n"
                       f"Original error: {str(err)}")
                raise ConversionError(msg) from err
            raise err
        except KeyError as err:
            if "unable to open object" in str(err).lower():
                msg = (f"Unable to load the model from '{model_file_path}'. This may be a "
                       "temporary error but most likely means that your model has corrupted.\n"
                       "You can try to load the model again but if the problem persists you "
                       "should use the Restore Tool to restore your model from backup.\n"
                       f"Original error: {str(err)}")
                raise ConversionError(msg) from err
            raise err

        self.logger.info("Loaded model from disk: '%s'", model_file_path)
        return model
