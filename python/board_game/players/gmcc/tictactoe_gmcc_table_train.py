from ...states import tictactoe_state
from . import tictactoe_gmcc_table_player
from . import gmcc_model_train

state = tictactoe_state.TicTacToeState()
model = tictactoe_gmcc_table_player.TicTacToeGMCCTableModel(state)

configs = {
    'check_interval': 100,
    'save_model_interval': 10000,
    'episode_num_per_iteration': 2,
    'dynamic_epsilon': [0.1, 0.1, 4],
    'discount': 0.99,
    'replay_memory_size': 4096,
    'batch_num_per_iteration': 2,
    'batch_size': 32,
    'learning_rate': 0.001,
    }

gmcc_model_train.main(state, model, configs)
