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

def solve_part_1(battery_banks):
    total = 0
    for bank in battery_banks:
        first_digit = max(bank[:-1])
        index_of_first_digit = bank.index(first_digit)

        second_digit = max(bank[index_of_first_digit+1:])

        print(bank, first_digit, second_digit, first_digit+second_digit, int(first_digit+second_digit))
        total += int(first_digit + second_digit)

    return total

def solve_part_2(battery_banks):
    total = 0
    for bank in battery_banks:
        print(bank)
        digits = ""
        remaining_bank = bank
        for i in range(12):
            next_digit = max(remaining_bank[:len(remaining_bank)-(11-len(digits))])
            next_digit_index = remaining_bank.index(next_digit)
            digits += next_digit
            remaining_bank = remaining_bank[next_digit_index+1:]
            print(i, next_digit, remaining_bank, 12 - i - 1)

        assert len(digits) == 12
        total += int(digits)
    return total

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
