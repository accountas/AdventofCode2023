from collections import deque
from pprint import pprint

DIR_UP = (-1, 0)
DIR_DOWN = (1, 0)
DIR_LEFT = (0, -1)
DIR_RIGHT = (0, 1)

DIRECTIONS = [DIR_UP, DIR_DOWN, DIR_RIGHT, DIR_LEFT]

INF = 2**30


def vec2_sum(a, b):
    return (a[0] + b[0], a[1] + b[1])


def read_input(file_name="input.txt"):
    with open(file_name, "r") as f:
        lines = [l.rstrip() for l in f.readlines()]

    return lines


def is_valid_pos(garden, pos, repeat=False):
    n = len(garden)
    m = len(garden[0])

    if not repeat and (pos[0] < 0 or pos[1] < 0 or pos[0] >= n or pos[1] >= n):
        return False

    return garden[pos[0] % n][pos[1] % m] != "#"


def get_distances(garden, start_pos, max_steps, repeat):
    distances = {}

    bfs_queue = deque()
    bfs_queue.append(start_pos)

    distances[start_pos] = 0

    while len(bfs_queue):
        cur_pos = bfs_queue.popleft()

        for dir in DIRECTIONS:
            new_pos = vec2_sum(cur_pos, dir)

            if (
                new_pos not in distances
                and is_valid_pos(garden, new_pos, repeat)
                and distances[cur_pos] < max_steps
            ):
                distances[new_pos] = distances[cur_pos] + 1
                bfs_queue.append(new_pos)

    return distances


def get_start_pos(garden):
    for i, line in enumerate(garden):
        for j, c in enumerate(line):
            if c == "S":
                return (i, j)


def subtask_1(garden, num_steps):
    start_pos = get_start_pos(garden)
    distances = get_distances(garden, start_pos, num_steps, repeat=True)

    return sum(d <= num_steps and d % 2 == num_steps % 2 for d in distances.values())


def subtask_2(garden, num_steps):
    """
    Cant believe this shit works
    Assumes some properties of the input: square, border is empty
    and empty lines in all direction from the start (I think this approach
    can be modified to work without the last assumption)
    """
    n = len(garden)

    corners = [(n - 1, 0), (0, n - 1), (0, 0), (n - 1, n - 1)]

    dist_to_corner = n + 1
    dist_to_center = (n - 1) // 2 + 1

    answer = 0

    for corner in corners:
        distances = get_distances(garden, corner, INF, repeat=False)
        for distance in distances.values():
            delta = num_steps - distance - dist_to_corner
            num_tiles = delta // n
            needs_odd = distance % 2 != num_steps % 2

            if delta < 0:
                continue

            if needs_odd:
                answer += ((num_tiles + 1) // 2) * (((num_tiles + 1) // 2) + 1)
            else:
                answer += ((num_tiles + 2) // 2) ** 2

    centers = [(0, n // 2), (n - 1, n // 2), (n // 2, 0), (n // 2, n - 1)]
    for center in centers:
        distances = get_distances(garden, center, INF, repeat=False)
        for distance in distances.values():
            delta = num_steps - distance - dist_to_center

            if delta < 0:
                continue

            num_tiles = delta // n
            needs_odd = (distance + dist_to_center) % 2 != num_steps % 2

            if needs_odd:
                answer += (num_tiles + 1) // 2
            else:
                answer += (num_tiles) // 2 + 1

    start_dist = get_distances(garden, get_start_pos(garden), INF, repeat=False)
    return answer + sum(
        d <= num_steps and d % 2 == num_steps % 2 for d in start_dist.values()
    )


def main():
    garden = read_input()

    print("Subtask 1:", subtask_1(garden, 64))
    print("Subtask 2:", subtask_2(garden, 26501365))


if __name__ == "__main__":
    main()
