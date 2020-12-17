#!/usr/bin/env python3

from collections import defaultdict


def get_neighbors(cube, coords):
    (x1, y1, z1, w1) = coords
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            for z in [-1, 0, 1]:
                for w in [-1, 0, 1]:
                    if not (x == 0 and y == 0 and z == 0 and w == 0):
                        yield cube[(x1 + x, y1 + y, z1 + z, w1 + w)]


def next_state(cube, coords):
    neighbors = [n for n in get_neighbors(cube, coords)]
    active = neighbors.count("#")

    if cube[coords] == "#":
        if not (active == 2 or active == 3):
            return "."

    else:
        if active == 3:
            return "#"


def current_size(cube):
    max_x = 0
    min_x = 0
    max_y = 0
    min_y = 0
    max_z = 0
    min_z = 0
    max_w = 0
    min_w = 0

    for coords in cube:
        if coords[0] > max_x:
            max_x = coords[0]
        if coords[0] < min_x:
            min_x = coords[0]
        if coords[1] > max_y:
            max_y = coords[1]
        if coords[1] < min_y:
            min_y = coords[1]
        if coords[2] > max_z:
            max_z = coords[2]
        if coords[2] < min_z:
            min_z = coords[2]
        if coords[3] > max_w:
            max_w = coords[3]
        if coords[3] < min_w:
            min_w = coords[3]

    return (min_x, max_x, min_y, max_y, min_z, max_z, min_w, max_w)


def next_cycle(cube):
    (min_x, max_x, min_y, max_y, min_z, max_z, min_w, max_w) = current_size(cube)

    updates = dict()
    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 2):
            for z in range(min_z - 1, max_z + 2):
                for w in range(min_w - 1, max_w + 2):
                    update = next_state(cube, (x, y, z, w))
                    if update:
                        updates[(x, y, z, w)] = update

    cube.update(updates)


def print_cube(cube):
    (min_x, max_x, min_y, max_y, min_z, max_z) = current_size(cube)

    for z in range(min_z, max_z + 1):

        cube_str = ""

        for y in range(min_y, max_y + 1):
            row_str = f" {y: >4} | "

            for x in range(min_x, max_x + 1):
                row_str += cube[(x, y, z)]

            if "#" in row_str:
                cube_str += row_str + "\n"

        if "#" in cube_str:
            print("{:-^80}".format(f"> Z = {z} <"))
            print(cube_str + "\n")


def solve_puzzle(input_data):
    cube = defaultdict(lambda: ".")

    rows = [row for row in input_data if len(row) > 0]
    size = len(rows)
    offset = int(size / 2)

    for y in range(len(rows)):
        for x in range(len(rows[y])):
            if rows[y][x] == "#":
                cube[(x - offset, y - offset, 0, 0)] = "#"

    # print("=" * 80)
    # print_cube(cube)
    for _ in range(6):
        # print("=" * 80)
        next_cycle(cube)
        # print_cube(cube)
    # print("=" * 80)

    active_cubes = 0
    for _, char in cube.items():
        if char == "#":
            active_cubes += 1

    return active_cubes
