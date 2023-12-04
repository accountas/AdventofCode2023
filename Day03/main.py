from collections import defaultdict

ADJACENT_DIR = [(0, 1), (0, -1), (1, -1), (1, 0), (1, 1), (-1, -1), (-1, 0), (-1, 1)]

def read_input(file_name = "input.txt"):
    with open(file_name, "r") as f:
        lines = f.readlines()

    engine_matrix = [
        list(line.replace("\n", ""))
        for line in lines
    ]
    
    return engine_matrix

def main():
    engine_matrix = read_input()

    height = len(engine_matrix)
    width = len(engine_matrix[0])

    parts_sum = 0
    neighbors_of_symbols = defaultdict(list)

    for i in range(height):
        digits = []
        adjacent_to = set()

        for j in range(width):
            cur_char = engine_matrix[i][j]
            if cur_char.isdigit():
                digits.append(cur_char)

                for di, dj in ADJACENT_DIR:
                    adj_i = i + di
                    adj_j = j + dj

                    if adj_i < 0 or adj_j < 0 or adj_j >= width or adj_i >= height:
                        continue
                    
                    adj_char = engine_matrix[adj_i][adj_j]
                    if adj_char != '.' and not adj_char.isdigit():
                        adjacent_to.add((adj_i, adj_j))

            if (not cur_char.isdigit() or j == width - 1) and len(digits) > 0:
                if len(adjacent_to) > 0:
                    part_num = int("".join(digits))
                    parts_sum += part_num
                    for symbol in adjacent_to:
                        neighbors_of_symbols[symbol].append(part_num)

                digits = []
                adjacent_to = set()
    
    gears_sum = 0
    for symbol_pos, neighbors in neighbors_of_symbols.items():
        if engine_matrix[symbol_pos[0]][symbol_pos[1]] == '*' and len(neighbors) == 2:
            gears_sum += neighbors[0] * neighbors[1]

    print("Subtask 1:", parts_sum)
    print("Subtask 2:", gears_sum)

if __name__ == "__main__":
    main()