# Copyright 2022 Inductor, Inc.

"""Abstractions for model storage and access (particularly for inference)."""

import abc
import collections
import datetime
import shutil
import os
import re
import tempfile
import threading
from typing import Any, Optional, Tuple

import boto3
import joblib

from inductor import util
from inductor.data.table import table

# Storage metadata for a model, consisting
# of (framework name, framework version).
StorageMetadata = Tuple[str, str]

class ModelStore(abc.ABC):
    """A persistent collection of models."""

    def __init__(
        self,
        metadata_table: table.WithPrimaryKey,
        unique_id_gen: util.UniqueIdGen):
        """Initializes ModelStore superclass' fields.

        Args:
            metadata_table: Table to be used to persist this ModelStore's
                metadata.
            unique_id_gen: UniqueIdGen to be used to generate unique IDs for
                models added to this ModelStore.  Should produce IDs that are
                guaranteed to be globally unique within the currently running
                Inductor app.
        """
        self._metadata_table = metadata_table
        self._unique_id_gen = unique_id_gen

    @abc.abstractmethod
    def _store_model(self, model: Any, model_id: str) -> StorageMetadata:
        """Stores model having given model_id.

        Args:
            model: The model to be stored.
            model_id: ID of the model; should be globally unique within
                the currently running Inductor app.

        Returns:
            A tuple containing the name and version of the ML framework
            of the model being stored, which are required to load the
            model from storage.
        """

    def add_model(self, model_name: str, model: Any):
        """Adds given model to this ModelStore under given model_name.

        If a model is already present in this ModelStore under given model_name,
        then that model is replaced.

        Args:
            model_name: Name via which model will be accessible in this
                ModelStore (via __getitem__()).
            model: The model to be stored.
        """
        model_id = self._unique_id_gen.unique_id()
        storage_metadata = self._store_model(model, model_id)
        (framework, version) = storage_metadata
        self._metadata_table[model_name] = {
            "model_id": model_id,
            "storage_framework_name": framework,
            "storage_framework_version": version,
            "python_type": str(type(model)),
            "add_time": datetime.datetime.now()
        }

    def __setitem__(self, model_name: str, model: Any):
        """Alias for self.add_model(model_name, model)."""
        self.add_model(model_name, model)

    @abc.abstractmethod
    def __getitem__(self, model_name: str) -> Optional[Any]:
        """Returns an object representing the model having given model_name.

        The type of the returned object depends on the type of model stored
        under given model_name.  In general, the returned object permits calling
        methods and retrieving the values of fields on the underlying model
        object, though the returned object may not be the underlying model
        object itself.

        If no model having given model_name is present in this ModelStore,
        then this method returns None.
        """

    def __contains__(self, model_name: str) -> bool:
        """Returns True iff this ModelStore contains a model having given name.

        Args:
            model_name: Model name for which to determine presence.
        """
        return model_name in self._metadata_table


class _CachedModelStore(ModelStore):
    """ModelStore that uses an in-memory LRU cache for model access.

    Requires implementing `_get_uncached_model` rather than
    `__getitem__`.
    """

    def __init__(
        self,
        metadata_table: table.WithPrimaryKey,
        unique_id_gen: util.UniqueIdGen
    ):
        """See base class."""
        super().__init__(metadata_table, unique_id_gen)
        self._cache_limit = 3
        self._cache = collections.OrderedDict()
        self._name_id_dict = {}
        # Ensure cache access and changes are thread-safe.
        self._cache_lock = threading.Lock()

    def __getitem__(self, model_name: str) -> Optional[Any]:
        """See base class."""
        model_metadata = self._metadata_table.get(model_name)
        if not model_metadata:
            return None
        model_id = model_metadata["model_id"]
        with self._cache_lock:
            # If a model with this name but a different id is in the cache,
            # it should be invalidated.
            if model_name in self._name_id_dict:
                if self._name_id_dict[model_name] != model_id:
                    outdated_id = self._name_id_dict[model_name]
                    del self._cache[outdated_id]
            # If this model is stored in the cache, return it.
            if model_id in self._cache:
                self._cache.move_to_end(model_id, last=False)
                return self._cache[model_id]
        model = self._get_uncached_model(model_name)
        if model is not None:
            # Cache the model before returning it.
            with self._cache_lock:
                self._name_id_dict[model_name] = model_id
                while len(self._cache) >= self._cache_limit:
                    self._cache.popitem(last=True)
                self._cache[model_id] = model
                self._cache.move_to_end(model_id, last=False)
        return model

    @abc.abstractmethod
    def _get_uncached_model(self, model_name: str) -> Optional[Any]:
        """See base class definition of __getitem__.

        This function is called if the requested model is not found
        in the cache.
        """


