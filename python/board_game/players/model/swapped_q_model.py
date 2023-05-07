from . import swapped_model

class SwappedQModel(swapped_model.SwappedModel):
    def get_swapped_batch(self, batch):
        swapped_batch = []
        for state, action, target_Q in batch:
            state, swapped = self.get_swapped_state(state)
            if swapped:
                action = state.swap_action(action)
            swapped_batch.append((state, action, target_Q))
        return swapped_batch
