import numpy as np


def read_input(file_name="input.txt"):
    with open(file_name, "r") as f:
        lines = [line.rstrip() for line in f.readlines()]

    patterns = [[]]
    for line in lines:
        if line == "":
            patterns.append([])
        else:
            bits = [0 if c == "." else 1 for c in line]
            patterns[-1].append(bits)

    patterns = [np.array(p) for p in patterns]

    return patterns


def find_horizontal_split(pattern, need_diff=0):
    for i in range(len(pattern) - 1):
        top = pattern[: i + 1, :]
        bottom = pattern[i + 1 :, :]

        min_length = min(len(top), len(bottom))

        top = top[i - min_length + 1 :]
        bottom = np.flip(bottom[:min_length, :], 0)

        diff = np.sum(top != bottom)

        if diff == need_diff:
            return i

    return None


def solve(patterns, need_diff=0):
    total = 0
    for pattern in patterns:
        flip = find_horizontal_split(pattern, need_diff)
        flip = (flip + 1) * 100 if flip is not None else None 
        if flip is None:
            flip = (
                len(pattern[0])
                - find_horizontal_split(np.rot90(pattern), need_diff)
                - 1
            )

        total += flip

    return total


def main():
    patterns = read_input()

    print("Subtask 1:", solve(patterns, 0))
    print("Subtask 2:", solve(patterns, 1))


if __name__ == "__main__":
    main()
