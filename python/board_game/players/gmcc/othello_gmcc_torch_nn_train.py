from ...states import othello_state
from . import othello_gmcc_torch_nn_player
from . import gmcc_model_train

state = othello_state.create_state()
model = othello_gmcc_torch_nn_player.create_model(state)

configs = gmcc_model_train.get_default_configs()

gmcc_model_train.main(state, model, configs)
