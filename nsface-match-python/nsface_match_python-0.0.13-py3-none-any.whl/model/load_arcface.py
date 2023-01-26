import torch

import numpy as np
import subprocess

from .load_onnx import Onnx_session
from .load_trt import load as Trt_load
from .load_vino import Openvino_multi

def check_gpu():
    cmd = "nvidia-smi --list-gpus"
    output = subprocess.check_output(cmd,shell=True)
    lines = output.decode().split('\n')
    lines = [ line.strip() for line in lines if line.strip() != '' ]

    return lines

def torch2numpy(outs):
    if isinstance(outs,list):
        outs = outs[0]
            
    if torch.is_tensor(outs):
        if outs.device.type=='cuda':
            outs = outs.cpu()
        
    return np.array(outs)  


class Arcface:
    def __init__(self,model_type,model_path,**kwargs):

        self.model_path = model_path
        self.model_type = model_type
        self.onnx_device = kwargs.get('onnx_device','cuda')

        if self.model_type=='onnx':
            if self.onnx_device=='cuda' and len(check_gpu())==0:
                print("GPU Not Exists...")
                return None
            self.net = Onnx_session(self.model_path,onnx_device=self.onnx_device)
        
        elif self.model_type=='v8.trt':
            if len(check_gpu())==0:
                print("GPU Not Exists...")
                return None
            torch.cuda.initialized = True
            torch.cuda.is_available()
            torch.cuda.set_device(0)
            self.net = Trt_load(self.model_path)

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

        # to cuda
        if self.model_type=='v8.trt':
            img = torch.from_numpy(img)
            img = img.cuda()

        feat = self.net(img)
        feat = torch2numpy(feat)

        return feat

