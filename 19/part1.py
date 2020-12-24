#!/usr/bin/env python3

import re

from collections import defaultdict


def resolve_sub_rule(rules, index):
    if isinstance(index, int):
        if isinstance(rules[index], str):
            ret = rules[index]
            return ret

        elif isinstance(rules[index], list):
            ret = "({})".format(
                "|".join(
                    [resolve_sub_rule(rules, sub_rule) for sub_rule in rules[index]]
                )
            )
            return ret

        else:
            raise Exception()

    elif isinstance(index, list):
        ret = "".join([resolve_sub_rule(rules, sub_rule) for sub_rule in index])
        return ret

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


def translate_rules(rules):
    translated = dict()
    for rule in rules:
        key, val = rule.split(":")
        translated[key] = val.strip(' "')

    # replace all direct character mappings
    char_map = {key: val for key, val in translated.items() if len(val) == 1}

    for key, val in translated.items():
        mapped = f" {val} "
        for map_from, map_to in char_map.items():
            map_from = f" {map_from} "
            map_to = f" {map_to} "
            mapped = mapped.replace(map_from, map_to)

        if "|" in mapped:
            mapped = f"( {mapped} )"

        translated[key] = mapped

    # do the remaining replacements
    found = True
    while found:
        found = False

        for key, val in translated.items():
            for map_from, map_to in translated.items():
                map_from = f" {map_from} "
                map_to = f" {map_to} "
                if map_from in val:
                    found = True
                    val = val.replace(map_from, map_to)

            translated[key] = val

    return {int(key): val.replace(" ", "") for key, val in translated.items()}


def solve_puzzle(input_data):
    messages = input_data.groups[1]
    rules = parse_rules(input_data.groups[0])

    translated = translate_rules(input_data.groups[0])
    regex = f"{translated[0]}"

    matches = 0
    for message in messages:
        match = re.fullmatch(regex, message)
        if match:
            matches += 1

    return matches
