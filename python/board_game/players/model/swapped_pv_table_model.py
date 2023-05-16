from . import pv_table_model
from . import swapped_pv_model

class SwappedPVTableModel(pv_table_model.PVTableModel, swapped_pv_model.SwappedPVModel):
    def __init__(self, state):
        pv_table_model.PVTableModel.__init__(self, state)

    def train(self, batch, learning_rate):
        swapped_batch = self.get_swapped_batch(batch)
        return super().train(swapped_batch, learning_rate)
        
    def get_V(self, state):
        state, swapped = self.get_swapped_state(state)
        return super().get_V(state)
        
    def get_P_logits_m(self, state):
        assert state.get_cur_player_id() == 1
        return super().get_P_logits_m(state)

    def get_P_logit_range(self, state):
        state, swapped = self.get_swapped_state(state)
        return super().get_P_logit_range(state)

    def get_P_m(self, state):
        assert state.get_cur_player_id() == 1
        return super().get_P_m(state)

    def get_legal_P_m(self, state):
        assert state.get_cur_player_id() == 1
        return super().get_legal_P_m(state)

    def get_legal_P(self, state):
        state, swapped = self.get_swapped_state(state)
        legal_P = super().get_legal_P(state)
        if swapped:
            legal_P = [legal_P[action_index] for action_index in state.get_swap_action_index_table()]
        return legal_P

    def get_P_range(self, state):
        state, swapped = self.get_swapped_state(state)
        return super().get_P_range(state)

    def get_action(self, state):
        state, swapped = self.get_swapped_state(state)
        action = super().get_action(state)
        if swapped:
            action = state.swap_action(action)
        return action
