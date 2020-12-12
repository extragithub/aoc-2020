#!/usr/bin/env python3

import math

COMPASS = ["N", "E", "S", "W"]


def move(instruction, position, facing):
    action = instruction[0]
    value = int(instruction[1:])

    if action == "N":
        position = (position[0], position[1] + value)
    elif action == "S":
        position = (position[0], position[1] - value)
    elif action == "E":
        position = (position[0] + value, position[1])
    elif action == "W":
        position = (position[0] - value, position[1])
    elif action == "L":
        index = COMPASS.index(facing)
        facing = COMPASS[index - int(value / 90)]
    elif action == "R":
        index = COMPASS.index(facing)
        facing = COMPASS[(index + int(value / 90)) % len(COMPASS)]
    elif action == "F":
        position, facing = move(f"{facing}{value}", position, facing)

    return position, facing


def solve_puzzle(input_data):
    position = (0, 0)
    facing = "E"
    for instruction in input_data.tokens:
        position, facing = move(instruction, position, facing)

    mdistance = abs(position[0]) + abs(position[1])
    return str(mdistance)
