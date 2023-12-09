from functools import reduce


def read_input(file_name="input.txt"):
    with open(file_name, "r") as f:
        lines = f.readlines()

    sequences = [[int(i) for i in line.rstrip().split()] for line in lines]

    return sequences


def main():
    sequences = read_input()

    total_next = 0
    total_prev = 0

    for seq in sequences:
        deltas = [seq]
        while set(deltas[-1]) != set([0]):
            new_deltas = [j - i for i, j in zip(deltas[-1], deltas[-1][1:])]
            deltas.append(new_deltas)

        total_next += sum(s[-1] for s in deltas)
        total_prev += reduce(lambda a, b: b - a, [s[0] for s in deltas][::-1])

    print("Subtask 1:", total_next)
    print("Subtask 2:", total_prev)


if __name__ == "__main__":
    main()
