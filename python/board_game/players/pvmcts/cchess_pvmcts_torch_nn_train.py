from ...states import cchess_state
from . import cchess_pvmcts_torch_nn_player
from . import pvmcts_model_train

state = cchess_state.create_state()
model = cchess_pvmcts_torch_nn_player.create_model(state)

configs = pvmcts_model_train.get_default_configs()

pvmcts_model_train.main(state, model, configs)
