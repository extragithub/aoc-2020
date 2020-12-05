#!/usr/bin/env python3

import math


def get_row(code, rows=128):
    max_row = rows - 1
    min_row = 0
    for char in code[:7]:
        if char == "F":
            max_row = math.floor(max_row - ((max_row - min_row) / 2))
        elif char == "B":
            min_row = math.ceil(min_row + ((max_row - min_row) / 2))
        else:
            raise ValueError(f"Invalid row code: {code}")
    assert max_row == min_row
    return max_row


def get_seat(code, seats=8):
    max_seat = seats - 1
    min_seat = 0
    for char in code[7:10]:
        if char == "L":
            max_seat = math.floor(max_seat - ((max_seat - min_seat) / 2))
        elif char == "R":
            min_seat = math.ceil(min_seat + ((max_seat - min_seat) / 2))
        else:
            raise ValueError(f"Invalid row code: {code}")
    assert max_seat == min_seat
    return max_seat


def get_id(code, rows=128, seats=8):
    row = get_row(code, rows)
    seat = get_seat(code, seats)
    return (row * seats) + seat


with open("input.txt", "r") as openfile:
    data = openfile.read()

seat_ids = [
    get_id(boarding_pass)
    for boarding_pass in data.split("\n")
    if len(boarding_pass) > 0
]
print("Highest boarding pass seat ID:\n  ", max(seat_ids))

before = after = None
for seat_id in sorted(seat_ids):
    if seat_id > min(seat_ids) and seat_id - 1 not in seat_ids:
        before = seat_id

    if seat_id < max(seat_ids) and seat_id + 1 not in seat_ids:
        after = seat_id

print("Seat ID:\n  ", int((before + after) / 2))
