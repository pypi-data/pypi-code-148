from __future__ import annotations

import functools
import logging
import typing as t
from dataclasses import dataclass, fields
from pathlib import Path

import numpy as np
import pandas as pd
import pyqtgraph as pg
import torch
from pyqtgraph import QtCore, QtWidgets
from pyqtgraph.parametertree import InteractiveFunction
from pyqtgraph.parametertree.parameterTypes import ActionGroupParameterItem
from qtextras import (
    AppLogger,
    ChainedActionGroupParameter,
    ParameterEditor,
    ParameterlessInteractor,
    RunOptions,
    bindInteractorOptions as bind,
    fns,
    widgets,
)
from sklearn import manifold
from sklearn.cluster import FeatureAgglomeration
from sklearn.decomposition import PCA
from sklearn.random_projection import GaussianRandomProjection

from gemovi.common.constants import get_device
from gemovi.common.dataset import default_image_transforms
from gemovi.common.utils import get_config, load_trainer_state_dict, to_pil_image
from gemovi.viz.plugins import (
    PerturbationPlugin,
    PopoutPlugin,
    ROIDecoderPlugin,
    SampleMetadataPlugin,
    ScatterplotPlugin,
    TabPlugin,
)
from gemovi.viz.transformer import NoneTransformer, NpOrNoneTransformer
from gemovi.viz.tutorial import GettingStartedWizard, LatentTransformWizard

device = get_device(1)
transformer_classes = {
    "PCA": PCA,
    "Gaussian Projecton": GaussianRandomProjection,
    "Feature Agglomeration": lambda *args, **kwargs: FeatureAgglomeration(),
    "TSNE": manifold.TSNE,
    "LLE": manifold.LocallyLinearEmbedding,
    "Isomap": manifold.Isomap,
    "MDS": manifold.MDS,
    "Spectral Embedding": manifold.SpectralEmbedding,
    "None": NoneTransformer,
}


class ModelTab(QtWidgets.QWidget):
    latent_dim_key: str = None
    sig_model_changed = QtCore.Signal()

    def __init__(self, model, parameter_info=None):
        QtWidgets.QWidget.__init__(self)
        self.editor = ParameterEditor(directory=".")
        self.model = model
        self.parameter_info = parameter_info
        self.plugins: dict[str, TabPlugin] = {}

        contents = self.setup_gui()
        if contents is not None:
            layout = QtWidgets.QVBoxLayout()
            self.setLayout(layout)
            layout.addWidget(contents)
        self.post_init(self.editor)

    def setup_gui(self) -> QtWidgets.QWidget | None:
        raise NotImplementedError

    def post_init(self, pe: ParameterEditor):
        self._init_plugins()

    def _init_plugins(self):
        old_default = self.editor.defaultParent
        for plugin_cls in self.get_plugin_classes():
            plugin = plugin_cls(self)
            self.editor.defaultParent = plugin.name
            plugin.register_functions(self.editor)
            self.plugins[plugin.name] = plugin
        self.editor.defaultParent = old_default

    def get_plugin_classes(self):
        return []

    def forward(self, input):
        raise NotImplementedError

    def get_image_size(self):
        if (
            (self.parameter_info is not None)
            and (data_params := self.parameter_info.get("data_params"))
            and (image_size := data_params.get("patch_size"))
        ):
            return image_size
        raise NotImplementedError

    def get_num_latent_dims(self):
        if (
            self.latent_dim_key
            and self.parameter_info
            and (model_params := self.parameter_info.get("model_params"))
        ):
            model_name = self.model.__class__.__name__
            return model_params[model_name][self.latent_dim_key]
        raise NotImplementedError

    def image_as_normed_tensor(self, image, add_batch_dim=True):
        tforms = default_image_transforms(self.get_image_size())
        if isinstance(image, torch.Tensor):
            norm = tforms.transforms[-1]
            return norm(image)
        # else
        image = to_pil_image(image)
        image = tforms(image).to(device)
        if add_batch_dim:
            image = image.unsqueeze(0)
        return image


