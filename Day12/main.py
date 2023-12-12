import numpy as np


def read_input(file_name="input.txt"):
    with open(file_name, "r") as f:
        lines = [line.rstrip() for line in f.readlines()]

    springs = [
        (line.split()[0], list(map(int, line.split()[1].split(",")))) for line in lines
    ]

    return springs


def safe_get(string, idx):
    return string[idx] if 0 <= idx < len(string) else None


def get_possibilities(spring, damaged):
    """
    Messy bottom up DP solution

    O(n ^ 2 * m)
    n - length of spring
    m - number of needed segments

    Should not be difficult to optimize into O(n * m). Third inner dp loop 
    looks easy to eliminate
    """

    dp = np.zeros((len(spring), len(damaged)))

    def can_put_here(i, j):
        if (
            i >= len(spring)
            or safe_get(spring, i + 1) == "#"
            or safe_get(spring, i - damaged[j]) == "#"
            or damaged[j] - 1 > i
        ):
            return False
        return all(spring[i - k] in ("?", "#") for k in range(damaged[j]))

    first_damage = spring.find("#")
    first_range = first_damage + damaged[0] + 1 if first_damage != -1 else len(spring)

    for i in range(first_range):
        if can_put_here(i, 0):
            dp[i][0] = 1

    for i in range(len(spring)):
        for j in range(1, len(damaged)):
            if can_put_here(i, j):
                for k in range(i - damaged[j] - 1, -1, -1):
                    dp[i][j] += dp[k][j - 1]
                    if spring[k] == "#":
                        break

    total = 0
    for i in range(len(spring) - 1, -1, -1):
        total += dp[i][len(damaged) - 1]
        if spring[i] == "#":
            break

    return total


def subtask_1(springs):
    return int(sum([get_possibilities(s[0], s[1]) for s in springs]))


def subtask_2(springs):
    return int(
        sum([get_possibilities(((s[0] + "?") * 5)[:-1], s[1] * 5) for s in springs])
    )


def test():
    assert get_possibilities("?###????????", [3, 2, 1]) == 10.0
    assert get_possibilities("???.###", [1, 1, 3]) == 1
    assert get_possibilities("..?...", [1]) == 1
    assert get_possibilities("?#?#?#?#?#?#?#?", [1, 3, 1, 6]) == 1
    assert get_possibilities("????.#...#...", [4, 1, 1]) == 1
    assert get_possibilities(".??..??...?##.", [1, 1, 3]) == 4
    assert get_possibilities("?#??..?#??..???", [3, 2, 1]) == 2 * 2 * 3 + 2
    assert get_possibilities("???...#", [3]) == 0
    assert get_possibilities("???...#", [3, 2]) == 0
    assert get_possibilities("#.#.#.??????", [1, 1, 1]) == 1
    assert get_possibilities("#.#.#.??#???", [1, 1, 1, 1]) == 1
    assert get_possibilities("#??#??#", [2, 1, 2]) == 1
    assert get_possibilities("..?.?#..?.#?...", [1, 1]) == 1
    assert get_possibilities("#.#???", [3]) == 0
    assert get_possibilities("?#?#.?", [3]) == 1
    assert get_possibilities("###?###", [6]) == 0
    assert get_possibilities("#..?#?..?#?..?#?", [1, 2, 2, 2]) == 8


def main():
    test()

    springs = read_input()

    print("Subtask 1:", subtask_1(springs))
    print("Subtask 2:", subtask_2(springs))


if __name__ == "__main__":
    main()