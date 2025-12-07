import argparse
from functools import cache
from rich import print
from grid import grid_from_input_txt, NORTH, SOUTH, EAST, WEST, Grid, Vector, print_grid

EXAMPLE_FILE_NAME = "example.txt"
INPUT_FILE_NAME= "input.txt"

def get_puzzle_input(use_example=False):
    input_filename = EXAMPLE_FILE_NAME if use_example else INPUT_FILE_NAME
    puzzle_input = []
    with open(input_filename) as input_txt:
        puzzle_input = grid_from_input_txt(input_txt.read(), out_of_bounds="X")
    return puzzle_input

def traverse_beam(grid:Grid, location:Vector):
    next_path = location + SOUTH

    if grid[next_path] == ".":
        grid[next_path] = "|"
        traverse_beam(grid, next_path)
    elif grid[next_path] == "^":
        traverse_beam(grid, next_path + WEST)
        traverse_beam(grid, next_path + EAST)
    elif grid[next_path] in "|X":
        pass
    else:
        raise Exception("Unexpected grid state")

def solve_part_1(grid:Grid):
    # Plan: Make all the beams go
    # Then: Count the splitters that have a beam above them

    start_location = grid.find_one('S')
    traverse_beam(grid, start_location)
    print_grid(grid)

    return sum(grid[split + NORTH] == "|" for split in grid.find("^"))

def solve_part_2(grid:Grid):

    @cache
    def count_possibilities(location:Vector) -> int:
        next_path = location + SOUTH
        next_path_content = grid[next_path]
        if next_path_content in ".|":
            return count_possibilities(next_path)
        if next_path_content == "^":
            count = count_possibilities(next_path + EAST)
            count += count_possibilities(next_path + WEST)
            return count

        return 1

    start_location = grid.find_one("S")

    return count_possibilities(start_location)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
