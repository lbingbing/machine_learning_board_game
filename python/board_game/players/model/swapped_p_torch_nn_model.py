from . import p_torch_nn_model
from . import swapped_p_model

class SwappedPTorchNNModel(p_torch_nn_model.PTorchNNModel, swapped_p_model.SwappedPModel):
    def train(self, batch, learning_rate):
        swapped_batch = self.get_swapped_batch(batch)
        return super().train(swapped_batch, learning_rate)

    def get_P_logits_t(self, state):
        assert state.get_cur_player_id() == 1
        return super().get_P_logits_t(state)

    def get_max_P_logit(self, state):
        state, swapped = self.get_swapped_state(state)
        return super().get_max_P_logit(state)

    def get_P_t(self, state):
        assert state.get_cur_player_id() == 1
        return super().get_P_t(state)

    def get_legal_P_t(self, state):
        assert state.get_cur_player_id() == 1
        return super().get_legal_P_t(state)

    def get_max_P(self, state):
        state, swapped = self.get_swapped_state(state)
        return super().get_max_P(state)

    def get_action(self, state):
        state, swapped = self.get_swapped_state(state)
        action = super().get_action(state)
        if swapped:
            action = state.swap_action(action)
        return action
