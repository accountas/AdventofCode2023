def read_input(file_name = "input.txt"):
    with open(file_name, "r") as f:
        lines = f.readlines()

    parsed = [
        [
            {
                color_count_pair.split()[1]: int(color_count_pair.split()[0]) 
                for color_count_pair in draw.split(", ")
            } 
            for draw in line.replace("\n", "").split(": ")[1].split("; ")
        ]
        for line in lines
    ]

    return parsed

def subtask_1(games):
    allowed = {
        "red" : 12,
        "green": 13,
        "blue": 14
    }

    answer = 0

    for game_id, game in enumerate(games):
        good_game = True
        for round in game:
            for color, count in round.items():
                if allowed[color] < count:
                    good_game = False

        if good_game:
            answer += game_id + 1

    return answer

def subtask_2(games):
    answer = 0

    for game in games:
        minimum_set = {}
        for round in game:
            for color, count in round.items():
                minimum_set[color] = max(minimum_set.get(color, 0), count)
        
        product = 1
        for color in ['red', 'green', 'blue']:
            product *= minimum_set.get(color, 0)
        answer += product
    
    return answer
    
def main():
    games = read_input()

    print("Subtask 1:", subtask_1(games))
    print("Subtask 2:", subtask_2(games))

if __name__ == "__main__":
    main()