#!/usr/bin/env python3

import part1

def is_valid(data, offset, value):
    total = 0
    for index in range(offset, len(data)):
        if total == value:
            return data[offset:index]
        if data[index] > value or total > value:
            return None
        total += data[index]

value = part1.data_stream[part1.offset]
for index in range(0, part1.offset + 1):
    nums = is_valid(part1.data_stream, index, value)
    if nums:
        print(min(nums) + max(nums))
        break
