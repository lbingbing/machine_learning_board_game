import os
import platform
import subprocess
import json

os.chdir('machine_learning_board_game_release')

def run(cmd, timeout=None):
    if platform.system() in ('Linux', 'Darwin'):
        os.environ['PATH'] = os.environ.get('PATH', '') + ':.'
    print(' '.join(cmd))
    res = subprocess.run(cmd, timeout=timeout)
    return res.returncode == 0

def create_train_configs_update_flag_file():
    configs = {
        'exploring_starts': [0.5, 0],
        'sim_num': 10,
        }
    with open('flag.train_configs_update', 'w') as f:
        json.dump(configs, f, indent=4)

create_train_configs_update_flag_file()

def test_tictactoe_game_regression_random():
    assert run(['python', '-m', 'board_game.games.tictactoe_game_regression', 'random', 'random', '100'])

def test_gomoku_game_regression_random():
    assert run(['python', '-m', 'board_game.games.gomoku_game_regression', 'random', 'random', '100'])

def test_othello_game_regression_random():
    assert run(['python', '-m', 'board_game.games.othello_game_regression', 'random', 'random', '100'])

def test_cchess_game_regression_random():
    assert run(['python', '-m', 'board_game.games.cchess_game_regression', 'random', 'random', '100'])

def test_tictactoe_game_regression_mcts():
    assert run(['python', '-m', 'board_game.games.tictactoe_game_regression', 'random', 'random', '1'])

def test_gomoku_game_regression_mcts():
    assert run(['python', '-m', 'board_game.games.gomoku_game_regression', 'random', 'random', '1'])

def test_othello_game_regression_mcts():
    assert run(['python', '-m', 'board_game.games.othello_game_regression', 'random', 'random', '1'])

def test_cchess_game_regression_mcts():
    assert run(['python', '-m', 'board_game.games.cchess_game_regression', 'random', 'random', '1'])

def test_tictactoe_gmcc_table_train():
    assert run(['python', '-m', 'board_game.players.gmcc.tictactoe_gmcc_table_train', '--iteration_num', '5'])

def test_tictactoe_gmcc_torch_nn_train():
    assert run(['python', '-m', 'board_game.players.gmcc.tictactoe_gmcc_torch_nn_train', '--iteration_num', '5'])

def test_gomoku_gmcc_torch_nn_train():
    assert run(['python', '-m', 'board_game.players.gmcc.gomoku_gmcc_torch_nn_train', '--iteration_num', '5'])

def test_othello_gmcc_torch_nn_train():
    assert run(['python', '-m', 'board_game.players.gmcc.othello_gmcc_torch_nn_train', '--iteration_num', '5'])

def test_cchess_gmcc_torch_nn_train():
    assert run(['python', '-m', 'board_game.players.gmcc.cchess_gmcc_torch_nn_train', '--iteration_num', '5'])

def test_tictactoe_pvmcts_table_train():
    assert run(['python', '-m', 'board_game.players.pvmcts.tictactoe_pvmcts_table_train', '--iteration_num', '5'])

def test_tictactoe_pvmcts_torch_nn_train():
    assert run(['python', '-m', 'board_game.players.pvmcts.tictactoe_pvmcts_torch_nn_train', '--iteration_num', '5'])

def test_gomoku_pvmcts_torch_nn_train():
    assert run(['python', '-m', 'board_game.players.pvmcts.gomoku_pvmcts_torch_nn_train', '--iteration_num', '5'])

def test_othello_pvmcts_torch_nn_train():
    assert run(['python', '-m', 'board_game.players.pvmcts.othello_pvmcts_torch_nn_train', '--iteration_num', '5'])

def test_cchess_pvmcts_torch_nn_train():
    assert run(['python', '-m', 'board_game.players.pvmcts.cchess_pvmcts_torch_nn_train', '--iteration_num', '5'])
