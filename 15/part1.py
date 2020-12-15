#!/usr/bin/env python3

from collections import defaultdict


def last_spoken(nums):
    for index in range(len(nums) - 2, -1, -1):
        num = nums[index]
        if num == nums[-1]:
            return len(nums) - index - 1
    raise Exception()


def yield_nums(nums, stop=100):
    spoken = defaultdict(int)
    for num in nums:
        spoken[num] += 1

    counter = 0
    while True:
        counter += 1
        if counter > stop:
            return

        if spoken[nums[-1]] == 1:
            nums.append(0)

        else:
            distance = last_spoken(nums)
            nums.append(distance)

        spoken[nums[-1]] += 1
        yield nums[-1]


def solve_puzzle(input_data):
    nums = [int(num) for num in input_data[0].split(",")]

    final = 0
    for num in yield_nums(nums, 2020 - len(nums)):
        final = num

    return final
