from . import player

def create_player(state, player_type, player_id):
    p = None
    if player_type == player.HUMAN_PLAYER:
        from .human import human_player
        p = human_player.HumanPlayer(player_id)
    elif player_type == player.RANDOM_PLAYER:
        from .random import random_player
        p = random_player.RandomPlayer(player_id)
    elif player_type == player.MCTS_PLAYER:
        from .mcts import mcts_player
        p = mcts_player.MctsPlayer(player_id, 1000)
    elif player_type == player.GMCCTRL_TORCH_NN_PLAYER:
        from .gmcc import gomoku_gmcc_torch_nn_player
        p = gomoku_gmcc_torch_nn_player.GomokuGMCCTorchNNPlayer(player_id, state)
    else:
        assert False
    return p