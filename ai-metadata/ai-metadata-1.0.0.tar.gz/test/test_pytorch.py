#
# Copyright (c) 2023 AutoDeployAI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris, load_boston
import pandas as pd
import numpy as np

from ai_metadata import ModelSerialization, MiningFunction, MetadataModel

seed = 123456
test_size = 0.33


def get_classifier():
    import torch.nn as nn  # PyTorch's module wrapper

    class Classifier(nn.Module):
        def __init__(self):
            super(Classifier, self).__init__()
            self.h_layer = nn.Linear(4, 3)
            self.s_layer = nn.Softmax()

        def forward(self, x):
            y = self.h_layer(x)
            p = self.s_layer(y)
            return p

    return Classifier()


def get_net():
    import torch
    import torch.nn as nn  # PyTorch's module wrapper
    import torch.nn.functional as F

    class Net(nn.Module):
        def __init__(self):
            super(Net, self).__init__()
            self.conv1 = nn.Conv2d(1, 32, 3, 1)
            self.conv2 = nn.Conv2d(32, 64, 3, 1)
            self.dropout1 = nn.Dropout2d(0.25)
            self.dropout2 = nn.Dropout2d(0.5)
            self.fc1 = nn.Linear(9216, 128)
            self.fc2 = nn.Linear(128, 10)

        def forward(self, x):
            x = self.conv1(x)
            x = F.relu(x)
            x = self.conv2(x)
            x = F.relu(x)
            x = F.max_pool2d(x, 2)
            x = self.dropout1(x)
            x = torch.flatten(x, 1)
            x = self.fc1(x)
            x = F.relu(x)
            x = self.dropout2(x)
            x = self.fc2(x)
            output = F.log_softmax(x, dim=1)
            return output

    return Net()


def test_classification():
    import torch
    import torch.nn as nn  # PyTorch's module wrapper
    from torch.autograd import Variable  # PyTorch's implementer of gradient descent and back

    X, y = load_iris(return_X_y=True)
    Y = pd.get_dummies(y).values
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)

    X_train_v = Variable(torch.FloatTensor(X_train), requires_grad=False)
    y_train_v = Variable(torch.FloatTensor(y_train), requires_grad=False)
    X_test_v = Variable(torch.FloatTensor(X_test), requires_grad=False)
    y_test_v = Variable(torch.FloatTensor(y_test), requires_grad=False)

    classifier = get_classifier()  # declaring the classifier to an object
    loss_fn = nn.BCELoss()  # calculates the loss
    optim = torch.optim.SGD(classifier.parameters(), lr=0.01)

    for num in range(100):  # 100 iterations
        pred = classifier(X_train_v)  # predict
        loss = loss_fn(pred, y_train_v)  # calculate loss
        optim.zero_grad()  # zero gradients to not accumulate
        loss.backward()  # update weights based on loss
        optim.step()  # update optimiser for next iteration

    model = MetadataModel.wrap(classifier,
                               x_test=X_test,
                               y_test=y_test,
                               source_object=get_classifier)
    model_metadata = model.model_metadata()

    print(model.model_metadata(as_json=True, indent=4))
    assert model_metadata['inputs'] == [
        {
            "name": None,
            "sample": [
                [
                    5.7,
                    4.4,
                    1.5,
                    0.4
                ]
            ],
            "type": "float64",
            "shape": [
                None,
                4
            ]
        }
    ]
    assert model_metadata['targets'] == [
        {
            "name": None,
            "sample": [
                1,
                0,
                0
            ],
            "type": "uint8",
            "shape": [
                None,
                3
            ]
        }
    ]
    assert model_metadata['outputs'] == [
        {
            "name": None,
            "type": "float32",
            "shape": [
                None,
                3
            ]
        }
    ]
    prediction = model.predict(model_metadata['inputs'][0]['sample'])
    assert prediction.tolist()
    assert model_metadata['metrics']
    assert model_metadata['object_name'] == 'get_classifier'
    assert model_metadata['object_source']
    assert model_metadata['serialization'] == ModelSerialization.PYTORCH
    assert model_metadata['function_name'] == MiningFunction.CLASSIFICATION
    assert model.save_model('./pytorch-cls')