class ModelWindow(QtWidgets.QMainWindow):
    sig_model_changed = QtCore.Signal()

    tab_types: list[type[ModelTab]] = []
    model_cls = None

    def __init__(self, parameter_info=None):
        super().__init__()
        if isinstance(parameter_info, str):
            parameter_info = get_config(parameter_info)
        else:
            parameter_info = parameter_info or {}
        self.parameter_info = parameter_info
        self.model = self.make_model(parameter_info)
        self.model.to(device).eval()
        self.settings_editor = ParameterEditor(directory=".")

        self.setup_gui()

        pe = self.settings_editor
        self.update_weights_proc = pe.registerFunction(
            self.update_weights, runOptions=RunOptions.ON_ACTION
        )
        pe.registerFunction(self.dev_console, runActionTemplate=dict(shortcut="Ctrl+`"))

        logger = AppLogger.getAppLogger(__file__)
        logger.registerExceptions(self)
        logger.setLevel(logging.INFO + 1)

    @bind(weights=dict(type="file"))
    def update_weights(self, weights="", model=None):
        if not Path(weights or "").is_file():
            return
        data = torch.load(weights, map_location=device)
        if model is None:
            model = self.model
        result = load_trainer_state_dict(model, data, strict=False)

        if not any(result):
            msg = str(result)
        else:
            missing, unexpected = [self._format_result_message(keys) for keys in result]
            msg = f"Missing keys: {missing}"
            msg += ", Unexpected keys: " + f"{unexpected}"
        self.statusBar().showMessage(msg)
        self.sig_model_changed.emit()

    @staticmethod
    def _format_result_message(key_list):
        if not key_list:
            return "<None>"
        missing_networks = set(key.split(".")[0] + ".*" for key in key_list)
        return ", ".join(missing_networks)

    # Variables are widget logistics, not used elsewhere
    # noinspection PyAttributeOutsideInit
    def setup_gui(self):
        self.tab_group = QtWidgets.QTabWidget()
        for tab_cls in self.tab_types:
            self.insert_tab(tab_cls)

        mb = self.menuBar()
        # Default size is a bit too small
        self.settings_editor.resize(400, 300)
        self.settings_editor.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        mb.addAction("&Settings", self.raise_settings_window)
        self.tutorial_menu = mb.addMenu("Tutorials")
        self.tutorial_menu.addAction(
            "Getting Started", self.show_getting_started_tutorial
        )
        self.tutorial_menu.addAction(
            "Latent Space Transforms", self.show_latent_transforms_tutorial
        )

        widgets.EasyWidget.buildMainWindow([self.tab_group], window=self)

    def raise_settings_window(self):
        self.settings_editor.show()
        self.settings_editor.raise_()

    def show_getting_started_tutorial(self):
        wizard = GettingStartedWizard(self)
        wizard.show()

    def show_latent_transforms_tutorial(self):
        wizard = LatentTransformWizard(self)
        wizard.show()

    def insert_tab(self, tab_type: type[ModelTab], tab_name: str = None):
        tab_inst = tab_type(self.model, self.parameter_info)
        tab_name_base = tab_type.__name__.replace("Tab", "")
        if tab_name is None:
            tab_name = f"&{tab_name_base} - {self.model_cls.__name__}"
        self.tab_group.addTab(tab_inst, tab_name)
        self.sig_model_changed.connect(tab_inst.sig_model_changed.emit)

    def dev_console(self):
        widgets.safeSpawnDevConsole(window=self)

    def get_tab(self, tab_number: int = None):
        if tab_number is None:
            tab_number = self.tab_group.currentIndex()
        return self.tab_group.widget(tab_number)

    @classmethod
    def make_model(cls, param_info=None):
        if cls.model_cls is None:
            raise ValueError("Model class not set")

        if param_info is None:
            param_info = {}
        elif isinstance(param_info, str):
            param_info = get_config(param_info)
            # Came from config file, parse portion of file that has params
            # for the model class
        model_cls_name = cls.model_cls.__name__
        if param_info.get("model_params"):
            param_info = param_info["model_params"][model_cls_name]
        return cls.model_cls(**param_info)


