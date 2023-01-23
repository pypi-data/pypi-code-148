from typing import List

import torch
from torch import nn
from torch.nn import functional as F
from torchvision.models import VGG19_BN_Weights, vgg19_bn

from gemovi.common.utils import load_trainer_state_dict
from gemovi.vae.models import BaseVAE


class DFCVAE(BaseVAE):
    def __init__(
        self,
        in_channels: int,
        latent_dim: int,
        hidden_dims: List = None,
        alpha: float = 1,
        beta: float = 0.5,
        strip_feature_weights_on_save=True,
        initial_weights_file: str = None,
        **kwargs,
    ) -> None:
        super(DFCVAE, self).__init__()

        self.latent_dim = latent_dim
        self.alpha = alpha
        self.beta = beta
        self.strip_feature_weights_on_save = strip_feature_weights_on_save

        modules = []
        if hidden_dims is None:
            hidden_dims = [32, 64, 128, 256, 512]

        # Build Encoder
        for h_dim in hidden_dims:
            modules.append(
                nn.Sequential(
                    nn.Conv2d(
                        in_channels,
                        out_channels=h_dim,
                        kernel_size=3,
                        stride=2,
                        padding=1,
                    ),
                    nn.BatchNorm2d(h_dim),
                    nn.LeakyReLU(),
                )
            )
            in_channels = h_dim

        self.encoder = nn.Sequential(*modules)
        self.fc_mu = nn.Linear(hidden_dims[-1] * 4, latent_dim)
        self.fc_var = nn.Linear(hidden_dims[-1] * 4, latent_dim)

        # Build Decoder
        modules = []

        self.decoder_input = nn.Linear(latent_dim, hidden_dims[-1] * 4)

        hidden_dims.reverse()

        for i in range(len(hidden_dims) - 1):
            modules.append(
                nn.Sequential(
                    nn.ConvTranspose2d(
                        hidden_dims[i],
                        hidden_dims[i + 1],
                        kernel_size=3,
                        stride=2,
                        padding=1,
                        output_padding=1,
                    ),
                    nn.BatchNorm2d(hidden_dims[i + 1]),
                    nn.LeakyReLU(),
                )
            )

        self.decoder = nn.Sequential(*modules)

        self.final_layer = nn.Sequential(
            nn.ConvTranspose2d(
                hidden_dims[-1],
                hidden_dims[-1],
                kernel_size=3,
                stride=2,
                padding=1,
                output_padding=1,
            ),
            nn.BatchNorm2d(hidden_dims[-1]),
            nn.LeakyReLU(),
            nn.Conv2d(hidden_dims[-1], out_channels=3, kernel_size=3, padding=1),
            nn.Tanh(),
        )

        self.feature_network = vgg19_bn(weights=VGG19_BN_Weights.DEFAULT)

        # Freeze the pretrained feature network
        for param in self.feature_network.parameters():
            param.requires_grad = False

        self.feature_network.eval()

        if initial_weights_file is not None:
            load_trainer_state_dict(
                self, torch.load(initial_weights_file), strict=False
            )

    def state_dict(self, *args, **kwargs) -> dict:
        """
        VGG19 is huge, so don't save these pretrained weights. They don't change
        during training anyway.
        """
        if not self.strip_feature_weights_on_save:
            return super().state_dict(*args, **kwargs)

        # Temporarily pretend we don't have a "feature_network" module
        try:
            feature_network = self._modules.pop("feature_network")
            state_dict = super().state_dict(*args, **kwargs)
        finally:
            self._modules["feature_network"] = feature_network
        return state_dict

    def encode(self, input: torch.Tensor) -> List[torch.Tensor]:
        """
        Encodes the input by passing through the encoder network
        and returns the latent codes.
        :param input: (Tensor) Input tensor to encoder [N x C x H x W]
        :return: (Tensor) List of latent codes
        """
        result = self.encoder(input)
        result = torch.flatten(result, start_dim=1)

        # Split the result into mu and var components
        # of the latent Gaussian distribution
        mu = self.fc_mu(result)
        log_var = self.fc_var(result)

        return [mu, log_var]

    def decode(self, z: torch.Tensor) -> torch.Tensor:
        """
        Maps the given latent codes
        onto the image space.
        :param z: (Tensor) [B x D]
        :return: (Tensor) [B x C x H x W]
        """
        result = self.decoder_input(z)
        result = result.view(-1, 512, 2, 2)
        result = self.decoder(result)
        result = self.final_layer(result)
        return result

    def reparameterize(self, mu: torch.Tensor, logvar: torch.Tensor) -> torch.Tensor:
        """
        Reparameterization trick to sample from N(mu, var) from
        N(0,1).
        :param mu: (Tensor) Mean of the latent Gaussian [B x D]
        :param logvar: (Tensor) Standard deviation of the latent Gaussian [B x D]
        :return: (Tensor) [B x D]
        """
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return eps * std + mu

    def forward(self, input: torch.Tensor, **kwargs) -> List[torch.Tensor]:
        mu, log_var = self.encode(input)
        z = self.reparameterize(mu, log_var)
        recons = self.decode(z)

        recons_features = self.extract_features(recons)
        input_features = self.extract_features(input)

        return [recons, input, recons_features, input_features, mu, log_var]

    def extract_features(
        self, input: torch.Tensor, feature_layers: List = None
    ) -> List[torch.Tensor]:
        """
        Extracts the features from the pretrained model
        at the layers indicated by feature_layers.
        :param input: (Tensor) [B x C x H x W]
        :param feature_layers: List of string of IDs
        :return: List of the extracted features
        """
        if feature_layers is None:
            feature_layers = ["14", "24", "34", "43"]
        features = []
        result = input
        for (key, module) in self.feature_network.features._modules.items():
            result = module(result)
            if key in feature_layers:
                features.append(result)

        return features

    def loss_function(self, *args, **kwargs) -> dict:
        """
        Computes the VAE loss function.
        KL(N(\mu, \sigma), N(0, 1)) = \log \frac{1}{\sigma} + \frac{\sigma^2 + \mu^2}{2} - \frac{1}{2}
        :param args:
        :param kwargs:
        :return:
        """
        recons = args[0]
        input = args[1]
        recons_features = args[2]
        input_features = args[3]
        mu = args[4]
        log_var = args[5]

        kld_weight = kwargs["M_N"]  # Account for the minibatch samples from the dataset
        recons_loss = F.mse_loss(recons, input)

        feature_loss = 0.0
        for (r, i) in zip(recons_features, input_features):
            feature_loss += F.mse_loss(r, i)

        kld_loss = torch.mean(
            -0.5 * torch.sum(1 + log_var - mu**2 - log_var.exp(), dim=1), dim=0
        )

        loss = (
            self.beta * (recons_loss + feature_loss)
            + self.alpha * kld_weight * kld_loss
        )
        return {"loss": loss, "Reconstruction_Loss": recons_loss, "KLD": -kld_loss}

    def sample(self, num_samples: int, current_device: int, **kwargs) -> torch.Tensor:
        """
        Samples from the latent space and return the corresponding
        image space map.
        :param num_samples: (Int) Number of samples
        :param current_device: (Int) Device to run the model
        :return: (Tensor)
        """
        z = torch.randn(num_samples, self.latent_dim)

        z = z.to(current_device)

        samples = self.decode(z)
        return samples

    def generate(self, x: torch.Tensor, **kwargs) -> torch.Tensor:
        """
        Given an input image x, returns the reconstructed image
        :param x: (Tensor) [B x C x H x W]
        :return: (Tensor) [B x C x H x W]
        """

        return self.forward(x)[0]

    def likelihood_is_real(self, images: torch.Tensor):
        mu, log_var = self.encode(images)

        var = torch.exp(log_var)
        multidim_liklihoods = torch.exp(-0.5 * mu**2 / var)
        return torch.mean(multidim_liklihoods, dim=1)

    def difference_from_generated(self, images: torch.Tensor, num_std_dev_samples=20):
        """
        Genrerate a grayscale difference image of the input minus its
        encoded->generated representation.
        """
        z, log_var = self.encode(images)
        generated = self.decode(z)
        difference = images - generated
        # Differences are highly fluctuating, prefer regions that
        # are consistent with each other by blurring
        difference = F.avg_pool2d(difference, 5, stride=1, padding=2).mean(dim=1)
        if num_std_dev_samples <= 1:
            return difference
        # Else
        heatmap_weights = torch.ones_like(difference, device=images.device)
        for ii, (sample_z, sample_log_var) in enumerate(zip(z, log_var)):
            varied_batch = (
                sample_z
                + torch.randn(
                    num_std_dev_samples, *sample_z.shape, device=images.device
                )
                * torch.exp(sample_log_var)
                * 4
            )
            # Check std dev of each pixel across samples and colors
            encoding_jitter = (self.decode(varied_batch) - generated[ii]).abs()
            if (max_jitter := encoding_jitter.max()) > 0:
                encoding_jitter = encoding_jitter / max_jitter
                encoding_jitter[encoding_jitter > 0] = -torch.log(
                    encoding_jitter[encoding_jitter > 0]
                )
                heatmap_weights[ii] = (
                    (encoding_jitter / encoding_jitter.max()).mean(dim=0).mean(dim=0)
                )
        return (difference * heatmap_weights).abs()
