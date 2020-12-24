#!/usr/bin/env python3

import sys


def yield_edges(tile):
    size = range(len(tile[0]))

    # yield edges forwards and backwards (to support flips)
    for step in [1, -1]:
        for index in [0, -1]:
            yield "".join([tile[index][x] for x in size][::step])
            yield "".join([tile[y][index] for y in size][::step])


def print_tile(tile):
    print("-" * len(tile[0]))
    for row in tile:
        for char in row:
            sys.stdout.write(char)
        sys.stdout.write("\n")
    print("-" * len(tile[0]))


def can_be_joined(tile_a, tile_b):
    edges_a = [edge for edge in yield_edges(tile_a)]
    for edge in yield_edges(tile_b):
        if edge in edges_a:
            return True

    return False


def find_matches(tiles):
    matches = dict()

    for check_id, check_grid in tiles.items():

        matches[check_id] = list()
        for tile_id, grid in [
            (tile_id, grid) for tile_id, grid in tiles.items() if tile_id != check_id
        ]:
            if can_be_joined(check_grid, grid):
                matches[check_id].append(tile_id)

    return matches


def parse_input_data(input_data):
    tiles = dict()

    for group in input_data.groups:
        tile_id = int(group[0].split(" ")[1].strip(":"))
        grid = [[char for char in row] for row in group[1:]]

        tiles[tile_id] = grid

    return tiles


def calculate_corner_multiple(matches):
    value = 1
    for tile_id in matches:
        if len(matches[tile_id]) == 2:
            value *= tile_id

    return value


def solve_puzzle(input_data):
    tiles = parse_input_data(input_data)
    matches = find_matches(tiles)

    return calculate_corner_multiple(matches)
