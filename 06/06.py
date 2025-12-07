import argparse
from rich import print

EXAMPLE_FILE_NAME = "example.txt"
INPUT_FILE_NAME= "input.txt"

def get_puzzle_input(use_example=False):
    input_filename = EXAMPLE_FILE_NAME if use_example else INPUT_FILE_NAME
    puzzle_input = []
    longest_line_len = 0
    with open(input_filename) as input_txt:
        for line in input_txt:
            line = line.strip()
            if len(line) > longest_line_len:
                longest_line_len = len(line)
            puzzle_input.append(line)

    for i, line in enumerate(puzzle_input):
        puzzle_input[i] = line + (longest_line_len - len(line)) * " "

    assert all(len(line) == len(puzzle_input[0]) for line in puzzle_input)
    return puzzle_input

def mul(*numbers):
    total = 1
    for n in numbers:
        total *= int(n)
    return total

def sum2(*numbers):
    total = 0
    for n in numbers:
        total += int(n)
    return total

def solve_part_1(puzzle_input):
    lines = []
    for line in puzzle_input:
        lines.append(line.split())

    columns = list(zip(*lines))

    total = 0
    for column in columns:
        operation = sum2 if column[4] == "+" else mul
        result = operation(*column[:4])
        total += result
        print(column, result, total)

    return total

def solve_part_2(puzzle_input):
    columns = list(zip(*puzzle_input))

    total = 0
    unused_words = []
    for column in reversed(columns):
        word = "".join(column).strip()
        print(word)

        if len(word) == 0:
            continue

        operand = None
        if word.endswith("+"):
            operand = sum2
        elif word.endswith("*"):
            operand = mul

        if operand is not None:
            word = word[:-1]

        unused_words.append(word)

        if operand is not None:
            total += operand(*unused_words)
            unused_words = []

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