@dataclass
class SampleInfo:
    samples: torch.Tensor = None
    numeric_labels: np.ndarray | None = None
    number_label_map: pd.Series = None
    image_files: t.Sequence[str] | None = None

    def unset_labels(self):
        self.numeric_labels = None
        self.number_label_map = pd.Series({1.0: None})
        self.image_files = None

    def __post_init__(self):
        self.unset_labels()

    def state_dict(self):
        return {field.name: getattr(self, field.name) for field in fields(self)}

    def load_state_dict(self, state_dict):
        found = set()
        for k, v in state_dict.items():
            if hasattr(self, k):
                setattr(self, k, v)
                found.add(k)
        msg = ""
        self_keys = set(self.state_dict())
        missing_keys = self_keys - found
        extra_keys = found - self_keys
        if not missing_keys and not extra_keys:
            msg = "<All sample keys loaded successfully>"
        if missing_keys:
            msg += f"<Missing sample keys: {missing_keys}>"
        if extra_keys:
            msg += f"<Extra sample keys: {extra_keys}>"
        return msg


class ClickableViewBox(pg.ViewBox):
    """
    Plot item that fires "sigClicked" to conveniently signal when a void point
    selection is made
    """

    sigClicked = QtCore.Signal(object)

    def mouseClickEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.sigClicked.emit(event)
        super().mouseClickEvent(event)


