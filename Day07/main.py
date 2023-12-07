from collections import Counter
from itertools import combinations_with_replacement

CARDS = "A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2, *".split(", ")


def read_input(file_name="input.txt"):
    with open(file_name, "r") as f:
        lines = f.readlines()

    cards = [line.replace("\n", "").split() for line in lines]

    return cards


def get_hand_values(hand):
    return [list(reversed(CARDS)).index(card) for card in hand]


def get_hand_type_rank(hand):
    counts = sorted(Counter(hand).values(), reverse=True)

    if counts == [5]:
        return 1
    elif counts == [4, 1]:
        return 2
    elif counts == [3, 2]:
        return 3
    elif counts == [3, 1, 1]:
        return 4
    elif counts == [2, 2, 1]:
        return 5
    elif counts == [2, 1, 1, 1]:
        return 6
    elif counts == [1, 1, 1, 1, 1]:
        return 7
    else:
        raise ValueError(f"Unrecognized hand type {hand}")


def best_rank_with_jokers(hand):
    non_jokers = [c for c in hand if c != "J"]
    num_jokers = 5 - len(non_jokers)

    if num_jokers == 5:
        return 1 # Five of a kind
    elif num_jokers == 0:
        return get_hand_type_rank(hand)

    # Replace jokers (only worth replacing with cards already in the hand)
    best_rank = 100
    for replacements in combinations_with_replacement(non_jokers, num_jokers):
        replaced = hand
        for joker_type in replacements:
            replaced = replaced.replace("J", joker_type, 1)
        best_rank = min(best_rank, get_hand_type_rank(replaced))

    return best_rank


def get_winnings(hands_sorted):
    return sum([(i + 1) * int(hand[1]) for i, hand in enumerate(hands_sorted)])


def subtask_1(hands):
    hands_sorted = sorted(
        hands, key=lambda h: (-get_hand_type_rank(h[0]), get_hand_values(h[0]))
    )
    return get_winnings(hands_sorted)


def subtask_2(hands):
    hands_sorted = sorted(
        hands,
        key=lambda h: (
            -best_rank_with_jokers(h[0]),
            get_hand_values(h[0].replace("J", "*")),
        )
    )
    return get_winnings(hands_sorted)


def main():
    cards = read_input()

    print("Subtask 1:", subtask_1(cards))
    print("Subtask 2:", subtask_2(cards))


if __name__ == "__main__":
    main()
