import srcheck
import torch

# load torch script model
model = torch.jit.load("/home/csaybar/Downloads/demo04quant.pt")
class srmodel(torch.nn.Module):
    def __init__(self, model):
        super(srmodel, self).__init__()
        self.model = model
    def forward(self, x):
        return self.model(x[:, None, :, :])
model = srmodel(model)

srfmodel(torch.Tensor(layer))


