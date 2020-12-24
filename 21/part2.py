#!/usr/bin/env python3

import part1


def reduce_allergen_map(allergen_map):
    reduced_map = dict()
    while len(allergen_map) > 0:
        reduced = list()

        for allergen, ingredients in allergen_map.items():
            if len(ingredients) == 1:
                reduced.append(allergen)
                reduced_map[allergen] = ingredients.pop()

            else:
                for a in [a for a in reduced_map if reduced_map[a] in ingredients]:
                    ingredients.remove(reduced_map[a])
                allergen_map[allergen] = ingredients

        for allergen in reduced:
            allergen_map.pop(allergen)

    return {value: key for key, value in reduced_map.items()}


def solve_puzzle(input_data):
    foods = [line for line in input_data if len(line) > 0]

    ingredients, allergen_map = part1.parse_foods(foods)
    allergen_map = reduce_allergen_map(allergen_map)

    return ",".join(sorted(allergen_map, key=lambda allergen: allergen_map[allergen]))
