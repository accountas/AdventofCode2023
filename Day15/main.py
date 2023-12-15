import numpy as np

ROCK = "O"
WALL = "#"
EMPTY = "."


def read_input(file_name="input.txt"):
    with open(file_name, "r") as f:
        return f.readline().rstrip().split(",")

def aoc_hash(string):
    current_value = 0
    for c in string:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
    return current_value


def subtask_1(instructions):
    return sum([aoc_hash(ins) for ins in instructions])


def subtask_2(instructions):
    boxes = {i : [] for i in range(257)}

    for instruction in instructions:
        if "=" in instruction:
            lens, focal_len = instruction.split("=")            
            lenses_in_box = boxes[aoc_hash(lens)]

            replaced = False
            for i in range(len(lenses_in_box)):
                if lenses_in_box[i][0] == lens:
                    lenses_in_box[i] = (lens, focal_len)
                    replaced = True
                    break
            
            if not replaced:
                lenses_in_box.append((lens, focal_len))
        else:
            lens = instruction[:-1]
            lenses_in_box = boxes[aoc_hash(lens)]
            for i in range(len(lenses_in_box)):
                if lenses_in_box[i][0] == lens:
                    boxes[aoc_hash(lens)] = lenses_in_box[:i] + lenses_in_box[i + 1:]
                    break
    
    total = 0
    for box, lenses in boxes.items():
        for idx, lens in enumerate(lenses):
            total += (box + 1) * (idx + 1) * int(lens[1])

    return total

def main():
    instructions = read_input()

    print("Subtask 1:", subtask_1(instructions))
    print("Subtask 2:", subtask_2(instructions))


if __name__ == "__main__":
    main()
