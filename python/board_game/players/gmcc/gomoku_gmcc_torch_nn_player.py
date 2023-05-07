import functools
import operator

import torch

from . import gmcc_torch_nn_model
from ..model import model_player

class Network(torch.nn.Module):
    def __init__(self, state):
        super().__init__()
        sequential1 = torch.nn.Sequential(
            torch.nn.Conv2d(state.get_state_numpy_shape()[1], 64, 3, padding=2),
            torch.nn.ReLU(),
            torch.nn.Conv2d(64, 64, 3, padding=2),
            torch.nn.ReLU(),
            torch.nn.Conv2d(64, 64, 3, padding=2),
            torch.nn.ReLU(),
            torch.nn.Conv2d(64, 64, 3, padding=2),
            torch.nn.ReLU(),
            torch.nn.Conv2d(64, 64, 3, padding=2),
            torch.nn.ReLU(),
            )
        dim1 = functools.reduce(operator.mul, sequential1(torch.rand(*state.get_state_numpy_shape())).shape)
        sequential2 = torch.nn.Sequential(
            torch.nn.Flatten(),
            torch.nn.Linear(dim1, state.get_action_dim()),
            torch.nn.ReLU(),
            torch.nn.Linear(state.get_action_dim(), state.get_action_dim()),
            )
        self.layers = torch.nn.Sequential(
            sequential1,
            sequential2,
            )

    def forward(self, x):
        return self.layers(x)

class GomokuGMCCTorchNNModel(gmcc_torch_nn_model.GMCCTorchNNModel):
    def create_network(self, state):
        return Network(state)

class GomokuGMCCTorchNNPlayer(model_player.ModelPlayer):
    def create_model(self, state):
        return GomokuGMCCTorchNNModel(state)
