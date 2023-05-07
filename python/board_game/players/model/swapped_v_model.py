from . import swapped_model

class SwappedVModel(swapped_model.SwappedModel):
    def get_swapped_batch(self, batch):
        swapped_batch = []
        for state, target_V in batch:
            state, swapped = self.get_swapped_state(state)
            swapped_batch.append((state, target_V))
        return swapped_batch
