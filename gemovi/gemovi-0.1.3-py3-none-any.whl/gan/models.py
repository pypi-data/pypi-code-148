from __future__ import annotations

from typing import Type

import numpy as np
import torch
from torch import nn, optim
from torch.nn import functional as F

from gemovi.common.utils import ParamDict, load_trainer_state_dict


def conv_transpose_bn(
    in_planes: int,
    out_planes: int,
    stride: int = 1,
    groups: int = 1,
    padding: int = 1,
    kernel_size=4,
    relu=True,
) -> nn.Sequential:
    """kxk (default 4x4) transposed convolution with padding and batch norm"""
    seq = nn.Sequential(
        nn.ConvTranspose2d(
            in_planes,
            out_planes,
            kernel_size=kernel_size,
            stride=stride,
            padding=padding,
            groups=groups,
            bias=False,
        ),
        nn.BatchNorm2d(out_planes),
    )
    if relu:
        seq.add_module(str(len(seq)), nn.ReLU(True))
    return seq


def conv_bn(
    in_planes: int,
    out_planes: int,
    stride: int = 1,
    groups: int = 1,
    padding: int = 1,
    kernel_size=4,
    leaky_relu=True,
) -> nn.Sequential:
    """kxk (default 4x4) convolution with padding and batch norm"""
    seq = nn.Sequential(
        nn.Conv2d(
            in_planes,
            out_planes,
            kernel_size=kernel_size,
            stride=stride,
            padding=padding,
            groups=groups,
            bias=False,
        ),
        nn.BatchNorm2d(out_planes),
    )
    if leaky_relu:
        seq.add_module(str(len(seq)), nn.LeakyReLU(0.2, True))
    return seq


def _validate_input_size(
    size: int | tuple[int, int], force_square=False, force_powers_of_two=False
) -> tuple[int, int]:
    if isinstance(size, int):
        size = (size, size)
    if len(size) != 2:
        raise ValueError(f"Invalid input size `{size}`")
    if force_square and size[0] != size[1]:
        raise ValueError(f"Input size must be square, got `{size}`")
    if force_powers_of_two and not all(np.log2(s).is_integer() for s in size):
        raise ValueError(f"Input size must be powers of two, got `{size}`")
    return size


