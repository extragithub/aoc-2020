#!/usr/bin/env python3

from part1 import *

# create a mask of the joltage ratings that have adapters
ratings = [False] * max(adapters)
ratings.insert(0, True)
for adapter in adapters:
    ratings[adapter] = True

def walk_ratings(ratings, index=0, combinations=0):
    """ walk the combination tree of a group of joltage ratings """
    # reached the end of a branch
    if index == len(ratings) - 1:
        return combinations + 1

    # walk each offset if it doesn't go past the max rating and the joltage is supported
    for offset in (3, 2, 1):
        if index + offset < len(ratings) and ratings[index + offset]:
            combinations = walk_ratings(ratings, index + offset, combinations)

    return combinations

# split adapters into groups divided by joltage differences of 3 and walk each group
adapters.insert(0, 0)
diffs = [b - a for a, b in zip(adapters[:-1], adapters[1:])]

combinations = 1
last = 0
for index in range(len(diffs)):
    if diffs[index] == 3:
        section = adapters[last:index + 1]
        last = index + 1

        combos = walk_ratings(section)
        combinations *= combos

print(combinations)
