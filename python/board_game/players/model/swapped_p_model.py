from . import swapped_model

class SwappedPModel(swapped_model.SwappedModel):
    def get_swapped_batch(self, batch):
        swapped_batch = []
        for state, target_P, factor in batch:
            state, swapped = self.get_swapped_state(state)
            if swapped:
                target_P = self.get_swapped_P(state, target_P)
            swapped_batch.append((state, target_P, factor))
        return swapped_batch

    def get_swapped_P(self, state, P):
        return [P[action_index] for action_index in state.get_swapped_action_index_table()]
