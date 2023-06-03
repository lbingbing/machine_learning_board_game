from . import v_table_model
from . import swapped_v_model

class SwappedVTableModel(v_table_model.VTableModel, swapped_v_model.SwappedVModel):
    def __init__(self, game_name, state_dim):
        v_table_model.VTableModel.__init__(self, game_name, state_dim)

    def train(self, batch, learning_rate):
        swapped_batch = self.get_swapped_batch(batch)
        return super().train(swapped_batch, learning_rate)
        
    def get_V(self, state):
        state, swapped = self.get_swapped_state(state)
        return super().get_V(state)
