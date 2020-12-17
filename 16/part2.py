#!/usr/bin/env python3

from part1 import parse_input, parse_rules

def check_field_order(order, rules, tickets):
    for ticket in tickets:
        for index in range(len(ticket)):
            if ticket[index] not in rules[order[index]]:
                return False
    return True


def solve_puzzle(input_data):
    rules, yours, nearby = parse_input(input_data)
    rules, valid = parse_rules(rules)

    # filter out invalid tickets
    valid_tickets = []
    for ticket in nearby:
        valid_ticket = True
        for val in ticket:
            if not val in valid:
                valid_ticket = False
                break

        if valid_ticket:
            valid_tickets.append(ticket)

    field_positions = dict()
    for field, positions in rules.items():
        field_positions[field] = set()

        for position in range(len(rules)):

            found_position = True
            for ticket in valid_tickets:
                if ticket[position] not in positions:
                    found_position = False
                    break

            if found_position:
                field_positions[field].add(position)

    pinned = dict()
    count = 0
    while len(pinned) < len(field_positions):
        count += 1

        found = None
        for field in field_positions:
            if len(field_positions[field]) == 1:
                found = field_positions[field].pop()
                pinned[field] = found
                break

        if found:
            for field in field_positions:
                if len(field_positions[field]) > 0:
                    field_positions[field].remove(found)
            found = None

        if count > 22:
            break

    missing = [field for field in rules if not field in pinned]

    # okay... getting tired, just brute force the remaining values
    for ap_val in field_positions["arrival platform"]:
        for at_val in field_positions["arrival track"]:
            for p_val in field_positions["price"]:
                for r_val in field_positions["row"]:
                    for t_val in field_positions["train"]:
                        for w_val in field_positions["wagon"]:
                            order = {
                                    ap_val: "arrival platform",
                                    at_val: "arrival track",
                                    p_val: "price",
                                    r_val: "row",
                                    t_val: "train",
                                    w_val: "wagon",
                            }
                            for field, position in pinned.items():
                                order[position] = field

                            try:
                                check_field_order(order, rules, valid_tickets)

                                total = 1
                                for index, field in order.items():
                                    if field.startswith("departure"):
                                        total *= yours[index]

                                return total

                            except KeyError:
                                pass



