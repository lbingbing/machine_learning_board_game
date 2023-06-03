from ..model import swapped_pv_torch_nn_model

class PVMctsTorchNNModel(swapped_pv_torch_nn_model.SwappedPVTorchNNModel):
    def get_model_algorithm(self):
        return 'pvmcts'