class LocalModelStore(_CachedModelStore):
    """ModelStore backed by the local filesystem."""

    def __init__(
        self,
        base_path: str,
        metadata_table: table.WithPrimaryKey,
        unique_id_gen: util.UniqueIdGen
    ):
        """Constructs a new LocalModelStore.

        Args:
            base_path: Path to the directory in the local filesystem to be used
                for model storage.  The directory need not already exist.
            metadata_table: Table to be used to persist this ModelStore's
                metadata.
            unique_id_gen: UniqueIdGen to be used to generate unique IDs for
                models added to this ModelStore.  Should produce IDs that are
                guaranteed to be globally unique within the currently running
                Inductor app.
        """
        super().__init__(metadata_table, unique_id_gen)
        self._base_path = base_path

    def _store_model(self, model: Any, model_id: str) -> StorageMetadata:
        """See base class.

        For safety (i.e., to prevent escaping base_dir), this method does not
        allow model_id to contain "..".
        """
        if ".." in model_id:
            raise ValueError("model_id cannot contain \"..\".")
        model_dir =  os.path.join(self._base_path, model_id)
        os.makedirs(model_dir)
        model_module = model.__module__
        # Sklearn models are stored with JobLib.
        if model_module.startswith("sklearn."):
            try:
                import sklearn # pylint: disable=import-outside-toplevel
                model_path = os.path.join(model_dir, "model.joblib")
                joblib.dump(model, model_path)
                return "sklearn", sklearn.__version__
            except ImportError as exc:
                raise ModuleNotFoundError(
                    "Received scikit-learn model but the sklearn module "
                    "is not installed."
                ) from exc
        # PyTorch models are stored in two ways, natively and in TorchScript.
        elif model_module.startswith("torch."):
            try:
                import torch # pylint: disable=import-outside-toplevel
                # PyTorch models are saved in entirety and in TorchScript
                model_path = os.path.join(model_dir, "model.pt")
                torch.save(model, model_path)
                model_ts_path = os.path.join(model_dir, "model.ptc")
                model_scripted = torch.jit.script(model)
                model_scripted.save(model_ts_path)
                return "torch", torch.__version__
            except ImportError as exc:
                raise ModuleNotFoundError(
                    "Received PyTorch model but the torch module "
                    "is not installed."
                ) from exc
        # Keras models are stored natively.
        elif model_module.startswith("keras."):
            try:
                import tensorflow # pylint: disable=import-outside-toplevel
                model_path = os.path.join(model_dir, "model")
                model.save(model_path)
                return "keras", tensorflow.__version__
            except ImportError as exc:
                raise ModuleNotFoundError(
                    "Received Keras model but the tensorflow module "
                    "is not installed."
                ) from exc
        # If not explicitly supported, attempt using joblib.
        else:
            joblib.dump(model, os.path.join(model_dir, "model.joblib"))
            return "joblib", ""

    def _get_uncached_model(self, model_name: str) -> Optional[Any]:
        """See base class."""
        model_metadata = self._metadata_table.get(model_name)
        if not model_metadata:
            return None
        model_framework_name = model_metadata["storage_framework_name"]
        model_id = model_metadata["model_id"]
        # Sklearn models are retrieved with JobLib.
        if model_framework_name == "sklearn":
            model_path = os.path.join(self._base_path, model_id, "model.joblib")
            return joblib.load(model_path)
        # PyTorch models are retrieved with native retrieval.
        elif model_framework_name == "torch":
            try:
                import torch # pylint: disable=import-outside-toplevel
                model_path =  os.path.join(
                    self._base_path,
                    model_id,
                    "model.ptc"
                )
                model = torch.jit.load(model_path)
                model.eval()
                return model
            except ImportError as exc:
                raise ModuleNotFoundError(
                    "Attempted to access PyTorch model but the torch module "
                    "is not installed."
                ) from exc
        # Keras models are retrieved with native retrieval.
        elif model_framework_name == "keras":
            try:
                import tensorflow # pylint: disable=import-outside-toplevel
                model_path = os.path.join(self._base_path, model_id, "model")
                return tensorflow.keras.models.load_model(model_path)
            except ImportError as exc:
                raise ModuleNotFoundError(
                    "Attempted to access Keras model but the tensorflow module "
                    "is not installed."
                ) from exc
        # All unknown frameworks are retrieved with JobLib.
        else:
            model_path = os.path.join(self._base_path, model_id, "model.joblib")
            return joblib.load(model_path)


