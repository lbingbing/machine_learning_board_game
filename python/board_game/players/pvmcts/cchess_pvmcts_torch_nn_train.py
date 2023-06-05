from ...states import cchess_state
from . import cchess_pvmcts_torch_nn_player
from . import pvmcts_model_train

state = cchess_state.create_state()
model = cchess_pvmcts_torch_nn_player.create_model(state)

configs = {
    'episode_num_per_iteration': 2,
    'sim_num': 1000,
    'dirichlet_factor': 0.25,
    'dirichlet_alpha': 0.03,
    'replay_memory_size': 4096,
    'batch_num_per_iteration': 2,
    'batch_size': 32,
    'dynamic_learning_rate': 0.001,
    'vloss_factor': 1,
    }

pvmcts_model_train.main(state, model, configs)
