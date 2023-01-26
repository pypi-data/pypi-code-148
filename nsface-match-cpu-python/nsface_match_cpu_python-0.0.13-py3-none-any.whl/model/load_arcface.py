import torch

import numpy as np
import subprocess

from .load_onnx import Onnx_session
from .load_vino import Openvino_multi


def torch2numpy(outs):
    if isinstance(outs,list):
        outs = outs[0]
        
    return np.array(outs)  


class Arcface:
    def __init__(self,model_type,model_path,**kwargs):

        self.model_path = model_path
        self.model_type = model_type

        if self.model_type=='onnx':
            self.net = Onnx_session(self.model_path,onnx_device='cpu')

        elif self.model_type=='openvino':
            self.net = Openvino_multi(self.model_path)

    def get(self,img):
        # onnx,vino (numpy, (b,3,h,w))
        # trt       (torch, (b,3,h,w), cuda)

        # shape
        if len(img.shape)==3:
            img = np.expand_dims(img,0)
        img = np.transpose(img,(0,3,1,2))

        # norm
        img = ((img / 255) - 0.5) / 0.5

        img = img.astype(np.float32)

        feat = self.net(img)
        feat = torch2numpy(feat)

        return feat

