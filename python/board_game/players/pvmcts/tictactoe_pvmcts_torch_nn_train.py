from ...states import tictactoe_state
from . import tictactoe_pvmcts_torch_nn_player
from . import pvmcts_model_train

state = tictactoe_state.create_state()
model = tictactoe_pvmcts_torch_nn_player.create_model(state)

configs = pvmcts_model_train.get_default_configs()

pvmcts_model_train.main(state, model, configs)
