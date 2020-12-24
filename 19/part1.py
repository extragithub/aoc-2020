#!/usr/bin/env python3

import re

from collections import defaultdict


def resolve_sub_rule(rules, index):
    if isinstance(index, int):
        if isinstance(rules[index], str):
            # print("LOOKUP", rules, index)
            return rules[index]

        elif isinstance(rules[index], list):
            # print("OR", rules, index)
            return "({})".format(
                "|".join(
                    [resolve_sub_rule(rules, sub_rule) for sub_rule in rules[index]]
                )
            )

        else:
            raise Exception()

    elif isinstance(index, list):
        # print("AND", rules, index)
        return "".join([resolve_sub_rule(rules, sub_rule) for sub_rule in index])

    else:
        raise Exception()


def parse_rules(rules):
    parsed = defaultdict(list)

    for rule in rules:
        num, sub_rule_str = rule.split(":")

        section_rules = sub_rule_str.strip().split("|")
        if len(section_rules) == 1:
            try:
                parsed[int(num)] = [
                    int(val) for val in section_rules[0].strip().split()
                ]

            except ValueError as error:
                parsed[int(num)] = section_rules[0].strip().strip('"')

        else:
            for section_rule in section_rules:
                try:
                    parsed[int(num)].append(
                        [int(val) for val in section_rule.strip().split()]
                    )

                except ValueError as error:
                    parsed[int(num)].append(section_rule.strip().strip('"'))

    return parsed


def solve_puzzle(input_data):
    messages = input_data.groups[1]
    rules = parse_rules(input_data.groups[0])

    regex = "^{}$".format(
        "".join([resolve_sub_rule(rules, sub_rule) for sub_rule in rules[0]])
    )
    print(regex)

    valid = list()
    for message in messages:
        print(re.match(regex, message))
        if re.match(regex, message):
            valid.append(message)

    return len(valid)
