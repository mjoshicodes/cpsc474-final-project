P1 = 1
P2 = 2

Left = 1
Right = 2

def get_greedy_action(actions, myself, opponent):
    all_actions = []

    for action in actions:
        action_type = action[0]
        left_hand = myself.left_hand()
        right_hand = myself.right_hand()

        opponent_left_hand = opponent.left_hand()
        opponent_right_hand = opponent.right_hand()

        if action_type == "SPLIT":
            new_left_hand, new_right_hand = action[1], action[2]
            reward = 0

            if new_left_hand + opponent_left_hand == 5 or new_left_hand + opponent_right_hand == 5 or new_right_hand + opponent_left_hand == 5 or new_right_hand + opponent_right_hand == 5:
                reward -= 1
            if left_hand + opponent_left_hand == 5 or left_hand + opponent_right_hand == 5 or right_hand + opponent_left_hand == 5 or right_hand + opponent_right_hand == 5:
                reward += 1

            all_actions.append(("SPLIT", new_left_hand, new_right_hand, reward))

        elif action_type == "ATTACK":
            attack_value, attacked_hand_idx = action[1], action[2]
            attacked_hand = opponent_left_hand if attacked_hand_idx == Left else opponent_right_hand
            resulting_attack_value = (attack_value + attacked_hand) % 5

            if resulting_attack_value == 0:
                all_actions.append(("ATTACK", attack_value, attacked_hand_idx, 1))
            elif (5 - resulting_attack_value) == left_hand or (5 - resulting_attack_value) == right_hand:
                all_actions.append(("ATTACK", attack_value, attacked_hand_idx, -1))
            else:
                all_actions.append(("ATTACK", attack_value, attacked_hand_idx, 0))
        else:
            new_left_hand, new_right_hand = action[1], action[2]
            reward = 0

            if new_left_hand + opponent_left_hand == 5 or new_left_hand + opponent_right_hand == 5 or new_right_hand + opponent_left_hand == 5 or new_right_hand + opponent_right_hand == 5:
                reward -= 1
            if left_hand + opponent_left_hand == 5 or left_hand + opponent_right_hand == 5 or right_hand + opponent_left_hand == 5 or right_hand + opponent_right_hand == 5:
                reward += 1

            all_actions.append(("DIVIDE", new_left_hand, new_right_hand, reward))

    print("all_Actions", all_actions)
    best_action = max(all_actions, key=lambda t: t[3])
    return (best_action[0], best_action[1], best_action[2])
