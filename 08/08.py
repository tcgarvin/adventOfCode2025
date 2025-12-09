import argparse
from itertools import combinations
from heapq import nsmallest, nlargest
from math import sqrt
from rich import print


EXAMPLE_FILE_NAME = "example.txt"
INPUT_FILE_NAME= "input.txt"

Point = tuple[int,int,int]

def get_puzzle_input(use_example=False):
    input_filename = EXAMPLE_FILE_NAME if use_example else INPUT_FILE_NAME
    puzzle_input = []
    with open(input_filename) as input_txt:
        for line in input_txt:
            puzzle_input.append(tuple(int(x) for x in line.split(",")))
    return puzzle_input

def get_distance(a:Point,b:Point) -> float:
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)

def get_sortable_connection(a:Point, b:Point) -> tuple[float, Point, Point]:
    return (get_distance(a,b), a, b)


def solve_part_1(puzzle_input):
    distance_generator = (get_sortable_connection(a,b) for a,b in combinations(puzzle_input, 2))


    clusters = [set((p,)) for p in puzzle_input]
    for _, a, b in nsmallest(1000, distance_generator):
        cluster_a = next(filter(lambda c: a in c, clusters))
        cluster_b = next(filter(lambda c: b in c, clusters))
        if cluster_a is cluster_b:
            continue

        cluster_a |= cluster_b
        clusters.remove(cluster_b)

    total = 1
    for cluster_size in nlargest(3, (len(c) for c in clusters)):
        total *= cluster_size
    return total


def solve_part_2(puzzle_input):
    distance_generator = (get_sortable_connection(a,b) for a,b in combinations(puzzle_input, 2))

    clusters = [set((p,)) for p in puzzle_input]
    len_clusters = len(clusters)
    for _, a, b in nsmallest(100000, distance_generator):
        cluster_a = next(filter(lambda c: a in c, clusters))
        cluster_b = next(filter(lambda c: b in c, clusters))
        if cluster_a is cluster_b:
            continue

        cluster_a |= cluster_b
        clusters.remove(cluster_b)
        if len(clusters) < len_clusters:
            print(len_clusters)
            len_clusters = len(clusters)

        if len(clusters) == 1:
            return a[0] * b[0]

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
