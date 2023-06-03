from . import v_torch_nn_model
from . import v_model

class SwappedVTorchNNModel(v_torch_nn_model.VTorchNNModel, swapped_v_model.SwappedVModel):
    def __init__(self, game_name, network):
        v_torch_nn_model.VTorchNNModel.__init__(self, game_name, network)

    def train(self, batch, learning_rate):
        swapped_batch = self.get_swapped_batch(batch)
        return super().train(swapped_batch, learning_rate)

    def get_V(self, state):
        state, swapped = self.get_swapped_state(state)
        return super().get_V(state)
