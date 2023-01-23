import logging

import torch

from dash.convertion.face_utils.models.fs_networks import Generator_Adain_Upsample
from dash.custom_utils.device import get_device

logger = logging.getLogger(__name__)


class FaceSwapNN(torch.nn.Module):
    def initialize(self, opt):
        self.Tensor = torch.Tensor
        torch.backends.cudnn.benchmark = True
        device = get_device()

        # Generator network
        self.generation_net = Generator_Adain_Upsample(input_nc=3, output_nc=3, latent_size=512, n_blocks=9, deep=False)
        self.generation_net.to(device)

        # Recognition network
        recognition_net_checkpoint = torch.load(opt.main_model, map_location=device)
        self.recognition_net = recognition_net_checkpoint['model'].module
        self.recognition_net = self.recognition_net.to(device)
        self.recognition_net.eval()
        self.generation_net.load_state_dict(torch.load(opt.generator))

    def forward(self, img_att, latent_id):
        return self.generation_net.forward(img_att, latent_id)
