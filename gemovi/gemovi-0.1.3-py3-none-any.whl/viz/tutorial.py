from __future__ import annotations

import copy
import typing as t
from pathlib import Path

import pandas as pd
from PIL import Image
from pyqtgraph.parametertree import RunOptions
from pyqtgraph.Qt import QtCore, QtWidgets
from qtextras import ParameterEditor, bindInteractorOptions as bind, fns
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

from gemovi.vae.models import DFCVAE
from gemovi.viz.plugins import FileSampleMetadataPlugin

if t.TYPE_CHECKING:
    from gemovi.viz import ModelTab, ModelWindow
    from gemovi.viz.base import GenerativeTab

T = t.TypeVar("T")


class WelcomePage(QtWidgets.QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Welcome to the tutorial")
        self.setSubTitle(
            "This wizard will guide you through the basic features of the visualization "
            "package. "
        )


class TutorialPage(QtWidgets.QWizardPage):
    folder: str | Path = None
    sig_folder_changed = QtCore.Signal(object)

    def __init__(
        self,
        long_message: str = None,
        title: str = None,
        register_set_folder: bool = True,
    ):
        super().__init__()
        if title:
            self.setTitle(title)
        label = None
        if long_message:
            label = QtWidgets.QLabel(long_message)
            label.setWordWrap(True)
        self.label = label
        self.editor = ParameterEditor()
        if register_set_folder:
            self.set_folder_proc = self.editor.registerFunction(
                self.set_folder,
                runOptions=RunOptions.ON_CHANGED,
            )
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        if label:
            layout.addWidget(label)
        layout.addWidget(self.editor.tree)
        self.setLayout(layout)

    @bind(folder=dict(type="file", fileMode="Directory"))
    def set_folder(self, folder: str | Path = "./gemovi-workspace"):
        folder = Path(folder).resolve()
        if folder == self.folder:
            return
        self.folder = folder
        self.sig_folder_changed.emit(folder)

    def on_folder_changed(self, folder: str | Path):
        if hasattr(self, "set_folder_proc"):
            self.set_folder_proc(folder=folder)


class LoadDataPage(TutorialPage):
    def __init__(self, gemovi_window: ModelWindow = None):
        msg = (
            "<qt>Skip this page if you already have weights from a trained model. "
            "Otherwise, this page will create data suitable for training a model from "
            "scikit-learn's digits dataset. Note that in practice, a much larger "
            "dataset (e.g., Yann Lecun's 'digit' dataset) yields a more accurate "
            "model.\n\nIf you already have a dataset of images, skip the `prepare data` "
            "option and just run `prepare config`. <strong>Note!</strong> If you do "
            "this, be sure to changethe `data_path` option in the config to your "
            "specified image folder.</qt>"
        )
        super().__init__(msg, title="Prepare data")
        self.gemovi_window = gemovi_window
        for function in self.prepare_data, self.prepare_config:
            self.editor.registerFunction(function)

    @bind(test_size=dict(step=0.1, limits=[0.01, 0.99]))
    def prepare_data(self, random_state=42, test_size=0.1):
        if self.folder is None:
            raise ValueError("Please specify a folder first by running `set folder`.")
        # Load the digits dataset
        digits = load_digits()
        X = digits.data
        y = digits.target

        # Make classic train/test splits
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        for folder_name, images in zip(["data_train", "data_test"], [X_train, X_test]):
            out_folder = self.folder / folder_name
            out_folder.mkdir(exist_ok=True, parents=True)
            for ii, image in enumerate(images):
                image = image.reshape((8, 8))
                image = (image - image.min()) / (image.max() - image.min())
                image = (image * 255).astype("uint8")
                image = Image.fromarray(image)
                image.save(out_folder / f"{ii}.png")
            for file, data in zip(["labels_train", "labels_test"], [y_train, y_test]):
                df = pd.DataFrame(data.reshape(-1, 1))
                df.columns = ["label"]
                df.to_csv(self.folder / f"{file}.csv", index=False)

    def prepare_config(self, use_gpu=True):
        if self.folder is None:
            raise ValueError("Please specify a folder first by running `set folder`.")
        base_config = copy.deepcopy(self.gemovi_window.parameter_info)

        data_params = base_config["data_params"]
        trainer_params = base_config["trainer_params"]

        data_params["data_path"] = str(self.folder / "data_train")
        data_params["num_workers"] = 1
        if not use_gpu:
            del trainer_params["accelerator"]
            del trainer_params["devices"]
        trainer_params["max_epochs"] = 5
        trainer_params["model_name"] = self.gemovi_window.model_cls.__name__
        trainer_params["log_dir"] = str(self.folder / trainer_params["log_dir"])

        fns.saveToFile(base_config, self.folder / "config.yaml")


class ModelTrainerPage(TutorialPage):
    def __init__(self):
        msg = (
            "Skip this page if you already have weights from a trained model. "
            "Otherwise, this page trains a model from the data generated on the "
            "previous page."
        )
        super().__init__(msg, title="Train a model")
        self.editor.registerFunction(self.train_model)

    def train_model(self):
        # If pytorch lightning wasn't installed, this isn't possible
        try:
            from gemovi.vae.train import main as train_main
        except ImportError:
            raise ImportError(
                "To train a model, you must install pytorch lightning using "
                "`pip install pytorch-lightning`"
            )
        if not self.folder:
            raise ValueError("Please specify a folder first by running `set folder`.")
        if not self.folder.joinpath("config.yaml").exists():
            raise ValueError(
                "No config file found; please run the previous page's"
                " `prepare config` function first."
            )

        QtWidgets.QMessageBox.information(
            self,
            "Training",
            "About to train model; close this dialog, then check the terminal for "
            "progress.",
        )
        train_main(self.folder / "config.yaml")


class FinishedPage(TutorialPage):
    def __init__(self, gemovi_window: ModelWindow = None):
        msg = (
            "Congratulations! You have a model that should be directly importable by "
            "the visualization package. Open the `settings` menu and load the best "
            "model weights from the training results folder. If you trained a model "
            "using the previous page, these should be under "
            "`gemovi-workspace/lightning_logs/version_0/checkpoints/`. "
        )
        super().__init__(msg, title="Finished!")
        self.gemovi_window = gemovi_window

        self.editor.registerFunction(self.open_settings)

    def open_settings(self):
        self.gemovi_window.raise_settings_window()


def finalize_tutorial_pages(pages):
    pass


class GettingStartedWizard(QtWidgets.QWizard):
    def __init__(self, parent: ModelWindow):
        super().__init__(parent)
        btn = self.WizardButton
        button_layout = [
            btn.Stretch,
            btn.BackButton,
            btn.CancelButton,
            btn.NextButton,
            btn.FinishButton,
        ]
        self.setButtonLayout(button_layout)
        self.setup_pages(self.get_pages())
        self.setWindowTitle("Tutorial")

    def get_pages(self):
        return [
            WelcomePage(),
            LoadDataPage(self.parent()),
            ModelTrainerPage(),
            FinishedPage(self.parent()),
        ]

    def setup_pages(self, pages):
        for page in pages:
            self.addPage(page)
            if not isinstance(page, TutorialPage):
                continue
            page.editor.tree.setMinimumHeight(
                page.editor.tree.sizeHint().height() * 1.25
            )
            for connect_page in pages:
                if page is connect_page or not isinstance(connect_page, TutorialPage):
                    continue
                page.sig_folder_changed.connect(connect_page.on_folder_changed)


class LatentTransformWizard(GettingStartedWizard):
    def __init__(self, parent: ModelWindow):
        window: ModelWindow = parent
        model_tab = None
        for ii in range(window.tab_group.count()):
            tab: ModelTab = window.tab_group.widget(ii)
            if isinstance(tab.model, DFCVAE):
                model_tab = tab
                break
        if model_tab is None:
            raise ValueError(
                "The `Data Transform` tutorial can only be run with a DFCVAE model "
                "class. Please restart gemovi with i.e. `python -m gemovi.viz "
                "--model_class dfcvae` to run this tutorial."
            )
        self.model_tab = model_tab
        super().__init__(parent)

    def get_pages(self):
        return [
            self.intro_factory(),
            self.download_data_factory(),
            self.load_images_and_labels_factory(),
            self.set_transformer_factory(),
            self.use_visuals_factory(),
        ]

    def intro_factory(self):
        page = TutorialPage(
            "This tutorial briefly shows the workflow for loading sample images from "
            "a folder into gemovi, running a transform on the latent space to increase "
            "the spread of the latent space, and using some of the visualizations.",
            title="Data Transform Tutorial",
            register_set_folder=False,
        )
        page.editor.tree.hide()
        return page

    def download_data_factory(self):
        # Mangle the link to make it hard for web scrapers
        mangled = (
            r"^jjfi0%%mmm$ZhefXen$Yec%i^%__[.&gcdl(&'Z[b%777;=J-+_n8cM_Ci-<7)"
            r"IoC[W5Zb3&"
        )
        url = "".join([chr(ord(letter) + 10) for letter in mangled])
        page = TutorialPage(
            f"<qt>First, we'll load some sample data and a model. Download the zip file "
            f"from <a href='{url}'>{url}</a> and extract it to a folder. Then, "
            f"point the `folder` below to the folder containing both the images and "
            f"model (i.e., the unzipped folder location).\n\n"
            f"Alternatively, skip the download and point to your own folder with a "
            f"`images` subfolder, `labels` csv, and `dfcvae.ckpt` file.</qt>",
            title="Load data and model",
            register_set_folder=True,
        )
        page.label.setTextInteractionFlags(
            page.label.textInteractionFlags()
            | QtCore.Qt.TextInteractionFlag.TextBrowserInteraction
        )
        return page

    def load_images_and_labels_factory(self):
        page = TutorialPage(
            "First, use `load model` below to load the model weights.\n\n"
            "Next, we'll load the images and labels into gemovi with `load data`. This "
            "will take a few seconds. To do this yourself, set the right `source` path "
            "under`Sample Metadata` -> `Get Samples From Folder` and press `Run`. "
            "Similarly, the `labels` csv file can be passed to `Sample Metadata -> "
            "Lable Samples From File`. Note that a `label column` must also be "
            "specified before pressing `Run`. Hover over each parameter to see a "
            "description of what it does.",
            title="Load images and labels",
        )

        def load_model():
            win: ModelWindow = self.parent()
            win.update_weights(page.folder / "dfcvae.ckpt")

        def load_data():
            metadata = self.get_plugin(FileSampleMetadataPlugin)

            # use "registered" version to also update parameter in tree
            registered = self.model_tab.editor.nameFunctionMap[
                metadata.get_samples_from_folder.__name__
            ]
            registered(source=page.folder / "images")

            registered = self.model_tab.editor.nameFunctionMap[
                metadata.label_samples_from_file.__name__
            ]
            registered(file=page.folder / "labels.csv", label_column="label")

        page.editor.registerFunction(load_model)
        page.editor.registerFunction(load_data)
        return page

    def set_transformer_factory(self):
        page = TutorialPage(
            "Now, we'll set the `transformer` to a PCA decomposition. This will "
            "allow us to spread out the variance of the latent space. The `transformer` "
            "can be set under `Latent Cross Section` -> `Set Transformer`. Which "
            "cross section is used can be updated by changing `Latent Cross Section` -> "
            "`Update Plane Dimensions`.",
            title="Set transformer",
            register_set_folder=False,
        )

        def set_transformer():
            tab: GenerativeTab = self.model_tab  # noqa
            tab.set_transformer()

        page.editor.registerFunction(set_transformer)
        return page

    def use_visuals_factory(self):
        page = TutorialPage(
            "Finally, we'll use some of the visualizations to see the effect of the "
            "transformer. Click on a scatterplot point to see a popup with the image "
            "and label. a target will also appear in the latent space. The target can "
            "be moved by dragging it. As it moves, the image will change to the "
            "decoding at the new latent position.\n\n"
            "There are many more visualization options available! Hover over each "
            "parameter in the tree to see a description of what it does.\n\n"
            "Change what happens when you click by choosing a different listener"
            "under `Listeners` -> `Set Enabled Listeners`.",
            title="Use visuals",
            register_set_folder=False,
        )
        page.editor.tree.hide()
        return page

    def get_plugin(self, plugin_cls: T.Type[T]) -> T:
        requested = None
        for plugin in self.model_tab.plugins.values():
            if isinstance(plugin, plugin_cls):
                requested = plugin
        if requested is None:
            raise ValueError("No metadata plugin found.")
        return requested
