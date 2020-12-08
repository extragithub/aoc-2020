#!/usr/bin/env python3

import part1

program = part1.program
comp = part1.comp

for index in range(len(program)):
    if program[index][:3] in ["nop", "jmp"]:
        if program[index][:3] == "nop":
            modified_instruction = program[index].replace("nop", "jmp")
        else:
            modified_instruction = program[index].replace("jmp", "nop")

        modified_program = program[:index] + [modified_instruction] + program[index + 1:]
        comp.run(modified_program)
