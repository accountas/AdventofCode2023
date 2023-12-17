import heapq
from dataclasses import dataclass
import cProfile

DIR_UP = (-1, 0)
DIR_DOWN = (1, 0)
DIR_LEFT = (0, -1)
DIR_RIGHT = (0, 1)

DIRECTIONS = [DIR_UP, DIR_DOWN, DIR_RIGHT, DIR_LEFT]

INF = int(1e9)


def read_input(file_name="input.txt"):
    with open(file_name, "r") as f:
        lines = [list(map(int, l.rstrip())) for l in f.readlines()]

    return lines


def valid_pos(matrix, index):
    return (
        index[0] >= 0
        and index[1] >= 0
        and index[0] < len(matrix)
        and index[1] < len(matrix[0])
    )


def vec2_sum(a, b):
    return (a[0] + b[0], a[1] + b[1])


class PriorityQueue:
    def __init__(self):
        self.values = []

    def put(self, value):
        heapq.heappush(self.values, value)

    def get(self):
        return heapq.heappop(self.values)

    def empty(self):
        return len(self.values) == 0


@dataclass(frozen=True, order=True)
class Node:
    pos: tuple[int, int]
    direction: tuple[int, int]
    moves_in_direction: int


def get_shortest_path(city, min_straight, max_straight):
    distances = {}
    pq = PriorityQueue()

    for dir in [DIR_RIGHT, DIR_DOWN]:
        start_node = Node(pos=(0, 0), direction=dir, moves_in_direction=1)
        distances[start_node] = 0
        pq.put((0, start_node))

    while not pq.empty():
        cur_distance, cur_node = pq.get()

        if distances[cur_node] != cur_distance:
            continue

        for dir in DIRECTIONS:
            same_dir = dir == cur_node.direction
            new_pos = vec2_sum(dir, cur_node.pos)

            if same_dir and cur_node.moves_in_direction >= max_straight:
                continue

            if not same_dir and cur_node.moves_in_direction < min_straight:
                continue

            if vec2_sum(dir, cur_node.direction) == (0, 0):
                continue

            if not valid_pos(city, new_pos):
                continue

            child_node = Node(
                pos=new_pos,
                direction=dir,
                moves_in_direction=[1, cur_node.moves_in_direction + 1][same_dir],
            )

            new_distance = cur_distance + city[new_pos[0]][new_pos[1]]

            if distances.get(child_node, INF) > new_distance:
                distances[child_node] = new_distance
                pq.put((new_distance, child_node))

    target_pos = (len(city) - 1, len(city[0]) - 1)
    return min(
        distance
        for node, distance in distances.items()
        if node.pos == target_pos and node.moves_in_direction >= min_straight
    )


def main():
    city = read_input()

    print("Subtask 1:", get_shortest_path(city, 0, 3))
    print("Subtask 2:", get_shortest_path(city, 4, 10))


if __name__ == "__main__":
    main()
