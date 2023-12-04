def read_input(file_name = "input.txt"):
    with open(file_name, "r") as f:
        lines = f.readlines()

    cards = [
        [
            set(int(number) for number in number_set.split(" ") if number != "") 
            for number_set in line.replace("\n", "").split(": ")[1].split(" | ")
        ]
        for line in lines
    ]

    return cards

def subtask_1(cards):
    total_score = 0

    for card in cards:
        match_amount = len(card[0] & card[1])
        if match_amount > 0:
            total_score += 2 ** (match_amount - 1)
    
    return total_score

def subtask_2(cards):
    number_of_instances = [1] * len(cards)

    for card_idx, card in enumerate(cards):
        match_amount = len(card[0] & card[1])

        for i in range(card_idx + 1, card_idx + match_amount + 1):
            number_of_instances[i] += number_of_instances[card_idx]
    
    return sum(number_of_instances)

def main():
    cards = read_input()
    
    print("Subtask 1:", subtask_1(cards))
    print("Subtask 2:", subtask_2(cards))

if __name__ == "__main__":
    main()