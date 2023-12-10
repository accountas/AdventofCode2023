from dataclasses import dataclass
from pprint import pprint
import sys

sys.setrecursionlimit(1_000_000)

CONNECTS = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(0, -1), (1, 0)],
    "F": [(0, 1), (1, 0)],
    "S": [(1, 0), (-1, 0), (0, 1), (-1, 0)],
    ".": []
}

@dataclass(frozen=True)
class Node:
    i: int
    j: int
    pipe: str

    def get_pos(this):
        return (this.i, this.j)


def read_input(file_name = "input.txt"):
    with open(file_name, "r") as f:
        lines = [
            line.replace("\n", "")
            for line in f.readlines()
        ]
    
    return lines


def build_graph(pipes):
    graph = {}

    height, width = len(pipes), len(pipes[0])

    for i in range(height):
        for j in range(width):
            node_now = Node(i, j, pipes[i][j])
            graph[node_now] = []

            for child_dir in CONNECTS[pipes[i][j]]:
                child = Node(
                    i + child_dir[0],
                    j + child_dir[1],
                    pipes[i + child_dir[0]][j + child_dir[1]]
                )

                connects_back = (i, j) in [
                    vec_2_add(child.get_pos(), dir) for dir in CONNECTS[child.pipe]
                ]
  
                if connects_back:
                    graph[node_now].append(child)
    
    return graph

def pad(pipes, pad_with = '.'):
    bottom_and_top = [pad_with * (len(pipes[0]) + 2)]
    padded_lines = [pad_with + line + pad_with for line in pipes]
    return bottom_and_top + padded_lines + bottom_and_top


def vec_2_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def subtask_1(graph):
    start = [node for node in graph if node.pipe == "S"][0]

    visited = set()

    def walk(node):
        visited.add(node)
        for adj in graph[node]:
            if adj not in visited:
                walk(adj)
    
    walk(start)

    return len(visited) // 2


def subtask_2(graph, pipes):
    start = [node for node in graph if node.pipe == "S"][0]

    visited = set()
    on_the_left = set()

    def walk(node):
        visited.add(node.get_pos())

        next_node = None
        for adj in graph[node]:
            if adj.get_pos() not in visited or (adj.pipe == 'S' and len(visited) > 2):
                next_node = adj
        
        if next_node is None:
            return
        
        new_direction = (
            next_node.i - node.i, next_node.j - node.j
        )
        on_the_left.add(
            (node.i - new_direction[1], node.j + new_direction[0])
        )
        on_the_left.add(
            (next_node.i - new_direction[1], next_node.j + new_direction[0])
        )
  
        walk(next_node)

    walk(start)

    height, width = len(pipes), len(pipes[0])

    def count_tiles(pos):
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= height or pos[1] >= width:
            return 0, False
        
        visited.add(pos)
        total_tiles = 1
        contains_left = pos in on_the_left

        for dir in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            new_pos = vec_2_add(pos, dir)
            if new_pos not in visited:
                land, left = count_tiles(new_pos)
                total_tiles += land
                contains_left = contains_left or left
        
        return total_tiles, contains_left

    left_is_inside = None
    land_inside = 0

    for i in range(height):
        for j in range(width):
            if (i, j) in visited:
                continue

            tiles, has_left = count_tiles((i, j))

            if i == 0 and j == 0:
                left_is_inside = not has_left
            elif left_is_inside == has_left:
                land_inside += tiles

    return land_inside


def main():
    pipes = pad(read_input())
    graph = build_graph(pipes)

    print("Subtask 1:", subtask_1(graph))
    print("Subtask 2:", subtask_2(graph, pipes))

if __name__ == "__main__":
    main()