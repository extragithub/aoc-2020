#!/usr/bin/env python3

def parse_rules(rules):
    out = dict()
    valid = set()

    for rule in rules:
        field, ranges = rule.split(":")
        out[field] = set()

        for val_range in ranges.strip().split(" or "):
            lower, upper = val_range.split("-")
            for val in range(int(lower), int(upper) + 1):
                out[field].add(val)
                valid.add(val)

    return (out, valid)

def parse_input(input_data):
    rules = []
    yours = None
    nearby = []

    mode = 0
    for row in input_data:
        if len(row) == 0:
            mode += 1
            continue

        if row in ["your ticket:", "nearby tickets:"]:
            continue

        if mode == 0:
            rules.append(row)
        elif mode == 1:
            yours = [int(val) for val in row.split(",")]
        else:
            nearby.append([int(val) for val in row.split(",")])

    return (rules, yours, nearby)

def solve_puzzle(input_data):
    rules, yours, nearby = parse_input(input_data)
    rules, valid = parse_rules(rules)

    total = 0
    for ticket in nearby:
        for val in ticket:
            if not val in valid:
                total += val

    return total

