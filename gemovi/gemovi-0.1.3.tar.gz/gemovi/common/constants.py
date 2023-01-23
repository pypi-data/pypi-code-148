import torch

num_gpus = 1
pad_on_resize = True


def get_device(ngpu=None):
    if ngpu is None:
        ngpu = num_gpus
    return torch.device("cuda:0" if (torch.cuda.is_available() and ngpu > 0) else "cpu")
