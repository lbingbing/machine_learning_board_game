from ...states import cchess_state
from . import cchess_gmcc_torch_nn_player
from . import gmcc_model_train

state = cchess_state.create_state()
model = cchess_gmcc_torch_nn_player.create_model(state)

configs = gmcc_model_train.get_default_configs()

gmcc_model_train.main(state, model, configs)
