import random
import math

import numpy as np

class Node:
    def __init__(self, player_id, action, P, parent):
        self.player_id = player_id # player_id that takes the action
        self.action = action # the action that player takes
        self.N = 0
        self.W = 0
        self.Q = 0
        self.P = P

        self.children = []
        self.parent = parent

    def __str__(self):
        return 'player={}\naction={}\nN={}\nW={}\nQ={}\nP={}'.format(self.player_id, self.action, self.N, self.W, self.Q, self.P)

    def is_leaf(self):
        return not self.children

    def get_uct_value(self):
        return self.get_uct_value_exploitation_factor() + self.get_uct_value_exploration_factor()

    def get_uct_value_exploitation_factor(self):
        return self.Q

    def get_uct_value_exploration_factor(self):
        return self.P * math.sqrt(self.parent.N) / (1 + self.N)

    def uct_select_children(self):
        child = max(self.children, key=lambda c: c.get_uct_value())
        return child

    def expand(self, player_id, actions, legal_P):
        for action, P in zip(actions, legal_P):
            child = Node(player_id, action, P, self)
            self.children.append(child)

    def update(self, V):
        self.N += 1
        self.W += V
        self.Q = self.W / self.N

class PVMctsTree:
    def __init__(self, model, root_state, player_id, sim_num, is_training, dirichlet_factor, dirichlet_alpha):
        self.model = model
        self.sim_num = sim_num
        self.is_training = is_training
        self.temperature = 1 if self.is_training else 1 / 3
        self.dirichlet_factor = dirichlet_factor
        self.dirichlet_alpha = dirichlet_alpha
        self.root_node = Node(root_state.get_next_player_id(player_id), None, None, None)
        self.root_state = root_state.clone()

    def get_action(self, state, player_id):
        assert player_id == self.root_state.get_next_player_id(self.root_node.player_id)

        for sim_id in range(self.sim_num):
            node = self.root_node
            state = self.root_state.clone()

            while not node.is_leaf():
                node = node.uct_select_children()
                state.do_action(node.player_id, node.action)

            result = state.get_result()
            if result >= 0:
                V = 1 if result > 0 else 0
            else:
                player_id = state.get_next_player_id(node.player_id)
                legal_actions = state.get_legal_actions(player_id)
                legal_action_indexes = [state.action_to_action_index(action) for action in legal_actions]
                P = self.model.get_P(state)
                P_m = np.array(P, dtype=np.float32)
                legal_P_m = P_m[legal_action_indexes]
                V = self.model.get_V(state)
                V = -V
                if self.is_training and not node.parent:
                    legal_P_m = legal_P_m * (1 - self.dirichlet_factor) + np.random.dirichlet(np.ones_like(legal_P_m).astype(dtype=np.float32) * self.dirichlet_alpha) * self.dirichlet_factor
                node.expand(player_id, legal_actions, legal_P_m.tolist())

            while node:
                node.update(V)
                V = -V
                node = node.parent

        Ns_m = np.array([c.N for c in self.root_node.children], dtype=np.int64)
        Ns_m = np.power(Ns_m, 1 / self.temperature)
        legal_P_m = Ns_m / np.sum(Ns_m)

        P_m = np.zeros(state.get_action_dim())
        action_indexes = [self.root_state.action_to_action_index(c.action) for c in self.root_node.children]
        P_m[action_indexes] = legal_P_m

        child = np.random.choice(self.root_node.children, p=legal_P_m)
        child.parent = None

        self.root_node = child
        self.root_state.do_action(self.root_node.player_id, self.root_node.action)

        return self.root_node.action, P_m.tolist()
