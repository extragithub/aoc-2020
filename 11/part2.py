#!/usr/bin/env python3

import copy


DIRECTIONS = [
    [1, 0],
    [1, 1],
    [0, 1],
    [-1, 1],
    [-1, 0],
    [-1, -1],
    [0, -1],
    [1, -1],
]


def yield_vector(seats, coords, direction, stop=[]):
    x = coords[0] + direction[0]
    y = coords[1] + direction[1]

    while x >= 0 and y >= 0 and x < len(seats[0]) and y < len(seats):
        if seats[y][x] in stop:
            yield seats[y][x]
            x = y = -1
        else:
            yield seats[y][x]
            x += direction[0]
            y += direction[1]


def will_be_empty(seats, coords):
    if not seats[coords[1]][coords[0]] == "#":
        return False

    count = 0
    for direction in DIRECTIONS:
        vector = [val for val in yield_vector(seats, coords, direction, "#L")]
        if "#" in vector:
            count += 1

        if count >= 5:
            return True

    return False


def will_be_occupied(seats, coords):
    if not seats[coords[1]][coords[0]] == "L":
        return False

    for direction in DIRECTIONS:
        vector = [val for val in yield_vector(seats, coords, direction, "#L")]
        if "#" in vector:
            return False

    return True


def run_pass(seats):
    updated = copy.deepcopy(seats)
    occupied = 0

    for x in range(len(seats[0])):
        for y in range(len(seats)):
            coords = (x, y)

            if will_be_occupied(seats, coords):
                updated[y][x] = "#"
                occupied += 1
            elif will_be_empty(seats, coords):
                updated[y][x] = "L"
            else:
                updated[y][x] = seats[y][x]
                if updated[y][x] == "#":
                    occupied += 1

    return updated, occupied


def solve_puzzle(input_data):
    rows = input_data.split("\n")
    seats = [[char for char in row] for row in rows]

    occupied = 0
    previous = 0

    while True:
        seats, occupied = run_pass(seats)

        # print("-" * 20)
        # print("\n".join(["".join(row) for row in seats]))
        # print(previous, occupied)

        if occupied == previous:
            break
        else:
            previous = occupied

    return str(previous)
