from ..model import swapped_q_torch_nn_model

class GMCCTorchNNModel(swapped_q_torch_nn_model.SwappedQTorchNNModel):
    def get_model_algorithm(self):
        return 'gmcc'
