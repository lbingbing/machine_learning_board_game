from ...states import cchess_state
from . import cchess_gmcc_torch_nn_player
from . import gmcc_model_train

state = cchess_state.create_state()
model = cchess_gmcc_torch_nn_player.create_model(state)

configs = {
    'episode_num_per_iteration': 2,
    'dynamic_epsilon': 0.1,
    'replay_memory_size': 4096,
    'batch_num_per_iteration': 2,
    'batch_size': 32,
    'dynamic_learning_rate': 0.001,
    }

gmcc_model_train.main(state, model, configs)
