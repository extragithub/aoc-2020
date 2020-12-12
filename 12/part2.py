#!/usr/bin/env python3

import math


def move(instruction, ship, waypoint):
    action = instruction[0]
    value = int(instruction[1:])

    if action == "N":
        waypoint = (waypoint[0], waypoint[1] + value)
    elif action == "S":
        waypoint = (waypoint[0], waypoint[1] - value)
    elif action == "E":
        waypoint = (waypoint[0] + value, waypoint[1])
    elif action == "W":
        waypoint = (waypoint[0] - value, waypoint[1])
    elif action in "LR":
        if value == 180:
            waypoint = (-waypoint[0], -waypoint[1])
        elif (action == "L" and value == 90) or (action == "R" and value == 270):
            waypoint = (-waypoint[1], waypoint[0])
        elif (action == "L" and value == 270) or (action == "R" and value == 90):
            waypoint = (waypoint[1], -waypoint[0])
    elif action == "F":
        ship = (ship[0] + (waypoint[0] * value), ship[1] + (waypoint[1] * value))

    return ship, waypoint


def solve_puzzle(input_data):
    ship = (0, 0)
    waypoint = (10, 1)
    for instruction in input_data.tokens:
        ship, waypoint = move(instruction, ship, waypoint)

    mdistance = abs(ship[0]) + abs(ship[1])
    return str(mdistance)
