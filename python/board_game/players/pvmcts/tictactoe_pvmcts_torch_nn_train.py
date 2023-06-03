from ...states import tictactoe_state
from . import tictactoe_pvmcts_torch_nn_player
from . import pvmcts_model_train

state = tictactoe_state.create_state()
model = tictactoe_pvmcts_torch_nn_player.create_model(state)

configs = {
    'check_interval': 100,
    'save_model_interval': 10000,
    'episode_num_per_iteration': 2,
    'sim_num': 100,
    'dirichlet_factor': 0.25,
    'dirichlet_alpha': 0.03,
    'replay_memory_size': 1024,
    'batch_num_per_iteration': 2,
    'batch_size': 32,
    'dynamic_learning_rate': 0.001,
    'vloss_factor': 1,
    }

pvmcts_model_train.main(state, model, configs)
