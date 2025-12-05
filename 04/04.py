import argparse
from rich import print
from grid import Grid, Vector, grid_from_input_txt, ALL_DIRECTION_VECTORS, print_grid

EXAMPLE_FILE_NAME = "example.txt"
INPUT_FILE_NAME= "input.txt"

def get_puzzle_input(use_example=False):
    input_filename = EXAMPLE_FILE_NAME if use_example else INPUT_FILE_NAME
    with open(input_filename) as input_txt:
        return grid_from_input_txt(input_txt.read())

def is_accessable(grid:Grid, roll_location:Vector) -> bool:
    adjacent_roll_count = 0
    for direction in ALL_DIRECTION_VECTORS:
        if grid[roll_location + direction] == "@":
            adjacent_roll_count += 1

    return adjacent_roll_count < 4

def get_accessable_rolls(grid:Grid) -> set[Vector]:
    accessable_rolls = set()
    for roll in grid.find("@"):
        if is_accessable(grid, roll):
            accessable_rolls.add(roll)

    return accessable_rolls


def solve_part_1(grid: Grid):
    return len(get_accessable_rolls(grid))

def solve_part_2(grid:Grid):
    done = False
    while done is False:
        accessable_rolls = get_accessable_rolls(grid)
        for roll in accessable_rolls:
            grid[roll] = "x"

        if len(accessable_rolls) == 0:
            done = True

    print_grid(grid)

    return sum(1 for _ in grid.find("x"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
