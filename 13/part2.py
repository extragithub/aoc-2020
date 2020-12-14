#!/usr/bin/env python3

import functools


def start(buses):
    bus_info = []

    for index in range(len(buses)):
        if buses[index] != "x":
            bus_info.append((int(buses[index]), index))

    return bus_info


def solve_puzzle(input_data):
    buses = input_data[1].split(",")

    bus_info = start(buses)
    print(bus_info)

    # set initial info
    bus = bus_info[0]

    step = bus[0]
    timestamp = 0

    for bus in bus_info[1:]:
        while (timestamp + bus[1]) % bus[0] != 0:
            timestamp += step
        step *= bus[0]

    return timestamp
