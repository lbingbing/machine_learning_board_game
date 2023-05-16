import torch

from . import gmcc_torch_nn_model
from ..model import model_player

class Network(torch.nn.Module):
    def __init__(self, state_shape, action_dim):
        super().__init__()
        dim1 = 2 ** action_dim
        self.layers = torch.nn.Sequential(
            torch.nn.Flatten(),
            torch.nn.Linear(action_dim, dim1),
            torch.nn.ReLU(),
            torch.nn.Linear(dim1, dim1),
            torch.nn.ReLU(),
            torch.nn.Linear(dim1, action_dim),
            )

    def forward(self, x):
        return self.layers(x)

class TicTacToeGMCCTorchNNModel(gmcc_torch_nn_model.GMCCTorchNNModel):
    def create_network(self, state):
        return Network(state.get_state_numpy_shape(), state.get_action_dim())

class TicTacToeGMCCTorchNNPlayer(model_player.ModelPlayer):
    def create_model(self, state):
        return TicTacToeGMCCTorchNNModel(state)
