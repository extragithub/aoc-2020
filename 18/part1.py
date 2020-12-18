#!/usr/bin/env python3


def solve_line(line, value, index):
    operator = "+"
    num_buffer = None

    while index < len(line):

        if line[index] == " ":
            if num_buffer:
                num = int(num_buffer)
                if operator == "+":
                    value += num
                else:
                    value *= num
                num_buffer = None

            index += 1
            continue

        if line[index] in ["+", "*"]:
            operator = line[index]
            index += 1
            continue

        if line[index] == "(":
            val, index = solve_line(line, 0, index + 1)
            if operator == "+":
                value += val
            else:
                value *= val

            continue

        if line[index] == ")":
            if num_buffer:
                num = int(num_buffer)
                if operator == "+":
                    value += num
                else:
                    value *= num
                num_buffer = None

            return value, index + 1

        if num_buffer == None:
            num_buffer = line[index]
        else:
            num_buffer += line[index]

        index += 1

    return value


def solve_puzzle(input_data):
    results = []
    for line in [line for line in input_data if len(line) > 0]:
        results.append(solve_line(line + " ", 0, 0))

    return sum(results)
