#!/usr/bin/env python3

import copy


def yield_surrounding(seats, coords):
    x = coords[0]
    y = coords[1]

    for off_x in [-1, 0, 1]:
        for off_y in [-1, 0, 1]:
            x2 = coords[0] + off_x
            y2 = coords[1] + off_y

            if (
                y2 >= 0
                and x2 >= 0
                and y2 < len(seats)
                and x2 < len(seats[0])
                and not (x == x2 and y == y2)
            ):
                yield seats[y2][x2]


def will_be_empty(seats, coords):
    seat = seats[coords[1]][coords[0]]
    if not seat == "#":
        return False

    if [seat for seat in yield_surrounding(seats, coords)].count("#") >= 4:
        return True

    return False


def will_be_occupied(seats, coords):
    seat = seats[coords[1]][coords[0]]
    if not seat == "L":
        return False

    if "#" in yield_surrounding(seats, coords):
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
    rows = input_data.tokens
    seats = [[char for char in row] for row in rows]

    previous = 0
    while True:

        # print("-" * 20)
        # print("\n".join(["".join(row) for row in seats]))

        seats, occupied = run_pass(seats)
        if occupied == previous:
            break
        else:
            previous = occupied

    return str(previous)
