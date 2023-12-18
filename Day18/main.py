import numpy as np
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Instruction:
    direction: str
    amount: int
    color: str


def read_input(file_name="input.txt"):
    with open(file_name, "r") as f:
        lines = [l.rstrip() for l in f.readlines()]

    dig_plan = []
    for line in lines:
        direction, amount, color = line.split()
        dig_plan.append(Instruction(direction, int(amount), color[1:-1]))

    return dig_plan


def get_polygon_area(vertices):
    area = 0
    for cur, next in zip(vertices, vertices[1:]):
        area += (cur[0] + next[0]) * (next[1] - cur[1])
    return abs(area // 2)


def get_dig_area(dig_plan):
    cur_pos = [0, 0]

    vertices = [tuple(cur_pos)]
    perimeter = 0

    for task in dig_plan:
        match task.direction:
            case "R":
                cur_pos[0] += task.amount
            case "L":
                cur_pos[0] -= task.amount
            case "U":
                cur_pos[1] += task.amount
            case "D":
                cur_pos[1] -= task.amount
        vertices.append(tuple(cur_pos))
        perimeter += task.amount

    return get_polygon_area(vertices) + perimeter // 2 + 1


def main():
    dig_plan = read_input()

    fixed_dig_plan = [
        Instruction(
            direction="RDLU"[int(bad.color[-1])],
            amount=int(bad.color[1:-1], 16),
            color="",
        )
        for bad in dig_plan
    ]

    print("Subtask 1:", get_dig_area(dig_plan))
    print("Subtask 2:", get_dig_area(fixed_dig_plan))


if __name__ == "__main__":
    main()
