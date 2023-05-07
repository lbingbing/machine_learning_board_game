from .. import player

class ModelPlayer(player.Player):
    def __init__(self, player_id, state):
        super().__init__(player_id)

        self.model = self.create_model(state)
        assert self.model.exists()
        self.model.load()

    def get_type(self):
        return '{}_{}'.format(self.model.get_model_algorithm(), self.model.get_model_structure())

    def create_model(self, state):
        raise NotImplementedError()

    def get_action(self, state):
        super().get_action(state)
        return self.model.get_action(state)
