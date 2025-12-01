import argparse
from rich import print

EXAMPLE_FILE_NAME = "example.txt"
INPUT_FILE_NAME= "input.txt"

def get_puzzle_input(use_example=False):
    input_filename = EXAMPLE_FILE_NAME if use_example else INPUT_FILE_NAME
    puzzle_input = []
    with open(input_filename) as input_txt:
        for line in input_txt:
            puzzle_input.append(line.strip())
    return puzzle_input

def solve_part_1(puzzle_input):
    position = 50
    zero_count = 0
    for rotation in puzzle_input:
        assert rotation[0] in "RL"
        direction = 1 if rotation[0] == "R" else -1
        amount = int(rotation[1:])
        position += direction * amount
        position %= 100

        if position == 0:
            zero_count += 1

    return zero_count

def solve_part_2(puzzle_input):
    position = 50
    zero_count = 0
    for rotation in puzzle_input:
        on_zero = position == 0
        direction = 1 if rotation[0] == "R" else -1
        amount = int(rotation[1:])
        position += direction * amount
        if position >= 100:
            zero_count += position // 100
        elif position <= 0:
            zero_count += abs(position) // 100 + (0 if on_zero else 1)
        position %= 100

    return zero_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
