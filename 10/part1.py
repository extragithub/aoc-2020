#!/usr/bin/env python3

from collections import defaultdict


get_valid = lambda adapters, rating: sorted([
    adapter for adapter in adapters if adapter > rating and adapter <= rating + 3
])


with open("input.txt", "r") as openfile:
    data = openfile.read()

adapters = sorted([int(adapter) for adapter in data.split("\n") if len(adapter) > 0])
adapters.append(max(adapters) + 3)


differences = defaultdict(int)
rating = 0
for index in range(len(adapters)):
    valid = get_valid(adapters, rating)
    differences[valid[0] - rating] += 1
    rating = valid[0]

print(differences)
print(differences[3] * differences[1])

