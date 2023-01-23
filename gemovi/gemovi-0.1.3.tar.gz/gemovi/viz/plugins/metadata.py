from __future__ import annotations

import os
import typing as t
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from qtextras import OptionsDict, ParameterEditor, bindInteractorOptions as bind
from sklearn.cluster import DBSCAN, FeatureAgglomeration, KMeans, MeanShift

from gemovi.common.utils import read_image_folder, tensor_to_np
from gemovi.viz.plugins import GenerativeTabPlugin, _mkspec

if t.TYPE_CHECKING:
    from gemovi.viz.base import GenerativeTab
    from gemovi.viz.vae import VAEEncoderTab


class SampleMetadataPlugin(GenerativeTabPlugin):
    name_clusterer_map = dict(
        kmeans=KMeans, agg=FeatureAgglomeration, dbscan=DBSCAN, meanshift=MeanShift
    )

    def __init__(self, tab: GenerativeTab):
        super().__init__(tab)
        tab.sig_model_changed.connect(self.on_model_changed)

    def on_model_changed(self):
        self.get_samples_from_latent_space()

    @bind(
        cluster_method=_mkspec("list", limits=list(name_clusterer_map)),
        cluster_kwargs=_mkspec("text"),
    )
    def label_samples_from_clustering(
        self,
        cluster_method="kmeans",
        cluster_kwargs: str | dict = None,
    ):
        """
        Fits a scikit-learn clustering algorithm to the latent space of the current model
        and labels the samples with the cluster labels.

        Parameters
        ----------
        cluster_method
            Clustering method to use. It is fit on the latent space of the samples,
            including any dimension transforms that have been applied. The output
            of ``fit_predict`` is used to label the samples.
        cluster_kwargs
            Keyword arguments to pass to the clustering method. If a string, it is
            evaluated as a dictionary literal. Multiple keywords can be comma-separated,
            e.g. ``"n_clusters=10, n_init=10"``.
        """
        samples_info = self.tab.samples_info
        if samples_info.samples is None:
            return
        if cluster_kwargs is None:
            cluster_kwargs = {}
        elif isinstance(cluster_kwargs, str):
            cluster_str = f"dict({cluster_kwargs})"
            cluster_kwargs = eval(cluster_str)

        clusterer = self.name_clusterer_map[cluster_method](**cluster_kwargs)
        transformed = self.tab.dim_transformer.transform(samples_info.samples)
        labels = clusterer.fit_predict(tensor_to_np(transformed))
        mapper = OptionsDict("Clusterer")
        numeric, mapping = mapper.toNumeric(labels, rescale=True, returnMapping=True)
        samples_info.number_label_map = mapping
        samples_info.numeric_labels = numeric

        self.tab.sig_samples_changed.emit()

    def get_samples_from_latent_space(self, n_samples=25):
        """
        Reset the sample latents to a random set of samples from the model

        Parameters
        ----------
        n_samples
            Number of samples to use
        """
        if n_samples <= 0:
            n_samples = None
        self.tab.samples_info.samples = self.tab.get_random_latent_samples(n_samples)
        self.tab.samples_info.unset_labels()
        self.tab.sig_samples_changed.emit()

    @bind(file=dict(type="file", fileMode="AnyFile", acceptMode="AcceptSave"))
    def save_samples(self, file="./sample_info.pt"):
        """
        Save the samples and their metadata (label, numeric->label map, etc.) to a file.

        Uses ``torch.save`` behind the scenes, so the file can be loaded with
        ``torch.load``.

        Parameters
        ----------
        file
            The file to save to, typically using the .pt extension
        """
        torch.save(self.tab.samples_info.state_dict(), file)

    @bind(file=dict(type="file"))
    def load_samples(self, file="./sample_info.pt"):
        """
        Loads a file saved by :meth:`save_samples`

        Parameters
        ----------
        file
            The file to load
        """
        self.tab.samples_info.load_state_dict(torch.load(file))
        self.tab.sig_samples_changed.emit()

    def register_functions(self, editor: ParameterEditor):
        editor.registerFunction(self.get_samples_from_latent_space)
        editor.registerFunction(self.label_samples_from_clustering)
        editor.registerFunction(self.save_samples)
        editor.registerFunction(self.load_samples)


class FileSampleMetadataPlugin(SampleMetadataPlugin):
    # Ensure name is same as parent
    name = "Sample Metadata"

    tab: VAEEncoderTab

    def register_functions(self, editor: ParameterEditor):
        editor.registerFunction(self.get_samples_from_folder)
        editor.registerFunction(self.label_samples_from_file)
        super().register_functions(editor)

    @bind(file=dict(type="file", value=""))
    def label_samples_from_file(self, file, label_column=""):
        """
        Label the samples with the values in a CSV file.

        Parameters
        ----------
        file
            Csv with at least ``label_column`` (see below) present
        label_column
            Column in ``file`` to use as label. If not present in the file or not
            provided, the function returns without doing anything. Depending on
            the data type of the column:
              - If numeric/bool-like, the values are normalized to 0->1 and used
                as labels.
              - If string-like, the values are mapped to numeric labels based on their
                order of appearance and used as above.
        """
        info = self.tab.samples_info
        df = pd.read_csv(file)
        if len(df) != len(info.samples) or label_column not in df:
            return
        labels = df[label_column]
        valid_label_mask = labels.notna()
        param = OptionsDict(label_column, "")
        numeric, mapping = param.toNumeric(
            labels[valid_label_mask], rescale=True, returnMapping=True
        )
        if not valid_label_mask.all():
            # Need to resize `numeric` to match data + add `nan` to the map
            new_numeric = np.full(len(labels), np.nan)
            new_numeric[valid_label_mask] = numeric
            mapping[np.nan] = None
            numeric = new_numeric
        info.number_label_map = mapping
        info.numeric_labels = numeric

        self.tab.sig_samples_changed.emit()

    @bind(source=_mkspec("file", fileMode="Directory"))
    def get_samples_from_folder(
        self,
        source: str | Path | list | torch.Tensor = "",
        batch_size=32,
        max_n_samples=1_000,
    ):
        """
        Generates latent samples by encoding each image in a folder.

        Parameters
        ----------
        source
            Folder of images. If blank, random latent samples are used instead
        batch_size
            Batch size to read images. Useful when dealing with large amounts of data.
        max_n_samples
            Upper bound on randomly selected samples from the source.
        """
        if not os.path.exists(source):
            return
        samples, names = read_image_folder(source)
        if not samples:
            return
        if max_n_samples < len(samples):
            keep_idxs = np.random.choice(len(samples), max_n_samples, replace=False)
            samples = [samples[i] for i in keep_idxs]
            names = [names[i] for i in keep_idxs]
        mu_all, std_all = [], []
        for batch_start in range(0, len(samples), batch_size):
            batch = samples[batch_start : batch_start + batch_size]
            batch = torch.cat(
                [self.tab.image_as_normed_tensor(im) for im in batch], dim=0
            )
            mu, std = self.tab.forward_encoder(batch)
            mu = mu.view(-1, mu.shape[1])
            std = std.view(-1, std.shape[1])
            mu_all.append(mu)
            std_all.append(std)
        mu_all = torch.cat(mu_all, dim=0)

        info = self.tab.samples_info
        info.unset_labels()
        info.samples = mu_all
        info.image_files = [os.path.join(source, name) for name in names]
        self.tab.sig_samples_changed.emit()
