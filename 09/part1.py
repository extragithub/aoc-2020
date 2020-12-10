#!/usr/bin/env python3

PREAMBLE_LEN = 25
with open("input.txt", "r") as openfile:
    data = openfile.read()

def generate_valid(preamble):
    for a in range(len(preamble)):
        for b in range(a + 1, len(preamble)):
            yield preamble[a] + preamble[b]

def is_valid(preamble, value):
    return (value in generate_valid(preamble))

data_stream = [int(line) for line in data.split("\n") if len(line) > 0]
offset = 0
for index in range(0, len(data_stream) - PREAMBLE_LEN + 1):
    offset = index + PREAMBLE_LEN
    value = data_stream[offset]
    valid = is_valid(data_stream[index:offset], value)

    if not valid:
        print(value)
        break
