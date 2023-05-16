import functools
import operator

import torch

from . import gmcc_torch_nn_model
from ..model import model_player

class Network(torch.nn.Module):
    def __init__(self, state_shape, action_dim):
        super().__init__()
        sequential1 = torch.nn.Sequential(
            torch.nn.Conv2d(state_shape[1], 64, 3, padding=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(64, 64, 3, padding=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(64, 64, 3, padding=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(64, 64, 3, padding=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(64, 64, 3, padding=1),
            torch.nn.ReLU(),
            )
        dim1 = functools.reduce(operator.mul, sequential1(torch.rand(*state_shape)).shape)
        sequential2 = torch.nn.Sequential(
            torch.nn.Flatten(),
            torch.nn.Linear(dim1, action_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(action_dim, action_dim),
            )
        self.layers = torch.nn.Sequential(
            sequential1,
            sequential2,
            )

    def forward(self, x):
        return self.layers(x)

class CChessGMCCTorchNNModel(gmcc_torch_nn_model.GMCCTorchNNModel):
    def create_network(self, state):
        return Network(state.get_state_numpy_shape(), state.get_action_dim())

class CChessGMCCTorchNNPlayer(model_player.ModelPlayer):
    def create_model(self, state):
        return CChessGMCCTorchNNModel(state)
