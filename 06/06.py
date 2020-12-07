#!/usr/bin/env python3


with open("input.txt", "r") as openfile:
    data = openfile.read()

groups = []
group = []
for line in data.split("\n"):
    if line == "":
        groups.append(group)
        group = []
    else:
        group.append(line)

answers = [set("".join(people)) for people in groups]
print(sum([len(answer) for answer in answers]))


def count_group(group):
    choices = set("".join(group))
    people = [set(person) for person in group]
    return choices.intersection(*people)


answers = [count_group(group) for group in groups]
print(sum([len(answer) for answer in answers]))
