import argparse
import sys
import itertools

from ..players import player
from . import utils

def print_progress(results, game_num):
    print('\rpl/p2/draw/total: {}/{}/{}/{}'.format(results[1], results[2], results[0], game_num), end='', file=sys.stderr, flush=True)

def print_finish():
    print(file=sys.stderr)

def main(state, create_player):
    parser = argparse.ArgumentParser('{} game regression'.format(state.get_name()))
    player.add_player_options(parser)
    parser.add_argument('game_num', type=int, help='game num')
    utils.add_game_options(parser)
    args = parser.parse_args()

    p1 = create_player(state, args.player_type1, 1)
    p2 = create_player(state, args.player_type2, 2)

    results = [0, 0, 0]
    print_progress(results, args.game_num)
    for game_id in range(args.game_num):
        state.reset()
        actions = []
        for step_id, p in enumerate(itertools.cycle((p1, p2))):
            action = p.get_action(state)
            state.do_action(p.get_player_id(), action)
            actions.append(action)
            result = state.get_result()
            if result >= 0:
                results[result] += 1
                if args.save_transcript:
                    transcript_player.save_transcript('{}.{}.trans'.format(state.get_name(), game_id), actions)
                break
        print_progress(results, args.game_num)
    print_finish()
