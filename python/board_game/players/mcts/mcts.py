import random
import math

class Node:
    def __init__(self, state, player_id, action, parent):
        self.player_id = player_id # player_id that takes the action
        self.action = action # the action that player takes
        self.N = 0
        self.W = 0
        self.Q = 0

        self.unexpanded_actions = list(state.get_legal_actions(state.get_next_player_id(player_id)))
        self.children = []
        self.parent = parent

    def __str__(self):
        return 'player={}\naction={}\nN={}\nW={}\nQ={}'.format(self.player_id, self.action, self.N, self.W, self.Q)

    def is_fully_expanded(self):
        return not self.unexpanded_actions

    def add_child(self, child):
        self.children.append(child)
        self.unexpanded_actions.remove(child.action)

    def get_uct_value(self):
        return self.get_uct_value_exploitation_factor() + self.get_uct_value_exploration_factor()

    def get_uct_value_exploitation_factor(self):
        return self.Q

    def get_uct_value_exploration_factor(self):
        return math.sqrt(2 * math.log(self.parent.N) / self.N)

    def uct_select_children(self):
        child = max(self.children, key=lambda c: c.get_uct_value())
        return child

    def get_most_visited_child(self):
        child = max(self.children, key=lambda c: c.N)
        return child

    def update(self, V):
        self.N += 1
        self.W += V
        self.Q = self.W / self.N

class MctsTree:
    def __init__(self, root_state, player_id, sim_num):
        self.sim_num = sim_num
        self.root_node = Node(root_state, root_state.get_next_player_id(player_id), None, None)
        self.root_state = root_state.clone()

    def get_action(self, state, player_id):
        assert player_id == self.root_state.get_next_player_id(self.root_node.player_id)

        for sim_id in range(self.sim_num):
            node = self.root_node
            state = self.root_state.clone()

            while not state.is_end() and node.is_fully_expanded():
                node = node.uct_select_children()
                state.do_action(node.player_id, node.action)

            if not state.is_end():
                action = random.choice(node.unexpanded_actions)
                next_player_id = state.get_next_player_id(node.player_id)
                state.do_action(next_player_id, action)
                child = Node(state, next_player_id, action, node)
                node.add_child(child)
                node = child

            player_id = node.player_id
            while not state.is_end():
                player_id = state.get_next_player_id(player_id)
                action = random.choice(state.get_legal_actions(player_id))
                state.do_action(player_id, action)

            result = state.get_result()
            if result > 0:
                V = 1 if result == node.player_id else -1
            else:
                V = 0
            while node:
                node.update(V)
                V = -V
                node = node.parent

        child = self.root_node.get_most_visited_child()
        child.parent = None

        self.root_node = child
        self.root_state.do_action(self.root_node.player_id, self.root_node.action)

        return self.root_node.action
