#!/usr/bin/env python3

def next_bus(bus_number, timestamp):
    val = 0
    while val < timestamp:
        val += bus_number
    return val

def solve_puzzle(input_data):
    timestamp = int(input_data[0])
    buses = input_data[1].split(",")

    schedule = []
    for bus in buses:
        if bus != "x":
            bus_num = int(bus)
            schedule.append((bus_num, next_bus(bus_num, timestamp)))

    bus_num, arrival = min(schedule, key=lambda sched: sched[1])
    return (bus_num * (arrival - timestamp))

