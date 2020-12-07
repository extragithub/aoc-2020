#!/usr/bin/env python3

import re




with open("input.txt", "r") as openfile:
    data = openfile.read()

holds = dict()
held = dict()

for line in [line for line in data.split("\n") if len(line) > 0]:
    attr, color, _, _, contents = line.split(" ", 4)
    bag = f"{attr} {color}"

    holds[bag] = list()
    if not contents.startswith("no"):
        for rule in [rule.strip() for rule in contents.split(",")]:
            count, attr, color, _ = rule.split(" ", 3)

            sub_bag = f"{attr} {color}"
            holds[bag] += [sub_bag] * int(count)

            if not sub_bag in held:
                held[sub_bag] = list()
            held[sub_bag].append(bag)

def held_by(held, bag, containers=None):
    if containers is None:
        containers = set()

    if not bag in held:
        return containers

    for parent in held[bag]:
        containers.add(parent)
        held_by(held, parent, containers)

    return containers

bag = "shiny gold"
bag_held_by = held_by(held, bag)
print(bag, len(bag_held_by))

def hold_count(holds, bag):
    count = 0

    if not bag in holds:
        return count

    for held_bag in holds[bag]:
        count += (hold_count(holds, held_bag) + 1)

    return count

bag_hold_count = hold_count(holds, bag)
print(bag, bag_hold_count)




