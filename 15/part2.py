#!/usr/bin/env python3

from collections import defaultdict


def yield_nums(nums, stop=100):
    spoken = defaultdict(lambda: -1)
    for index in range(len(nums) - 1):
        spoken[nums[index]] = index

    counter = 0
    while True:
        counter += 1
        if counter > stop:
            return

        if spoken[nums[-1]] == -1:
            spoken[nums[-1]] = len(nums) - 1
            nums.append(0)

        else:
            distance = len(nums) - spoken[nums[-1]] - 1
            spoken[nums[-1]] = len(nums) - 1
            nums.append(distance)

        yield nums[-1]


def solve_puzzle(input_data):
    nums = [int(num) for num in input_data[0].split(",")]

    final = 0
    for num in yield_nums(nums, 30000000 - len(nums)):
        final = num

    return final
