from ...states import tictactoe_state
from . import tictactoe_pvmcts_table_player
from . import pvmcts_model_train

state = tictactoe_state.TicTacToeState()
model = tictactoe_pvmcts_table_player.create_model(state)

configs = pvmcts_model_train.get_default_configs()

pvmcts_model_train.main(state, model, configs)
