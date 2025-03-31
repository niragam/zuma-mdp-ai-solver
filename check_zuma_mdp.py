import zuma
import zuma_mdp_controller
import random

def solve(game: zuma.Game):
    random.seed(game.get_model()['seed'])
    policy = zuma_mdp_controller.Controller(game)
    print('Solving Zuma game:')
    for i in range(game.get_current_state()[3]):
        game.submit_next_action(chosen_action=policy.choose_next_action())
        # print(game.get_current_reward())
    print('Game result:\n\tLine state ->', game.get_current_state()[0], '\n\tReward result->',
          game.get_current_reward())
    game.show_history()
    return game.get_current_reward()


example1 = {
    'chosen_action_prob': {1: 0.6, 2: 0.7, 3: 0.5, 4: 0.9},
    'next_color_dist': {1: 0.1, 2: 0.6, 3: 0.15, 4: 0.15},
    'color_pop_prob': {1: 0.6, 2: 0.7, 3: 0.4, 4: 0.9},
    'color_pop_reward': {'3_pop': {1: 3, 2: 1, 3: 2, 4: 2},
                         'extra_pop': {1: 1, 2: 2, 3: 3, 4: 1}},
    'color_not_finished_punishment': {1: 2, 2: 3, 3: 5, 4: 1},
    'finished_reward': 150,
    'seed': 42}
example2 = {
    'chosen_action_prob': {1: 0.6, 2: 0.7, 3: 0.5, 4: 0.9},
    'next_color_dist': {1: 0.25, 2: 0.25, 3: 0.25, 4: 0.25},
    'color_pop_prob': {1: 0.6, 2: 0.7, 3: 0.4, 4: 0.9},
    'color_pop_reward': {'3_pop': {1: 3, 2: 1, 3: 2, 4: 2},
                         'extra_pop': {1: 1, 2: 2, 3: 3, 4: 1}},
    'color_not_finished_punishment': {1: 2, 2: 3, 3: 5, 4: 1},
    'finished_reward': 150,
    'seed': 42}
example3 = {
    'chosen_action_prob': {1: 1, 2: 1, 3: 1, 4: 1},
    'next_color_dist': {1: 0.1, 2: 0.6, 3: 0.15, 4: 0.15},
    'color_pop_prob': {1: 0.6, 2: 0.7, 3: 0.4, 4: 0.9},
    'color_pop_reward': {'3_pop': {1: 3, 2: 1, 3: 2, 4: 2},
                         'extra_pop': {1: 1, 2: 2, 3: 3, 4: 1}},
    'color_not_finished_punishment': {1: 2, 2: 3, 3: 5, 4: 1},
    'finished_reward': 150,
    'seed': 42}
example4 = {
    'chosen_action_prob': {1: 1, 2: 1, 3: 1, 4: 1},
    'next_color_dist': {1: 0.25, 2: 0.25, 3: 0.25, 4: 0.25},
    'color_pop_prob': {1: 0.6, 2: 0.7, 3: 0.4, 4: 0.9},
    'color_pop_reward': {'3_pop': {1: 3, 2: 1, 3: 2, 4: 2},
                         'extra_pop': {1: 1, 2: 2, 3: 3, 4: 1}},
    'color_not_finished_punishment': {1: 2, 2: 3, 3: 5, 4: 1},
    'finished_reward': 150,
    'seed': 42}


def main():
    # debug_mode = False
    debug_mode = True
    games = []
    game = zuma.create_zuma_game((200, [1, 2, 3, 3, 3, 4, 2, 1, 2, 3, 4, 4], example1, debug_mode))
    games.append(game)
    game = zuma.create_zuma_game((200, [1, 2, 3, 3, 3, 4, 2, 1, 2, 3, 4, 4], example2, debug_mode))
    games.append(game)
    game = zuma.create_zuma_game((200, [1, 2, 3, 3, 3, 4, 2, 1, 2, 3, 4, 4], example3, debug_mode))
    games.append(game)
    game = zuma.create_zuma_game((200, [1, 2, 3, 3, 3, 4, 2, 1, 2, 3, 4, 4], example4, debug_mode))
    games.append(game)
    game = zuma.create_zuma_game((20,  [1, 2, 3, 3, 3, 4, 2, 1, 2, 3, 4, 4], example1, debug_mode))
    games.append(game)
    game = zuma.create_zuma_game((20,  [1, 2, 3, 3, 3, 4, 2, 1, 2, 3, 4, 4], example2, debug_mode))
    games.append(game)
    game = zuma.create_zuma_game((20,  [1, 2, 3, 3, 3, 4, 2, 1, 2, 3, 4, 4], example3, debug_mode))
    games.append(game)
    game = zuma.create_zuma_game((20,  [1, 2, 3, 3, 3, 4, 2, 1, 2, 3, 4, 4], example4, debug_mode))
    games.append(game)
    game = zuma.create_zuma_game((20, [1, 1], example1, debug_mode))
    games.append(game)
    game = zuma.create_zuma_game((20, [1, 1], example2, debug_mode))
    games.append(game)
    game = zuma.create_zuma_game((20, [1, 1], example3, debug_mode))
    games.append(game)
    game = zuma.create_zuma_game((20, [1, 1], example4, debug_mode))
    games.append(game)
    results = [solve(game) for game in games]
    print('Results:', results)
    print('Average:', sum(results) / len(results))


if __name__ == "__main__":
    main()
