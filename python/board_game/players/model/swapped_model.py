class SwappedModel:
    def get_swapped_state(self, state):
        if state.get_cur_player_id() == 2:
            state = state.clone()
            state.swap_players()
            return state, True
        else:
            return state, False
