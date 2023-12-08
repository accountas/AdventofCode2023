import math


def read_input(file_name="input.txt"):
    with open(file_name, "r") as f:
        lines = [line.rstrip() for line in f.readlines()]

    directions = lines[0]

    graph = {}
    for line in lines[2:]:
        node, children = line.split(" = ")
        left, right = children[1:-1].split(", ")
        graph[node] = (left, right)

    return directions, graph


def steps_till(start_node, graph, path, condition):
    now = start_node
    step = 0
    while not condition(now):
        now = graph[now][path[step % len(path)] == "R"]
        step += 1
    return step


def subtask_1(directions, graph):
    return steps_till("AAA", graph, directions, lambda n: n == "ZZZ")


def subtask_2(directions, graph):
    """
    Input is weak at least in my case. Only one z in each ghosts loop.
    Time to reach Z is equal to the loop length from that Z. This only solves 
    such sub-case of the problem.
    """
    cycle_lengths = [
        steps_till(node, graph, directions, lambda n: n[2] == "Z") 
        for node in graph.keys() 
        if node[2] == "A"
    ]
    return math.lcm(*cycle_lengths)


def main():
    directions, graph = read_input()

    print("Subtask 1:", subtask_1(directions, graph))
    print("Subtask 2:", subtask_2(directions, graph))


if __name__ == "__main__":
    main()