class Discriminator(nn.Module):
    def __init__(self, num_filters, num_image_channels, image_size=64):
        super().__init__()

        # We start with input size (channels, image_size, image_size) and
        # end with (1, 1, 1) (i.e. a single scalar)
        # So downsample by a factor of 2 at each stage until the last layer, where
        # a stride of 1 turns 4x4 into 1x1
        size, _ = _validate_input_size(
            image_size, force_square=True, force_powers_of_two=True
        )
        n_multipliers = int(np.log2(size // 4))
        multipliers = [2**ii for ii in range(n_multipliers)]

        first_layer = nn.Sequential(
            nn.Conv2d(num_image_channels, num_filters, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
        )
        # Keeps growing filters while decreasing spatial size
        conv_layers = [
            conv_bn(num_filters * in_mult, num_filters * out_mult, stride=2)
            for in_mult, out_mult in zip(multipliers, multipliers[1:])
        ]
        # End of layers should be a single 4x4 convolution, turn this into
        # scalar with final conv + sigmoid activation
        last_layer = nn.Sequential(
            nn.Conv2d(num_filters * multipliers[-1], 1, 4, 1, 0, bias=False),
            nn.Sigmoid(),
        )
        self.main = nn.Sequential(*first_layer, *conv_layers, *last_layer)

    def forward(self, input):
        return self.main(input)


class Generator(nn.Module):
    def __init__(self, num_latent_dims, num_filters, num_image_channels, image_size=64):
        super().__init__()
        # Since square size is required, arbitrarily grab the first value
        size, _ = _validate_input_size(
            image_size, force_square=True, force_powers_of_two=True
        )
        # First conv has stride 1 and increases size by 4, all others have stride 2
        # So divide by 4 to get number of conv layers & multipliers
        # Further reduce by 1 to account for the last conv layer
        n_multipliers = int(np.log2(size // 4)) - 1
        multipliers = [2**ii for ii in range(n_multipliers, -1, -1)]

        # input is Z, going into a convolution
        first_layer = conv_transpose_bn(
            num_latent_dims, num_filters * multipliers[0], stride=1, padding=0
        )
        conv_upsampling = [
            conv_transpose_bn(num_filters * in_mult, num_filters * out_mult, stride=2)
            for (in_mult, out_mult) in zip(multipliers, multipliers[1:])
        ]
        # Final layer converts to num_image_channels x image_size x image_size
        last_layer = conv_transpose_bn(
            num_filters, num_image_channels, stride=2, relu=False
        )
        self.main = nn.Sequential(
            *first_layer, *conv_upsampling, *last_layer, nn.Tanh()
        )

    def forward(self, input):
        return self.main(input)


class Encoder(Discriminator):
    def __init__(self, num_filters, num_image_channels, num_latent_dims, *image_wh):
        super().__init__(num_filters, num_image_channels)

        if len(image_wh) == 1:
            image_wh = (image_wh[0], image_wh[0])
        image_size = (num_image_channels, *image_wh)
        num_in_features = np.prod(self.main(torch.rand(1, *image_size)).shape)
        self.main[-1] = nn.Linear(num_in_features, num_latent_dims)


class DCGAN(nn.Module):
    real_label = 1.0
    fake_label = 0.0

    manage_gradients = True

    def __init__(
        self,
        num_latent_dims=128,
        num_generator_filters=64,
        num_discrim_filters=64,
        num_image_channels=3,
        image_size=64,
        learn_rate=0.0002,
        beta1=0.5,
        beta2=0.999,
        discriminator_cls=Discriminator,
        generator_cls=Generator,
        encoder_cls: Type[Encoder] = None,
        initial_weights_file: str = None,
    ):
        super().__init__()
        self.opts = ParamDict(locals())
        for kk in list(self.opts):
            if kk == "self" or "cls" in kk:
                self.opts.pop(kk)

        generator = generator_cls(
            num_latent_dims,
            num_generator_filters,
            num_image_channels,
            image_size=image_size,
        )
        discriminator = discriminator_cls(
            num_discrim_filters, num_image_channels, image_size=image_size
        )
        encoder = None
        if encoder_cls is not None:
            encoder = encoder_cls(
                num_discrim_filters, num_image_channels, num_latent_dims, image_size
            )

        self.generator = generator
        self.discriminator = discriminator
        self.encoder = encoder

        # Apply the weights_init function to randomly initialize all weights
        # to mean=0, stdev=0.02 as per the DCGAN paper.
        for model in self.children():
            model.apply(self._weights_init)
        if initial_weights_file:
            load_trainer_state_dict(
                self, torch.load(initial_weights_file), strict=False
            )

        self.configure_optimizers()

        # Initialize BCELoss function
        self.criterion = F.binary_cross_entropy

    def configure_optimizers(self):
        betas = self.opts.beta1, self.opts.beta2
        optimizers = []
        for model in self.children():
            cur_optim = optim.Adam(
                model.parameters(), lr=self.opts.learn_rate, betas=betas
            )
            optimizers.append(cur_optim)
        # "None" only applies when no encoder is used
        optimizers.append(None)
        self.gen_optim, self.discrim_optim, self.encoder_optim = optimizers[:3]
        return optimizers[:3]

    def resolve_batch_and_noise(self, batch):
        if not isinstance(batch, torch.Tensor):
            batch, _ = batch
        b_size = batch.size(0)
        noise = torch.randn(
            b_size, self.opts.num_latent_dims, 1, 1, device=batch.device
        )
        return batch, noise

    def training_step(self, batch, optimizer_idx):
        batch, noise = self.resolve_batch_and_noise(batch)
        return self.train_step_for_idx(optimizer_idx)(batch, noise)

    def loss_for_idx(self, idx):
        return ["err_g", "err_d", "err_e"][idx]

    def train_step_for_idx(self, idx):
        return [
            self.gen_train_step,
            self.discrim_train_step,
            self.encoder_train_step,
        ][idx]

    def _maybe_update_gradients(self, optimizer, loss):
        if self.manage_gradients:
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    def discrim_train_step(self, batch, noise):
        """Update D network: maximize log(D(x)) + log(1 - D(G(z)))"""
        # Forward pass real batch through D
        discrim_on_real = self.discriminator(batch).view(-1)
        label = torch.full_like(discrim_on_real, self.real_label)
        # Calculate loss on all-real batch
        err_d_real = self.criterion(discrim_on_real, label)

        # Train with all-fake batch
        # Generate fake image batch with G
        fake = self.generator(noise).detach()
        label = torch.full_like(discrim_on_real, self.fake_label)
        # Classify all fake batch with D
        discrim_on_fake = self.discriminator(fake).view(-1)
        # Calculate D's loss on the all-fake batch
        err_d_fake = self.criterion(discrim_on_fake, label)
        # Compute error of D as sum over the fake and the real batches
        err_d = (err_d_real + err_d_fake) / 2

        self._maybe_update_gradients(self.discrim_optim, err_d)

        d_g_z1 = discrim_on_fake.mean()
        d_x = discrim_on_real.mean()
        log = dict(err_d=err_d, d_g_z1=d_g_z1, d_x=d_x)
        return log

    def gen_train_step(self, batch, noise):
        """Update G network: maximize log(D(G(z)))"""

        fake = self.generator(noise)

        # Since we just updated D, perform another forward pass of all-fake batch through D
        output = self.discriminator(fake).view(-1)
        label = torch.full_like(output, self.real_label)
        # Calculate G's loss based on this output
        err_g = self.criterion(output, label)
        d_g_z2 = output.mean()
        log_dict = dict(d_g_z2=d_g_z2, err_g=err_g)

        self._maybe_update_gradients(self.gen_optim, err_g)

        return log_dict

    def encoder_train_step(self, batch, noise):
        if not self.encoder:
            return dict()
        fake = self.generator(noise).detach()
        encoded = self.encoder(fake).view(noise.shape)
        err_e = F.mse_loss(encoded, noise)
        self._maybe_update_gradients(self.encoder_optim, err_e)

        log = dict(err_e=err_e)
        return log

    # custom weights initialization called on netG and netD
    @staticmethod
    def _weights_init(model):
        classname = model.__class__.__name__
        if classname.find("Conv") != -1:
            nn.init.normal_(model.weight.data, 0.0, 0.02)
        elif classname.find("BatchNorm") != -1:
            nn.init.normal_(model.weight.data, 1.0, 0.02)
            nn.init.constant_(model.bias.data, 0)

    def likelihood_is_real(self, images: torch.Tensor):
        return self.discriminator(images).view(-1)
