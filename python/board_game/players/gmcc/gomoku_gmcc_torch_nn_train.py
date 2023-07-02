from ...states import gomoku_state
from . import gomoku_gmcc_torch_nn_player
from . import gmcc_model_train

state = gomoku_state.create_state()
model = gomoku_gmcc_torch_nn_player.create_model(state)

configs = gmcc_model_train.get_default_configs()

gmcc_model_train.main(state, model, configs)