class GenerativeTab(ModelTab):
    sig_samples_changed = QtCore.Signal()
    sig_transformer_changed = QtCore.Signal()
    sig_samples_selected = QtCore.Signal(list)

    listener_interactor = ParameterlessInteractor()

    def __init__(self, model, parameter_info=None):
        self.xdim, self.ydim = 0, 1
        self.selected_sample_indexes = []
        self.dim_transformer = NpOrNoneTransformer()
        self.samples_info = SampleInfo()
        self._transformed_samples_cache = None
        # Gets set to id(self.samples_info.samples) when cache is populated
        self._cache_samples_id = -1

        self.plot_widget = pg.PlotWidget(viewBox=ClickableViewBox())
        self.plot_widget.invertY()
        self.plot_widget.plotItem.getViewBox().sigClicked.connect(
            self.on_viewbox_clicked
        )
        self.plot_widget.setAspectLocked(True)

        self.menu = QtWidgets.QMenu("Gemovi Options")

        def toggle_aspect():
            vb = self.plot_widget.getViewBox()
            vb.setAspectLocked(not vb.state["aspectLocked"])

        self.menu.addAction("Toggle Aspect Locked", toggle_aspect)
        self._setup_selection_listener()

        super().__init__(model, parameter_info)
        # Treat sample changes as a deselection
        self.sig_samples_selected.connect(self.on_samples_selected)
        self.sig_samples_changed.connect(self.on_viewbox_clicked)

    def post_init(self, pe):
        with fns.overrideAttr(pe, "defaultParent", "Latent Cross Section"):
            self.update_dims_proc = pe.registerFunction(
                self.update_plane_dimensions, runOptions=RunOptions.ON_ACTION
            )
            ndims = self.get_num_latent_dims()
            pe.registerFunction(
                self.set_transformer, n_components=dict(value=ndims, limits=[1, ndims])
            )
        super().post_init(pe)

        pe.treeButtonsWidget.show()
        for grp in fns.flattenedParameters(pe.rootParameter):
            grp.setOpts(expanded=False)

        initial_listeners = [
            ch.name() for ch in self.selection_listener_chain if ch.opts["enabled"]
        ]
        self.set_enabled_listeners_proc = self.editor.registerFunction(
            self.set_enabled_listeners,
            listeners=dict(
                limits=list(self.selection_listener_chain.names),
                value=initial_listeners,
                default=initial_listeners,
            ),
            runOptions=[RunOptions.ON_CHANGING, RunOptions.ON_CHANGED],
        )

    def on_samples_selected(self, sample_indexes: list[int]):
        if not sample_indexes:
            # Special case: on deselection, propagate to every listener regardless
            # of whether they are activated
            for listener in self.selection_listener_chain:
                listener.opts["function"](sample_indexes=sample_indexes)
        else:
            self.selection_listener_chain.activate(sample_indexes=sample_indexes)

    def setup_gui(self):
        self.plot_widget.getViewBox().menu.addMenu(self.menu)

        contents = widgets.EasyWidget.buildWidget(
            self._get_easy_children(), layout="H", useSplitter=True
        )
        return contents

    def _setup_selection_listener(self):
        self.selection_listener_chain = ChainedActionGroupParameter(
            name="Selection Listeners"
        )
        # Don't allow outer-level parameter to be disabled. Do this by reassigning
        # its item class before it's added to any trees
        self.selection_listener_chain.itemClass = ActionGroupParameterItem

    @bind(listeners=dict(type="checklist", exclusive=True))
    def set_enabled_listeners(self, listeners: list[str] | str):
        """
        Choose what happens when a sample is selected

        Parameters
        ----------
        listeners
            Which listeners to enable. Each controls different activities which
            are explained in more detail from other tree options with similar names
        """
        if isinstance(listeners, str):
            listeners = [listeners]
        for child in self.selection_listener_chain.children():
            child.setOpts(
                enabled=child.name() in listeners or child.title() in listeners
            )

    def register_selection_listener(
        self, listener: InteractiveFunction | t.Callable, enabled=True
    ):
        registered = self.selection_listener_chain.addStage(
            listener, interactor=self.listener_interactor
        )
        if not enabled:
            registered.setOpts(enabled=False)
        registered.sigOptionsChanged.connect(self.on_selection_listener_opts_changed)
        return registered

    def on_selection_listener_opts_changed(self, parameter, opts):
        if "enabled" in opts and not opts["enabled"]:
            # Spoof an empty selection to ensure gui remnants are removed
            parameter.opts["function"](sample_indexes=[])

    def _get_easy_children(self):
        return [self.plot_widget, self.editor]

    @property
    def samples(self):
        return self.samples_info.samples

    @property
    def numeric_labels(self):
        labels = self.samples_info.numeric_labels
        if labels is None:
            labels = np.ones(len(self.samples), dtype="float32")
        return labels

    def get_plugin_classes(self):
        return [
            SampleMetadataPlugin,
            ROIDecoderPlugin,
            ScatterplotPlugin,
            PerturbationPlugin,
            PopoutPlugin,
        ]

    def get_transformed_samples(self, sample_idxs: int | t.Sequence[int] = None):
        if self._transformed_samples_cache is None or self._cache_samples_id != id(
            self.samples
        ):
            if not self.dim_transformer.implements("transform"):
                AppLogger.getAppLogger(__file__).warning(
                    f"`{self.dim_transformer.transformer}` cannot re-transform new "
                    f"data. You must call `set_transformer` again with the current data "
                    f" to use it. For now, no transform is applied."
                )
            # Calling "transform" without the implementation will just return the
            # original data
            self._transformed_samples_cache = self.dim_transformer.transform(
                self.samples
            )
            self._cache_samples_id = id(self.samples)
        if sample_idxs is None:
            sample_idxs = slice(None)
        xformed = self._transformed_samples_cache[sample_idxs]
        return xformed

    def get_index_as_image(self, index=None, pil_or_tensor="pil"):
        if index is None and self.selected_sample_indexes:
            index = self.selected_sample_indexes[0]
        if index is None:
            return None
        info = self.samples_info
        if info.image_files:
            data = info.image_files[index]
        else:
            data = self.forward(self.samples[index].unsqueeze(0))[0]

        image = to_pil_image(data)
        if pil_or_tensor == "pil":
            return image
        return self.image_as_normed_tensor(image)

    def on_viewbox_clicked(self):
        self.update_selected_samples([])

    def update_selected_samples(self, sample_indexes: list):
        """
        Update the selected sample in the preview widget.
        """
        self.selected_sample_indexes = sample_indexes
        self.sig_samples_selected.emit(sample_indexes)
        window = self.window()
        if hasattr(window, "statusBar") and sample_indexes:
            msg = f"Selected sample {sample_indexes[0]}"
            window.statusBar().showMessage(msg)

    def update_plane_dimensions(self, xdim=0, ydim=1):
        """
        Update the dimensions of the plane to display in the preview widget. If no
        transformer has been set, this will be the raw index into the latent space.
        Otherwise, these are slices of the transformed latent space.

        Parameters
        ----------
        xdim, ydim : int
            The dimensions to display in the preview widget
        """
        if self.samples is None or not len(self.samples):
            return
        dims = np.array([xdim, ydim])
        dummy_data = self.get_transformed_samples(0)
        dims = np.clip(dims, 0, len(dummy_data) - 1)
        self.xdim, self.ydim = dims
        self.sig_transformer_changed.emit()
        self.update_selected_samples(self.selected_sample_indexes)

    @bind(
        transformer=dict(limits=list(transformer_classes), type="list"),
        n_components=dict(type="int", limits=[1, 100]),
        transformer_kwargs=dict(type="text", value=""),
    )
    def set_transformer(
        self,
        transformer="PCA",
        n_components=None,
        max_n_samples=10_000,
        transformer_kwargs: dict | str = None,
    ):
        """
        Set a transformer to compress the latent space into a 2D plane for display.

        Note! Transformers should generally only be used when data has been loaded
        from a legitimate dataset, not when it has been generated by i.e. sampling
        randomly from a latent space.

        Parameters
        ----------
        transformer
            Type of transformer to use. Must be a class in the `transformer_classes`
        n_components
            Number of components to use in the transformer
        max_n_samples
            Maximum number of samples to use in the transformer. If the number of
            samples is greater than this, a random subset will be used.
        transformer_kwargs
            Additional keyword arguments to pass to the transformer. Must be a
            dictionary or a string that specifies dict keys, i.e. "key1=value1,"
        """
        samples = self.samples
        labels = self.numeric_labels

        if n_components is None:
            n_components = samples.shape[1]
        if max_n_samples <= 0:
            max_n_samples = len(samples)
        transformer_kwargs = transformer_kwargs or {}
        if isinstance(transformer_kwargs, str):
            transformer_kwargs = eval(f"dict({transformer_kwargs})")

        transformer = transformer_classes[transformer](
            n_components=min(n_components, samples.shape[0], samples.shape[1]),
            **transformer_kwargs,
        )
        self.dim_transformer.set_transformer(transformer)
        truncated_data = max_n_samples < len(samples)
        self._handle_transformer_warnings_errors(truncated_data)

        if len(samples) > max_n_samples:
            rows = np.random.permutation(samples.shape[0])[:max_n_samples]
            samples = samples[rows]
            labels = labels[rows]

        fit_transformed = self.dim_transformer.fit_transform(samples, y=labels)
        if truncated_data:
            self._transformed_samples_cache = self.dim_transformer.transform(
                self.samples
            )
        else:
            self._transformed_samples_cache = fit_transformed
        self._cache_samples_id = id(self.samples)
        # Make sure selection listeners don't fire if inverse transforming is not
        # allowed, otherwise errors will abound
        tformer_has_inverse = self.dim_transformer.implements("inverse_transform")
        self.selection_listener_chain.setOpts(enabled=tformer_has_inverse)
        # Re-trigger old enabled listeners, otherwise everything gets enabled when
        # enabling the parent
        self.set_enabled_listeners_proc()
        self.update_dims_proc(xdim=0, ydim=1)

    def _handle_transformer_warnings_errors(self, truncated_training_data=False):
        implements = self.dim_transformer.implements

        if not implements("fit_transform"):
            raise ValueError("Data transformer must implement `fit_transform`")
        if truncated_training_data and not implements("transform"):
            raise ValueError(
                f"{self.dim_transformer.transformer} does not provide a `transform` "
                f"method, so it cannot be used to transform new data. Please use a "
                f"transformer that implements `transform` or pass the full samples "
                f"dataset (max_n_samples >= {len(self.samples)}) while fitting "
                f"`{self.dim_transformer.transformer}`"
            )
        if not implements("inverse_transform"):
            AppLogger.getAppLogger(__file__).warning(
                f"`{self.dim_transformer.transformer}` does not provide an inverse "
                f"transform. Selection listeners will not be active, so no action will "
                f"be taken when selecting samples in the view area."
            )

    @functools.lru_cache(maxsize=1)
    def get_image_size(self):
        noise = torch.zeros(1, self.get_num_latent_dims(), device=device)
        return self.forward(noise).shape[-2:]

    def forward(self, input: torch.Tensor):
        return self.model.generator(input.view(*input.shape, 1, 1))

    def get_random_latent_samples(self, n_samples=None):
        if n_samples is None:
            if self.samples is None:
                raise ValueError(
                    "No samples to sample from and no `approximate_n_samples` given"
                )
            else:
                n_samples = self.samples.shape[0]
        return torch.randn(n_samples, self.get_num_latent_dims(), device=device)
