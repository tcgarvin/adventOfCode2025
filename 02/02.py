import argparse
from rich import print

EXAMPLE_FILE_NAME = "example.txt"
INPUT_FILE_NAME= "input.txt"

def normalize_range(r:str) -> tuple[int, int]:
    r_split = r.split('-')
    return [int(r_split[0]), int(r_split[1])]


def get_puzzle_input(use_example=False):
    input_filename = EXAMPLE_FILE_NAME if use_example else INPUT_FILE_NAME
    puzzle_input = []
    with open(input_filename) as input_file:
        text = input_file.read().strip()
        ranges = [normalize_range(r) for r in text.split(',')]
    return ranges

def solve_part_1(ranges):
    total = 0
    for r in ranges:
        for i in range(r[0], r[1]+1):
            # could do this with ints, but don't want to think through edge cases
            product_id = str(i)

            if len(product_id) % 2 != 0:
                continue

            midpoint = len(product_id) // 2
            if product_id[:midpoint] == product_id[midpoint:]:
                total += i

    return total

def any_repeating_sequence(product_id:int) -> bool:
    # could do this with ints, but don't want to think through edge cases
    product_id = str(product_id)
    product_id_len = len(product_id)

    for sequence_length in range(1, product_id_len // 2 + 1):
        if product_id_len % sequence_length == 0:
            sequences = [product_id[x:x+sequence_length] for x in range(0, product_id_len, sequence_length)]
            all_match = True
            for sequence in sequences:
                all_match &= sequence == sequences[0]

            if all_match:
                return True

    return False

def solve_part_2(ranges):
    total = 0
    for r in ranges:
        for i in range(r[0], r[1]+1):
            if any_repeating_sequence(i):
                total += i

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
