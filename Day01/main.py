def read_input(file_name = "input.txt"):
    with open(file_name, "r") as f:
        lines = [
            line.replace("\n", "")
            for line in f.readlines()
        ]
    
    return lines

def subtask_1(lines):
    digits = [list(filter(str.isdigit, s)) for s in lines]
    return sum(int("".join([d[0], d[-1]])) for d in digits)

def subtask_2(lines):
    search_strings = {
        "1": 1,
        "one": 1,
        "2": 2,
        "two": 2,
        "3": 3,
        "three": 3,
        "4": 4,
        "four": 4,
        "5": 5,
        "five": 5,
        "6": 6,
        "six": 6,
        "7": 7,
        "seven": 7,
        "8": 8,
        "eight": 8,
        "9": 9,
        "nine": 9
    }

    answer = 0

    for line in lines:
        found = []
        for idx in range(len(line)):
            for target, value in search_strings.items():
                substring = line[idx : idx + len(target)]
                if substring == target:
                    found.append(value)

        answer += 10 * found[0] + found[-1]    
    
    return answer

def main():
    lines = read_input()
    
    print("Subtask 1:", subtask_1(lines))
    print("Subtask 2:", subtask_2(lines))

if __name__ == "__main__":
    main()