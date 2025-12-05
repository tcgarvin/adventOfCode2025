import argparse
from rich import print

EXAMPLE_FILE_NAME = "example.txt"
INPUT_FILE_NAME= "input.txt"

def get_puzzle_input(use_example=False):
    input_filename = EXAMPLE_FILE_NAME if use_example else INPUT_FILE_NAME
    puzzle_input = []
    with open(input_filename) as input_txt:
        ranges = []
        items = []
        for line in input_txt:
            line = line.strip()
            if "-" in line:
                r = tuple(map(int, line.split("-")))
                assert r[0] <= r[1]
                ranges.append(r)
            elif len(line) > 0:
                items.append(int(line))
    return ranges, items

def solve_part_1(ranges, items):
    fresh_items = 0
    for item in items:
        for range in ranges:
            if item >= range[0] and item <= range[1]:
                fresh_items += 1
                break
    return fresh_items

def ranges_intersect(a:tuple[int,int], b:tuple[int, int]) -> bool:
    return a[0] <= b[1] and a[1] >= b[0]

def combine_ranges(a:tuple[int,int], b:tuple[int, int]) -> tuple[int,int]:
    return (min(a[0], b[0]), max(a[1], b[1]))

def solve_part_2(ranges, _):
    uncleared_ranges = set(ranges)
    cleared_ranges = []
    while len(uncleared_ranges) > 0:
        range_to_check = uncleared_ranges.pop()

        found_intersection = False
        for other_range in list(uncleared_ranges):
            if ranges_intersect(range_to_check, other_range):
                found_intersection = True
                range_to_check = combine_ranges(range_to_check, other_range)
                uncleared_ranges.remove(other_range)

        if found_intersection:
            uncleared_ranges.add(range_to_check)
        else:
            cleared_ranges.append(range_to_check)

    return sum(r[1] - r[0] + 1 for r in cleared_ranges)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    ranges, items = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(ranges, items)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(ranges, items)
    print(f"Part 2: {answer_2}")
