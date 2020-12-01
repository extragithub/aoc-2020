#!/usr/bin/env python3

with open("input.txt", "r") as openfile:
    data = openfile.read()

numbers = [int(num) for num in data.split("\n") if len(num) > 0]
for first in range(len(numbers)):
    for second in range(first + 1, len(numbers)):
        if numbers[first] + numbers[second] == 2020:
            print(numbers[first], numbers[second], numbers[first] * numbers[second])

for first in range(len(numbers)):
    for second in range(first + 1, len(numbers)):
        for third in range(second + 1, len(numbers)):
            if numbers[first] + numbers[second] + numbers[third] == 2020:
                print(numbers[first], numbers[second], numbers[third], numbers[first] * numbers[second] * numbers[third])
