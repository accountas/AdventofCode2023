import sys
import numpy as np
from enum import Enum

sys.setrecursionlimit(1000000)

DIR_UP = (-1, 0)
DIR_DOWN = (1, 0)
DIR_LEFT = (0, -1)
DIR_RIGHT = (0, 1)


def v_sum(vector_a, vector_b):
    return tuple(a + b for a, b in zip(vector_a, vector_b))


def read_input(file_name="input.txt"):
    with open(file_name, "r") as f:
        lines = [l.rstrip() for l in f.readlines()]

    return lines


def get_number_energized(cavern, entry_pos, entry_dir):
    width = len(cavern[0])
    height = len(cavern)

    visited = set()

    def walk(pos, dir):
        if (
            (pos, dir) in visited
            or pos[0] < 0
            or pos[1] < 0
            or pos[0] >= height
            or pos[1] >= width
        ):
            return

        visited.add((pos, dir))
        cur_char = cavern[pos[0]][pos[1]]

        match cur_char:
            case ".":
                walk(v_sum(pos, dir), dir)
            case "|":
                if dir in (DIR_UP, DIR_DOWN):
                    walk(v_sum(pos, dir), dir)
                else:
                    walk(v_sum(pos, DIR_UP), DIR_UP)
                    walk(v_sum(pos, DIR_DOWN), DIR_DOWN)
            case "-":
                if dir in (DIR_LEFT, DIR_RIGHT):
                    walk(v_sum(pos, dir), dir)
                else:
                    walk(v_sum(pos, DIR_LEFT), DIR_LEFT)
                    walk(v_sum(pos, DIR_RIGHT), DIR_RIGHT)
            case "/":
                new_dir_mapping = {
                    DIR_UP: DIR_RIGHT,
                    DIR_DOWN: DIR_LEFT,
                    DIR_LEFT: DIR_DOWN,
                    DIR_RIGHT: DIR_UP,
                }
                new_dir = new_dir_mapping[dir]
                walk(v_sum(pos, new_dir), new_dir)
            case "\\":
                new_dir_mapping = {
                    DIR_UP: DIR_LEFT,
                    DIR_DOWN: DIR_RIGHT,
                    DIR_LEFT: DIR_UP,
                    DIR_RIGHT: DIR_DOWN,
                }
                new_dir = new_dir_mapping[dir]
                walk(v_sum(pos, new_dir), new_dir)

    walk(entry_pos, entry_dir)
    return len(set(node[0] for node in visited))


def subtask_1(cavern):
    return get_number_energized(cavern, (0, 0), DIR_RIGHT)


def subtask_2(cavern):
    ans = 0
    for start_row in range(len(cavern)):
        ans = max(ans, get_number_energized(cavern, (start_row, 0), DIR_RIGHT))
        ans = max(
            ans, get_number_energized(cavern, (start_row, len(cavern[0]) - 1), DIR_LEFT)
        )

    for start_col in range(len(cavern[0])):
        ans = max(ans, get_number_energized(cavern, (0, start_col), DIR_DOWN))
        ans = max(
            ans, get_number_energized(cavern, (len(cavern) - 1, start_col), DIR_UP)
        )

    return ans


def main():
    cavern = read_input()

    print("Subtask 1:", subtask_1(cavern))
    print("Subtask 2:", subtask_2(cavern))


if __name__ == "__main__":
    main()