def test_regression():
    import torch
    import torch.nn as nn  # PyTorch's module wrapper

    X, y = load_boston(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)

    torch.set_default_dtype(torch.float64)

    dim = X.shape[1]
    net = nn.Sequential(
        nn.Linear(dim, 50, bias=True), nn.ELU(),
        nn.Linear(50, 50, bias=True), nn.ELU(),
        nn.Linear(50, 50, bias=True), nn.Sigmoid(),
        nn.Linear(50, 1)
    )
    criterion = nn.MSELoss()
    opt = torch.optim.Adam(net.parameters(), lr=.0005)
    y_train_t = torch.from_numpy(y_train).clone().reshape(-1, 1)
    x_train_t = torch.from_numpy(X_train).clone()

    losssave = []
    stepsave = []

    for i in range(100):
        y_hat = net(x_train_t)
        loss = criterion(y_train_t, net(x_train_t))
        losssave.append(loss.item())
        stepsave.append(i)
        loss.backward()
        opt.step()
        opt.zero_grad()
        y_hat_class = (y_hat.detach().numpy())
        accuracy = np.sum(y_train.reshape(-1, 1) == y_hat_class) / len(y_train)
        if i > 0 and i % 100 == 0:
            print('Epoch %d, loss = %g acc = %g ' % (i, loss, accuracy))

    model = MetadataModel.wrap(net,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()

    print(model.model_metadata(as_json=True, indent=4))
    assert model_metadata['inputs'] == [
        {
            "name": None,
            "sample": [
                [
                    22.5971,
                    0.0,
                    18.1,
                    0.0,
                    0.7,
                    5.0,
                    89.5,
                    1.5184,
                    24.0,
                    666.0,
                    20.2,
                    396.9,
                    31.99
                ]
            ],
            "type": "float64",
            "shape": [
                None,
                13
            ]
        }
    ]
    assert model_metadata['targets'] == [
        {
            "name": None,
            "sample": 7.4,
            "type": "float64",
            "shape": None
        }
    ]
    assert model_metadata['outputs'] == [
        {
            "name": None,
            "type": "float64",
            "shape": [
                None,
                1
            ]
        }
    ]

    prediction = model.predict(model_metadata['inputs'][0]['sample'])
    assert prediction.tolist()
    assert model_metadata['metrics']
    assert model_metadata['serialization'] == ModelSerialization.PYTORCH
    assert model_metadata['function_name'] == MiningFunction.REGRESSION
    assert model.save_model('./pytorch-reg')


def test_mnist():
    import torch
    import torch.optim as optim
    from torchvision import datasets, transforms
    from torch.optim.lr_scheduler import StepLR

    use_cuda = torch.cuda.is_available()
    batch_size = 64
    lr = 1.0
    gamma = 0.7
    epochs = 1

    torch.manual_seed(seed)
    device = torch.device("cuda" if use_cuda else "cpu")

    kwargs = {'batch_size': batch_size}
    if use_cuda:
        kwargs.update({'num_workers': 1,
                       'pin_memory': True,
                       'shuffle': True},
                      )

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    dataset1 = datasets.MNIST('./data', train=True, download=True, transform=transform)
    dataset2 = datasets.MNIST('./data', train=False, transform=transform)
    train_loader = torch.utils.data.DataLoader(dataset1, **kwargs)
    test_loader = torch.utils.data.DataLoader(dataset2, **kwargs)

    net = get_net().to(device)
    optimizer = optim.Adadelta(net.parameters(), lr=lr)

    scheduler = StepLR(optimizer, step_size=1, gamma=gamma)

    for epoch in range(1, epochs + 1):
        run_train(net, device, train_loader, optimizer)
        run_test(net, device, test_loader)
        scheduler.step()

    examples = enumerate(test_loader)
    batch_idx, (x_test, y_test) = next(examples)

    model = MetadataModel.wrap(net,
                               x_test=x_test,
                               y_test=y_test,
                               source_object=get_net)
    model_metadata = model.model_metadata()

    print(model.model_metadata(as_json=True, indent=4))
    assert model_metadata['inputs'][0]['shape'] == [None, 1, 28, 28]
    assert model_metadata['targets'] == [
        {
            "name": None,
            "sample": 7,
            "type": "int64",
            "shape": None
        }
    ]
    assert model_metadata['outputs'] == [
        {
            "name": None,
            "type": "float64",
            "shape": [
                None,
                10
            ]
        }
    ]

    prediction = model.predict(model_metadata['inputs'][0]['sample'])
    assert prediction.tolist()
    assert model_metadata['metrics']
    assert model_metadata['object_name'] == 'get_net'
    assert model_metadata['object_source']
    assert model_metadata['serialization'] == ModelSerialization.PYTORCH
    assert model_metadata['function_name'] == MiningFunction.CLASSIFICATION
    assert model.save_model('./pytorch-mnist')


def run_train(model, device, train_loader, optimizer):
    import torch.nn.functional as F

    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()


def run_test(model, device, test_loader):
    import torch
    import torch.nn.functional as F

    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))

