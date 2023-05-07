from . import swapped_model

class SwappedPModel(swapped_model.SwappedModel):
    def get_swapped_batch(self, batch):
        swapped_batch = []
        for state, action, target_V, factor in batch:
            state, swapped = self.get_swapped_state(state)
            if swapped:
                action = state.swap_action(action)
            swapped_batch.append((state, action, target_V, factor))
        return swapped_batch
