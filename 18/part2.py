#!/usr/bin/env python3


def resolve_stacks(num_stack, operator_stack):
    n_stack = []
    n_stack.append(num_stack[0])
    o_stack = []

    for num, op in zip(num_stack[1:], operator_stack):
        if op == "+":
            num2 = n_stack.pop()
            n_stack.append(num + num2)
        else:
            n_stack.append(num)
            o_stack.append(op)

    while len(n_stack) > 1 and len(o_stack) > 0:
        op = o_stack.pop()
        num1 = n_stack.pop()
        num2 = n_stack.pop()
        n_stack.append(num1 * num2)

    return n_stack[0]


def solve_line(line, index):
    num_buffer = None
    num_stack = list()
    operator_stack = list()

    while index < len(line):
        if line[index] == " ":
            if num_buffer:
                num_stack.append(int(num_buffer))
                num_buffer = None

                if len(operator_stack) > 0 and operator_stack[-1] == "+":
                    operator_stack.pop()
                    num1 = num_stack.pop()
                    num2 = num_stack.pop()

                    num_stack.append(num1 + num2)

            index += 1
            continue

        if line[index] in ["+", "*"]:
            operator_stack.append(line[index])

            index += 1
            continue

        if line[index] == "(":
            val, index = solve_line(line, index + 1)
            num_stack.append(val)
            continue

        if line[index] == ")":
            if num_buffer:
                num_stack.append(int(num_buffer))
                num_buffer = None

                if len(operator_stack) > 0 and operator_stack[-1] == "+":
                    operator_stack.pop()
                    num1 = num_stack.pop()
                    num2 = num_stack.pop()

                    num_stack.append(num1 + num2)

            return resolve_stacks(num_stack, operator_stack), index + 1

        if num_buffer is None:
            num_buffer = line[index]
        else:
            num_buffer += line[index]

        index += 1

    return resolve_stacks(num_stack, operator_stack)


def solve_puzzle(input_data):
    results = []
    for line in [line for line in input_data if len(line) > 0]:
        results.append(solve_line(line + " ", 0))

    return sum(results)
