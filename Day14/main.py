import numpy as np

ROCK = "O"
WALL = "#"
EMPTY = "."


def read_input(file_name="input.txt"):
    with open(file_name, "r") as f:
        lines = [line.rstrip() for line in f.readlines()]

    platform = [list(line) for line in lines]

    return np.array(platform)


def roll_up(panel):
    height = len(panel)
    width = len(panel[0])

    for j in range(width):
        num_rocks = 0
        for i in range(height - 1, -1, -1):
            if panel[i, j] == ROCK:
                panel[i, j] = EMPTY
                num_rocks += 1

            if panel[i, j] == WALL:
                panel[i + 1 : i + 1 + num_rocks, j] = ROCK
                num_rocks = 0

        if num_rocks > 0:
            panel[:num_rocks, j] = ROCK


def cycle(panel, num_cycles):
    seen = {}

    def do_one_cycle(panel):
        for _ in range(4):
            roll_up(panel)
            panel = np.rot90(panel, 3)

    for cycle_id in range(num_cycles):
        do_one_cycle(panel)

        key = hash(panel.data.tobytes())

        if key in seen:
            cycle_length = cycle_id - seen[key]
            for _ in range((num_cycles - cycle_id - 1) % cycle_length):
                do_one_cycle(panel)
            break
        else:
            seen[key] = cycle_id


def get_weight(panel):
    return np.sum(np.sum(panel == ROCK, axis=1) * np.arange(len(panel), 0, -1))


def subtask_1(panel):
    panel_cpy = np.copy(panel)
    roll_up(panel_cpy)
    return get_weight(panel_cpy)


def subtask_2(panel):
    panel_cpy = np.copy(panel)
    cycle(panel_cpy, 1000000000)
    return get_weight(panel_cpy)


def main():
    panel = read_input()

    print("Subtask 1:", subtask_1(panel))
    print("Subtask 2:", subtask_2(panel))


if __name__ == "__main__":
    main()
