#!/usr/bin/env python3

from collections import defaultdict

MEMORY = defaultdict(int)


def apply_mask(mask, bits):
    val = []
    for m, b in zip(mask, bits):
        if m == "X":
            val.append(b)
        else:
            val.append(m)
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
            bits = to_bits(int(val.strip()))
            MEMORY[address] = apply_mask(mask, bits)

    total = 0
    for address, val in MEMORY.items():
        val = to_int(val)
        print(f"[{address}]: {val}")
        total += val

    return total
