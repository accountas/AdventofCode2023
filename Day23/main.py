import sys
from copy import copy

sys.setrecursionlimit(1000000)

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


def is_valid_pos(island, pos):
    n, m = len(island), len(island[0])

    if pos[0] < 0 or pos[1] < 0 or pos[0] >= n or pos[1] >= m or island[pos[0]][pos[1]] == "#":
        return False

    return True


def subtask_1(island):
    start_pos = (0, island[0].index("."))
    end_pos = (len(island) - 1, island[-1].index("."))

    longest_path = 0

    def dfs(pos, in_path):
        nonlocal longest_path
        if not is_valid_pos(island, pos) or pos in in_path:
            return

        in_path.add(pos)

        if pos == end_pos:
            longest_path = max(longest_path, len(in_path))

        match island[pos[0]][pos[1]]:
            case ">":
                dfs(vec2_sum(pos, DIR_RIGHT), in_path)
            case "<":
                dfs(vec2_sum(pos, DIR_LEFT), in_path)
            case "^":
                dfs(vec2_sum(pos, DIR_UP), in_path)
            case "v":
                dfs(vec2_sum(pos, DIR_DOWN), in_path)
            case ".":
                for child in [vec2_sum(pos, dir) for dir in DIRECTIONS]:
                    dfs(child, in_path)

        in_path.remove(pos)

    dfs(start_pos, set())

    return longest_path - 1


def subtask_2(island):
    condensed_nodes = []

    for i in range(len(island)):
        for j in range(len(island[0])):
            if not is_valid_pos(island, (i, j)):
                continue

            num_children = sum(is_valid_pos(island, vec2_sum((i, j), dir)) for dir in DIRECTIONS)
            if num_children > 2 or num_children == 1:
                condensed_nodes.append((i, j))

    def get_distance(cur_node, start, end, visited):
        if cur_node == end:
            return 0

        if (
            not is_valid_pos(island, cur_node)
            or (cur_node in condensed_nodes and cur_node != start)
            or cur_node in visited
        ):
            return None

        visited.add(cur_node)

        for child in [vec2_sum(cur_node, dir) for dir in DIRECTIONS]:
            if child != cur_node:
                dist = get_distance(child, start, end, visited)
                if dist is not None:
                    return dist + 1

        return None

    graph = {node: [] for node in condensed_nodes}

    for i in range(len(condensed_nodes)):
        for j in range(i + 1, len(condensed_nodes)):
            a = condensed_nodes[i]
            b = condensed_nodes[j]
            dist = get_distance(a, a, b, set())
            if dist is not None:
                graph[a].append((b, dist))
                graph[b].append((a, dist))

    for children in graph.values():
        children.sort(key=lambda x: -x[1])

    # Visualise with graphviz
    # for node, children in graph.items():
    #     name = lambda node: f"\"{node[0]}-{node[1]}\""
    #     for child in children:
    #         print(f"{name(node)} -> {name(child[0])} [label={child[1]}]")

    start_node = (0, island[0].index("."))
    end_node = (len(island) - 1, island[-1].index("."))

    best_dist = 0

    def brute_force(cur_node, cur_dist, cur_path):
        nonlocal best_dist
        if cur_node in cur_path:
            return

        if cur_node == end_node:
            if cur_dist > best_dist:
                best_dist = cur_dist
            return

        cur_path.add(cur_node)

        for child, dist in graph[cur_node]:
            brute_force(child, cur_dist + dist, cur_path)

        cur_path.remove(cur_node)

    brute_force(start_node, 0, set())
    return best_dist


def main():
    island = read_input()

    print("Subtask 1:", subtask_1(island))
    print("Subtask 2:", subtask_2(island))


if __name__ == "__main__":
    main()
