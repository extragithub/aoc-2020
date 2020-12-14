#!/usr/bin/env python3

from collections import defaultdict
import itertools

MEMORY = defaultdict(int)


def apply_mask(mask, bits):
    val = []
    for m, b in zip(mask, bits):
        if m == 0:
            val.append(b)
        elif m == 1:
            val.append(1)
        elif m == "X":
            val.append("X")
        else:
            raise Exception()
    return val


def to_bits(val):
    return [int(char) for char in f"{val:0>36b}"]


def to_int(bits):
    return int("".join([str(val) for val in bits]), 2)


def to_mask(val):
    mask = []
    for char in val:
        if char == "X":
            mask.append(char)
        else:
            mask.append(int(char))
    return mask


def yield_combos(xs):
    combos = list(itertools.product([0, 1], repeat=len(xs)))
    for combo in combos:
        yield (xs, combo)


def set_values(memory, floating, value):
    xs = []
    for index in range(len(floating)):
        if floating[index] == "X":
            xs.append(index)

    for index, val in yield_combos(xs):
        for i, v in zip(index, val):
            floating[i] = v
        memory[to_int(floating)] = to_int(value)


def solve_puzzle(input_data):
    for instruction in input_data:
        if len(instruction) == 0:
            continue

        print(instruction)
        instruction, val = instruction.split("=")

        if instruction.startswith("mask"):
            mask = to_mask(val.strip())

        elif instruction.startswith("mem"):
            _, address = instruction.split("[")

            address = int(address.strip("] "))
            address = to_bits(address)

            val = to_bits(int(val.strip()))

            floating = apply_mask(mask, address)
            set_values(MEMORY, floating, val)

    total = 0
    for address, val in MEMORY.items():
        total += val

    return total
