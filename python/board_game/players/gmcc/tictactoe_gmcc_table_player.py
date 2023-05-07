from . import gmcc_table_model
from ..model import model_player

class TicTacToeGMCCTableModel(gmcc_table_model.GMCCTableModel):
    pass

class TicTacToeGMCCTablePlayer(model_player.ModelPlayer):
    def create_model(self, state):
        return TicTacToeGMCCTableModel(state)
