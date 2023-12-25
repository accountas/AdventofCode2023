import random
from collections import deque


def read_input(filename="input.txt"):
    with open(filename, "r") as file:
        lines = [l.rstrip() for l in file.readlines()]

    graph = {}
    for line in lines:
        node, children = line.split(": ")
        children = children.split()

        for child in children:
            if node not in graph:
                graph[node] = []
            if child not in graph:
                graph[child] = []

            graph[node].append(child)
            graph[child].append(node)

    return graph


def solve(graph):
    """
    Assumes graph splits are pretty close in size,
    otherwise its N^3. Pick two random nodes - in O(n) check
    if they are in different splits - if yes find the cut edges.
    Probability of hitting two nodes in different splits should
    be high with the first assumption
    """
    
    def get_path(start, end, ignore_edges):
        parent = {start: start}

        bfs_queue = deque()
        bfs_queue.append(start)

        while len(bfs_queue) > 0:
            node = bfs_queue.popleft()
            for child in graph[node]:
                if child not in parent and (node, child) not in ignore_edges:
                    parent[child] = node
                    bfs_queue.append(child)

        if end not in parent:
            return None, len(parent)

        path = [end]
        while end != start:
            end = parent[end]
            path.append(end)

        return path, len(parent)

    while True:
        node_a = random.choice(list(graph.keys()))
        node_b = random.choice(list(graph.keys()))
        if node_a == node_b:
            continue

        edges_in_paths = set()
        paths = []
        in_different_splits = False
        for path_num in range(1, 5):
            path, _ = get_path(node_a, node_b, edges_in_paths)
            if path is None:
                assert path_num == 4
                in_different_splits = True
                break

            for i in range(len(path) - 1):
                edges_in_paths.add((path[i], path[i + 1]))
                edges_in_paths.add((path[i + 1], path[i]))
            paths.append(path[::-1])

        if not in_different_splits:
            continue

        cut_edges = set()
        for path in paths:
            for prev_node, node in zip(path, path[1:]):
                if get_path(node_a, node, edges_in_paths)[0] is None:
                    cut_edges.add((prev_node, node))
                    break

        _, size = get_path(node_a, "Merry christmas!", cut_edges)
        return size * (len(graph) - size)


def main():
    graph = read_input()

    print("Result:", solve(graph))


if __name__ == "__main__":
    main()
