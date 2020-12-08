#!/usr/bin/env python3

class Computer:

    @staticmethod
    def acc(cursor, acc, val):
        return (cursor + 1, acc + val)

    @staticmethod
    def jmp(cursor, acc, val):
        return (cursor + val, acc)

    @staticmethod
    def nop(cursor, acc, val):
        return (cursor + 1, acc)

    @classmethod
    def run(cls, program):
        accumulator = 0
        cursor = 0
        visited = [False] * len(program)

        while True:
            if visited[cursor] == True:
                break

            instruction = program[cursor]
            visited[cursor] = True

            cmd, val = instruction.split()
            if val[0] == "+":
                val = int(val[1:])
            else:
                val = -1 * int(val[1:])

            fn = getattr(cls, cmd)
            cursor, accumulator = fn(cursor, accumulator, val)

            if cursor > len(program) - 1:
                raise StopIteration(accumulator)


        return accumulator


with open("input.txt", "r") as openfile:
    data = openfile.read()

program = [line for line in data.split("\n") if len(line) > 0]
comp = Computer()

print(comp.run(program))

