from ...states import gomoku_state
from . import gomoku_pvmcts_torch_nn_player
from . import pvmcts_model_train

state = gomoku_state.create_state()
model = gomoku_pvmcts_torch_nn_player.create_model(state)

configs = pvmcts_model_train.get_default_configs()

pvmcts_model_train.main(state, model, configs)