class S3ModelStore(_CachedModelStore):
    """ModelStore backed by AWS S3 bucket storage."""

    def __init__(
        self,
        s3_url: str,
        metadata_table: table.WithPrimaryKey,
        unique_id_gen: util.UniqueIdGen,
    ):
        """Constructs a new S3ModelStore.

        Args:
            s3_url: The S3 URL to be used for model storage, in the format
                s3://bucket/prefix/ where prefix is optional.
            metadata_table: Table to be used to persist this ModelStore's
                metadata.
            unique_id_gen: UniqueIdGen to be used to generate unique IDs for
                models added to this ModelStore.  Should produce IDs that are
                guaranteed to be globally unique within the currently running
                Inductor app.
        """
        super().__init__(metadata_table, unique_id_gen)
        (bucket_name, model_prefix) = self._get_bucket_prefix_from_url(s3_url)
        self._bucket_name = bucket_name
        self._model_prefix = model_prefix
        self._client = boto3.client("s3")

    def _get_bucket_prefix_from_url(
        self,
        s3_url: str
    ) -> Tuple[str, Optional[str]]:
        """Destructures an S3 URL into a bucket and optional prefix.

        Args:
            s3_url: An S3 URL in the format s3://bucket/prefix/
                where prefix is optional.

        Returns:
            A tuple containing the S3 bucket name and, if it exists, the
            optional prefix.
        """
        reg_exp = "\\As3://([^/]+)(/?)(.*)\\Z"
        match = re.search(reg_exp, s3_url)
        if match is None:
            raise RuntimeError("Unable to parse provided S3 URL.")
        (bucket, _, prefix) = match.groups()
        if prefix == "":
            return (bucket, None)
        else:
            return (bucket, prefix)

    def _store_model(self, model: Any, model_id: str) -> StorageMetadata:
        """See base class.

        For consistency with LocalModelStore, this method does not
        allow model_id to contain "..".
        """
        if ".." in model_id:
            raise ValueError("model_id cannot contain \"..\".")
        model_module = model.__module__
        framework = None
        version = None
        with tempfile.TemporaryDirectory() as tempdir:
            model_dir = os.path.join(tempdir, model_id)
            os.makedirs(model_dir)
            # Sklearn models are stored with JobLib.
            if model_module.startswith("sklearn."):
                try:
                    import sklearn # pylint: disable=import-outside-toplevel
                    model_path = os.path.join(model_dir, "model.joblib")
                    joblib.dump(model, model_path)
                    framework = "sklearn"
                    version = sklearn.__version__
                except ImportError as exc:
                    raise ModuleNotFoundError(
                        "Received scikit-learn model but the sklearn module "
                        "is not installed."
                    ) from exc
            # PyTorch models are stored natively and in TorchScript.
            elif model_module.startswith("torch."):
                try:
                    import torch # pylint: disable=import-outside-toplevel
                    # PyTorch models are saved in entirety and in TorchScript
                    model_path = os.path.join(model_dir, "model.pt")
                    torch.save(model, model_path)
                    model_ts_path = os.path.join(model_dir, "model.ptc")
                    model_scripted = torch.jit.script(model)
                    model_scripted.save(model_ts_path)
                    framework = "torch"
                    version = torch.__version__
                except ImportError as exc:
                    raise ModuleNotFoundError(
                        "Received PyTorch model but the torch module "
                        "is not installed."
                    ) from exc
            # Keras models are stored natively.
            elif model_module.startswith("keras."):
                try:
                    import tensorflow # pylint: disable=import-outside-toplevel
                    model_path = os.path.join(model_dir, "model")
                    model.save(model_path)
                    framework = "keras"
                    version = tensorflow.__version__
                except ImportError as exc:
                    raise ModuleNotFoundError(
                        "Received Keras model but the tensorflow module "
                        "is not installed."
                    ) from exc
            # If not explicitly supported, attempt using joblib.
            else:
                joblib.dump(model, os.path.join(model_dir, "model.joblib"))
                framework = "joblib"
                version = ""
            # Framework and version should be set by now.
            assert framework is not None
            assert version is not None
            # Zip the temporary directory.
            local_model_zip_path = os.path.join(tempdir, model_id)
            local_model_zip_name = f"{local_model_zip_path}.zip"
            model_zip_name = f"{model_id}.zip"
            if self._model_prefix is not None:
                model_zip_name = os.path.join(
                    self._model_prefix,
                    model_zip_name
                )
            shutil.make_archive(local_model_zip_path, "zip", model_dir)
            # Upload the zipped model directory.
            with open(local_model_zip_name, "rb") as model_binary:
                self._client.upload_fileobj(
                    model_binary,
                    self._bucket_name,
                    model_zip_name
                )
            # Return the storage metadata.
            return framework, version

    def _get_uncached_model(self, model_name: str) -> Optional[Any]:
        """See base class."""
        model_metadata = self._metadata_table.get(model_name)
        if not model_metadata:
            return None
        model_framework_name = model_metadata["storage_framework_name"]
        model_id = model_metadata["model_id"]
        with tempfile.TemporaryDirectory() as tempdir:
            local_model_path = os.path.join(tempdir, model_id)
            os.makedirs(local_model_path)
            # Download the zipped model.
            local_model_zip_name = f"{local_model_path}.zip"
            model_zip_name = f"{model_id}.zip"
            if self._model_prefix is not None:
                model_zip_name = os.path.join(
                    self._model_prefix,
                    model_zip_name
                )
            with open(local_model_zip_name, "wb") as model_binary:
                self._client.download_fileobj(
                    self._bucket_name,
                    model_zip_name,
                    model_binary
                )
            shutil.unpack_archive(local_model_zip_name, local_model_path)
            # Sklearn models are retrieved with JobLib.
            if model_framework_name == "sklearn":
                model_path = os.path.join(local_model_path, "model.joblib")
                return joblib.load(model_path)
            # PyTorch models are retrieved with native retrieval.
            elif model_framework_name == "torch":
                try:
                    import torch # pylint: disable=import-outside-toplevel
                    model_path = os.path.join(local_model_path, "model.ptc")
                    model = torch.jit.load(model_path)
                    model.eval()
                    return model
                except ImportError as exc:
                    raise ModuleNotFoundError(
                        "Attempted to access PyTorch model but the torch "
                        "module is not installed."
                    ) from exc
            # Keras models are retrieved with native retrieval.
            elif model_framework_name == "keras":
                try:
                    import tensorflow # pylint: disable=import-outside-toplevel
                    model_path = os.path.join(local_model_path, "model")
                    return tensorflow.keras.models.load_model(model_path)
                except ImportError as exc:
                    raise ModuleNotFoundError(
                        "Attempted to access Keras model but the tensorflow "
                        "module is not installed."
                    ) from exc
            # All unknown frameworks are retrieved with JobLib.
            else:
                model_path = os.path.join(local_model_path, "model.joblib")
                return joblib.load(model_path)
