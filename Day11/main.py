def read_input(file_name="input.txt"):
    with open(file_name, "r") as f:
        galaxy = [list(line.replace("\n", "")) for line in f.readlines()]

    return galaxy


def find_all_stars(galaxy):
    stars = []
    for i, line in enumerate(galaxy):
        for j, char in enumerate(line):
            if char == "#":
                stars.append((i, j))
    return stars


def solve(stars, expand_by):
    def expand_1d(coords):
        expanded = []
        total_expansion = 0
        for i in range(len(coords)):
            now = coords[i]
            last = -1 if i == 0 else coords[i - 1]
            delta = max(0, now - last - 1) * (expand_by - 1)
            total_expansion += delta
            expanded.append(now + total_expansion)
        return expanded

    old_i = [s[0] for s in stars]
    old_j = [s[1] for s in stars]

    new_i = expand_1d(sorted(old_i))
    new_j = expand_1d(sorted(old_j))

    total_dist = 0
    for i in range(len(stars)):
        for j in range(i + 1, len(stars)):
            total_dist += abs(new_i[i] - new_i[j])
            total_dist += abs(new_j[i] - new_j[j])

    return total_dist


def main():
    galaxy = read_input()
    stars = find_all_stars(galaxy)

    print("Subtask 1:", solve(stars, expand_by=2))
    print("Subtask 2:", solve(stars, expand_by=1000000))


if __name__ == "__main__":
    main()
