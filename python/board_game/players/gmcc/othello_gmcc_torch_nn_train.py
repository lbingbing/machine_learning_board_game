from ...states import othello_state
from . import othello_gmcc_torch_nn_player
from . import gmcc_model_train

state = othello_state.create_state()
model = othello_gmcc_torch_nn_player.OthelloGMCCTorchNNModel(state)

configs = {
    'check_interval': 100,
    'save_model_interval': 10000,
    'episode_num_per_iteration': 2,
    'dynamic_epsilon': [0.1, 0.1, 32],
    'discount': 0.99,
    'replay_memory_size': 4096,
    'batch_num_per_iteration': 2,
    'batch_size': 32,
    'learning_rate': 0.001,
    }

gmcc_model_train.main(state, model, configs)