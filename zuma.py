import random
import time
import re
from pprint import pprint


class Game:
    """Game class --- presents a Zuma game played for given number of steps."""

    def __init__(self, max_steps, line, model, debug=False):
        """Initialize the Game class.
        max_steps - represents the number of steps the game is run
        line - the initial state of the line
        probabilities - the transition probabilities"""
        self._max_steps = max_steps
        self._line = line
        self._model = model
        self._debug = debug
        if self._debug:
            self._history = list()
        self._steps = 0
        self._current_ball = None
        self._reward = 0
        self._chosen_action_prob = model['chosen_action_prob']
        self._next_color_dist = model['next_color_dist']
        self._color_pop_prob = model['color_pop_prob']
        self._color_pop_reward = model['color_pop_reward']
        self._color_not_finished_punishment = model['color_not_finished_punishment']
        self._finished_reward = model['finished_reward']
        self._seed = model['seed']
        random.seed(self._seed)
        if sum(self._next_color_dist.values()) != 1:
            raise ValueError("Next color distribution doesn't add to 1.")

    def get_ball(self):
        """ Generates new ball or
        returns the ball that hadn't been used yet from previous function call.
        Uses the distribution given in the game model.
        :return: scalar (ball)
        """
        if self._current_ball is not None:
            return self._current_ball
        r_num = random.random()
        sum_count = 0
        for k, v in self._next_color_dist.items():
            if r_num < v + sum_count:
                # self._ball_count += 1
                self._current_ball = k
                return k
            else:
                sum_count += v

    def get_current_state(self):
        """
        Tuple of the current state of the game.
        :return: list (current line of balls), scalar (ball to be thrown),
        scalar (steps passed), scalar (number of steps program will run)
        """
        if self._current_ball is None:
            self.get_ball()
        return self._line, self._current_ball, self._steps, self._max_steps

    def get_current_reward(self):
        """
        Current reward of the game
        :return: scalar
        """
        return self._reward

    def get_model(self):
        """
        Dictionary of detailing the model of the game.
        :return: dictionary (detailed in the pdf)
        """
        return self._model

    def _remove_group(self, line, addition, reward=0):
        """
        removes groups of balls according to their pop probability.
        :param line: list (sequence of balls to check for pops)
        :param addition: scalar (index of ball insertion)
        :param reward: scalar (reward of current insertion)
        :return: list (updated sequence of balls), scalar (reward of insertion)
        """
        burstable = re.finditer(r'1{3,}|2{3,}|3{3,}|4{3,}', ''.join([str(i) for i in line]))
        new_reward = reward
        new_line = line.copy()
        for group in burstable:
            if addition in range(group.span()[0], group.span()[1]):
                r_num = random.random()
                if r_num < self._color_pop_prob[line[group.start()]]:
                    new_reward += (self._color_pop_reward['3_pop'][line[group.start()]] +
                                   (group.span()[1] - group.span()[0] - 3) *
                                   self._color_pop_reward['extra_pop'][line[group.start()]])
                    new_line = line[:group.span()[0]] + line[group.span()[1]:]
                    if self._debug:
                        self._history[-1].append(f'removed color group {line[group.start()]} {group.span()}, prob: {r_num:1.4}, updated reward: {self._reward + new_reward}')
                    addition = group.span()[0]
                break
        if new_reward != reward:
            new_line, new_reward = self._remove_group(new_line, addition, new_reward)
        return new_line, new_reward

    def _finished_game(self):
        """
        Rewards or punishes for any leftovers in the line
        """
        if len(self._line) == 0:
            self._reward += self._finished_reward
            if self._debug:
                self._history.append(f'Finished game successfully, final reward: {self._reward}')
        else:
            for k, v in self._color_not_finished_punishment.items():
                num_of_ball = self._line.count(k)
                self._reward -= num_of_ball * v
                if self._debug:
                    self._history.append(f'{k} color has {num_of_ball} not popped, updated reward: {self._reward}')
            if self._debug:
                self._history.append(f'Finished game unsuccessfully, final reward: {self._reward}')

    def submit_next_action(self, chosen_action):
        """
        Takes chosen action from user and updates the game from its consequences.
        :param chosen_action: scalar (index of where to shoot the current ball)
        """
        self.get_ball()
        r_num = random.random()
        if r_num < self._chosen_action_prob[self._current_ball]:
            action = chosen_action
        else:
            action = random.choice([i for i in range(-1, len(self._line) + 1) if i != chosen_action])
        if self._debug:
            submit_result = list()
            submit_result.append(f'step {self._steps}, added ball: {self._current_ball}, prob: {r_num:1.4}, index: {action}')
            self._history.append(submit_result)
        if action != -1:
            self._line.insert(action, self._current_ball)
            self._line, add_reward = self._remove_group(self._line, action)
            self._reward += add_reward
        self._steps += 1
        self._current_ball = None
        if self._steps == self._max_steps:
            self._finished_game()

    def show_history(self):
        """
        Debug function used to see the probabilities and the process of the game.
        """
        if self._debug:
            print('History:')
            pprint(self._history)


def create_zuma_game(game):
    print('--------DEBUG MODE--------')
    print('<< create zuma game >>')
    print('<maximize R on>', game[1])
    print('in', game[0], 'steps')
    print('under these conditions:')
    pprint(game[2])
    return Game(*game)

