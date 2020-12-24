#!/usr/bin/env python3


def allergen_split(ingredients, allergen_map):
    allergen_danger = set.union(
        *[ingredients for _, ingredients in allergen_map.items()]
    )
    return allergen_danger, ingredients - allergen_danger


def parse_food(line):
    ingredients, allergens = line.split("(")
    ingredients = set(ingredients.split())

    _, allergens = allergens.strip(")").split(" ", 1)
    allergens = [allergen.strip() for allergen in allergens.split(",")]

    return {allergen: ingredients for allergen in allergens}


def parse_foods(lines):
    combined_map = dict()

    all_ingredients = set()
    for line in lines:
        allergen_map = parse_food(line)

        for allergen, ingredients in allergen_map.items():
            all_ingredients.update(ingredients)
            if allergen in combined_map:
                combined_map[allergen] = combined_map[allergen].intersection(
                    ingredients
                )
            else:
                combined_map[allergen] = ingredients

    return all_ingredients, combined_map


def solve_puzzle(input_data):
    foods = [line for line in input_data if len(line) > 0]

    ingredients, allergen_map = parse_foods(foods)
    _, allergen_safe = allergen_split(ingredients, allergen_map)

    count = 0
    for food in foods:
        for safe in allergen_safe:
            if safe in food.split():
                count += 1

    return count
