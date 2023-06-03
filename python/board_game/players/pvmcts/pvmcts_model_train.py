import argparse
import itertools

from . import pvmcts
from ..utils import train_utils
from ..utils import replay_memory
from ..utils import train_flags

def sample(state, model, rmemory, configs):
    model.set_training(False)

    episode_num_per_iteration = configs['episode_num_per_iteration']
    sim_num = configs['sim_num']
    dirichlet_factor = configs['dirichlet_factor']
    dirichlet_alpha = configs['dirichlet_alpha']

    rmemory.resize(configs['replay_memory_size'])

    scores = [0] * 3
    action_nums = []
    for episode_id in range(episode_num_per_iteration):
        samples = []
        state.reset()
        pvmcts_tree = pvmcts.PVMctsTree(model, state, 1, sim_num, is_training=True, dirichlet_factor=dirichlet_factor, dirichlet_alpha=dirichlet_alpha)
        for t, player_id in zip(itertools.count(), itertools.cycle((1, 2))):
            action, P = pvmcts_tree.get_action(state, player_id)
            samples.append((state.clone(), P))
            state.do_action(player_id, action)
            result = state.get_result()
            is_end = state.is_end(result)
            if is_end:
                break
        scores[result] += 1
        action_nums.append(state.get_action_num())
        if result == 1:
            Vs = (1, -1)
        elif result == 2:
            Vs = (-1, 1)
        else:
            Vs = (0, 0)
        for (S, P), V in zip(samples, itertools.cycle(Vs)):
            rmemory.record((S, P, 1, V))
    return scores, action_nums

def train(model, rmemory, configs, iteration_id):
    model.set_training(True)

    batch_num_per_iteration = configs['batch_num_per_iteration']
    batch_size = configs['batch_size']
    learning_rate = train_utils.get_dynamic_learning_rate(iteration_id, configs['dynamic_learning_rate'])
    vloss_factor = configs['vloss_factor']

    plosses = []
    vlosses = []
    for i in range(batch_num_per_iteration):
        batch = rmemory.sample(batch_size)
        ploss, vloss = model.train(batch, learning_rate, vloss_factor)
        plosses.append(ploss)
        vlosses.append(vloss)
    return plosses, vlosses

def main(state, model, configs):
    parser = argparse.ArgumentParser('train {} pvmcts model'.format(state.get_name()))
    train_utils.add_train_arguments(parser)
    args = parser.parse_args()

    if not train_flags.check_and_update_train_configs(model.get_model_path(), configs):
        print('train configs:')
        train_flags.print_train_configs(configs)

    check_interval = configs['check_interval']
    save_model_interval = configs['save_model_interval']

    train_utils.init_model(model, args.device)

    rmemory = replay_memory.ReplayMemory(configs['replay_memory_size'])

    plosses = []
    vlosses = []
    scores = [0, 0, 0]
    action_nums = []
    for iteration_id in itertools.count(1):
        scores1, action_nums1 = sample(state, model, rmemory, configs)
        plosses1, vlosses1 = train(model, rmemory, configs, iteration_id)
        plosses += plosses1
        vlosses += vlosses1
        for i, e in enumerate(scores1):
            scores[i] += e
        action_nums += action_nums1
        need_check = iteration_id % check_interval == 0
        if need_check:
            state.reset()
            model.set_training(False)
            V1 = model.get_V(state)
            legal_P_logit_range1 = model.get_legal_P_logit_range(state)
            legal_P_range1 = model.get_legal_P_range(state)
            action = model.get_action(state)
            state.do_action(1, action)
            V2 = model.get_V(state)
            legal_P_logit_range2 = model.get_legal_P_logit_range(state)
            legal_P_range2 = model.get_legal_P_range(state)
            avg_ploss = sum(plosses) / len(plosses)
            avg_vloss = sum(vlosses) / len(vlosses)
            avg_action_num = sum(action_nums) / len(action_nums)
            print('{} iter: {} ploss: {:.2f} vloss: {:.2f} Vs: {:.2f} {:.2f} P_logit_ranges: [{:.2f}, {:.2f}] [{:.2f}, {:.2f}] P_ranges: [{:.2f}, {:.2f}] [{:.2f}, {:.2f}] p1/p2/draw: {}/{}/{} action_num: {:.2f}'.format(train_utils.get_current_time_str(), iteration_id, avg_ploss, avg_vloss, V1, V2, *legal_P_logit_range1, *legal_P_logit_range2, *legal_P_range1, *legal_P_range2, scores[1], scores[2], scores[0], avg_action_num))
            plosses.clear()
            vlosses.clear()
            scores = [0, 0, 0]
            action_nums.clear()
            train_flags.check_and_update_train_configs(model.get_model_path(), configs)
        if iteration_id % save_model_interval == 0 or (need_check and train_flags.check_and_clear_save_model_flag_file(model.get_model_path())):
            model.save()
            print('model {} saved'.format(model.get_model_path()))
        if need_check and train_flags.check_and_clear_stop_train_flag_file(model.get_model_path()):
            print('stopped')
            break
        if args.iteration_num > 0 and iteration_id >= args.iteration_num:
            break