import copy

id = ["311319313"]

class Controller:
    def __init__(self, game):
        self.original_game = game
        self.model = game.get_model()
        self.cache = {}

    def _simulate_pop(self, line, ball, pos):
        if tuple(line + [ball, pos]) in self.cache:
            return self.cache[tuple(line + [ball, pos])]
            
        test_line = line[:pos] + [ball] + line[pos:]
        # Find all potential sequences of same color
        sequences = []
        current_seq = [0, 0, test_line[0]]
        
        for i, color in enumerate(test_line):
            if color == current_seq[2]:
                current_seq[1] = i + 1
            else:
                if current_seq[1] - current_seq[0] >= 3:
                    sequences.append(current_seq.copy())
                current_seq = [i, i + 1, color]
                
        if current_seq[1] - current_seq[0] >= 3:
            sequences.append(current_seq)
            
        result = []
        for seq in sequences:
            if pos in range(seq[0], seq[1]):
                result.append((seq[2], seq[1] - seq[0]))
                
        self.cache[tuple(line + [ball, pos])] = result
        return result

    def _evaluate_position(self, line, pos, ball, remaining_steps, max_steps):
        if pos == -1:
            return -100 if remaining_steps > 5 else -20

        score = 0
        success_prob = self.model['chosen_action_prob'][ball]
        pop_prob = self.model['color_pop_prob'][ball]
        
        # Analyze potential pops
        potential_pops = self._simulate_pop(line, ball, pos)
        for color, length in potential_pops:
            base_reward = self.model['color_pop_reward']['3_pop'][color]
            extra_reward = self.model['color_pop_reward']['extra_pop'][color] * (length - 3)
            pop_value = (base_reward + extra_reward) * pop_prob * success_prob
            
            # Scale based on game stage
            time_factor = min(1.5, 1 + (max_steps - remaining_steps) / max_steps)
            score += pop_value * time_factor
        
        # Analyze near-matches (2 in a row)
        test_line = line[:pos] + [ball] + line[pos:]
        for i in range(len(test_line) - 1):
            if test_line[i] == test_line[i + 1]:
                next_prob = self.model['next_color_dist'][test_line[i]]
                future_value = self.model['color_pop_reward']['3_pop'][test_line[i]] * next_prob * pop_prob
                score += future_value * (remaining_steps / max_steps)

        # Strategic positioning
        middle_pos = len(line) / 2
        pos_factor = 1 - abs(pos - middle_pos) / len(line)
        score *= (1 + 0.2 * pos_factor)

        # End game considerations
        if remaining_steps < 10:
            if len(line) < 6:
                clear_potential = 0
                for color in set(line):
                    matches = line.count(color)
                    if matches >= 2:
                        clear_potential += matches * self.model['color_pop_reward']['3_pop'][color]
                score += clear_potential * success_prob

        # Penalty avoidance
        remaining_factor = remaining_steps / max_steps
        penalty_weight = self.model['color_not_finished_punishment'][ball]
        if len(potential_pops) > 0:
            score += penalty_weight * 2
        elif remaining_factor < 0.3:
            score -= penalty_weight

        return score

    def choose_next_action(self):
        state = self.original_game.get_current_state()
        line, ball, steps, max_steps = state
        
        if steps >= max_steps or not line or ball is None:
            return -1
            
        best_score = float('-inf')
        best_pos = -1
        remaining_steps = max_steps - steps
        
        # Consider all positions
        for pos in range(-1, len(line) + 1):
            score = self._evaluate_position(line, pos, ball, remaining_steps, max_steps)
            if score > best_score:
                best_score = score
                best_pos = pos
                
        return best_pos