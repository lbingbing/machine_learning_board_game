from ...states import tictactoe_state
from . import tictactoe_gmcc_torch_nn_player
from . import gmcc_model_train

state = tictactoe_state.create_state()
model = tictactoe_gmcc_torch_nn_player.create_model(state)

configs = gmcc_model_train.get_default_configs()

gmcc_model_train.main(state, model, configs)
