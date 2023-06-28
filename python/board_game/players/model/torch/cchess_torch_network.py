import torch

from . import torch_network

class Backbone(torch.nn.Module):
    def __init__(self, state_shape, action_dim):
        super().__init__()

        channel_num = ((int((state_shape[2] * state_shape[3]) ** 0.5) + 15) // 16) * 16
        sequential1 = torch.nn.Sequential(
            torch.nn.Conv2d(state_shape[1], channel_num, 3, padding=1),
            torch_network.ConvResidualBlock(channel_num, 3),
            torch_network.ConvResidualBlock(channel_num, 3),
            torch_network.ConvResidualBlock(channel_num, 3),
            torch_network.ConvResidualBlock(channel_num, 3),
            torch.nn.Flatten(),
            )
        dim = torch_network.get_output_dim(sequential1, (2, *state_shape[1:])) // 2
        sequential2 = torch.nn.Sequential(
            torch.nn.Linear(dim, 64),
            torch.nn.ReLU(),
            torch_network.FcResidualBlock(64),
            torch_network.FcResidualBlock(64),
            torch_network.FcResidualBlock(64),
            torch_network.FcResidualBlock(64),
            )
        self.layers = torch.nn.Sequential(
            sequential1,
            sequential2,
            )

    def forward(self, x):
        return self.layers(x)

class QNetwork(torch_network.QNetwork):
    def __init__(self, state_shape, action_dim):
        super().__init__(state_shape, action_dim, Backbone(state_shape, action_dim))

class PNetwork(torch_network.PNetwork):
    def __init__(self, state_shape, action_dim):
        super().__init__(state_shape, action_dim, Backbone(state_shape, action_dim))

class PVNetwork(torch_network.PVNetwork):
    def __init__(self, state_shape, action_dim):
        super().__init__(state_shape, action_dim, Backbone(state_shape, action_dim))
