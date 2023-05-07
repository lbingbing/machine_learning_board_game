from . import q_torch_nn_model
from . import swapped_q_model

class SwappedQTorchNNModel(q_torch_nn_model.QTorchNNModel, swapped_q_model.SwappedQModel):
    def train(self, batch, learning_rate):
        swapped_batch = self.get_swapped_batch(batch)
        return super().train(swapped_batch, learning_rate)

    def get_Q_t(self, state):
        assert state.get_cur_player_id() == 1
        return super().get_Q_t(state)

    def get_action_Q(self, state, action):
        state, swapped = self.get_swapped_state(state)
        if swapped:
            action = state.swap_action(action)
        return super().get_action_Q(state, action)

    def get_legal_Q_t(self, state):
        assert state.get_cur_player_id() == 1
        return super().get_legal_Q_t(state)

    def get_max_Q(self, state):
        state, swapped = self.get_swapped_state(state)
        return super().get_max_Q(state)

    def get_opt_action(self, state):
        state, swapped = self.get_swapped_state(state)
        action = super().get_opt_action(state)
        if swapped:
            action = state.swap_action(action)
        return action
