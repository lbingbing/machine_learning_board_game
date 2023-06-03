from ...states import gomoku_state
from . import gomoku_pvmcts_torch_nn_player
from . import pvmcts_model_train

state = gomoku_state.create_state()
model = gomoku_pvmcts_torch_nn_player.create_model(state)

configs = {
    'check_interval': 100,
    'save_model_interval': 10000,
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
