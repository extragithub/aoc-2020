#!/usr/bin/env python3

def _update_axis(a, b, size=None):
    val = a + b
    if size:
        val = val % size
    return val

def _update_coords(a, b, width):
    return (_update_axis(a[0], b[0], width), _update_axis(a[1], b[1]))

class Toboggan:

    def __init__(self, x, y):
        self.x_ = x
        self.y_ = y

    @property
    def angle(self):
        return (self.x_, self.y_)

    def run(self, slope):
        slope = slope.split("\n")

        hill_height = len(slope)
        slope_width = len(slope[0])

        position = (0, 0)
        while position[1] < hill_height:
            yield slope[position[1]][position[0]]
            position = _update_coords(position, self.angle, slope_width)


with open("input.txt", "r") as openfile:
    slope = openfile.read().strip()

toboggan = Toboggan(3, 1)
moves = [move for move in toboggan.run(slope)]
print(moves.count("#"))



results = {}
for angle in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    toboggan = Toboggan(angle[0], angle[1])
    moves = [move for move in toboggan.run(slope)]
    results[angle] = moves.count("#")

product = 1
for angle, trees in results.items():
    product = product * trees
print(product)
