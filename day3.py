import math

def day3():

    map = {}

    intersections = []

    def addPoint(x, y, value, wire):
        key = (x, y)
        if key in map:
            v , w = map.get(key)
            if w != wire:
                if x != 0 or y != 0:
                    intersections.append((x, y))
                value += v
            else:
                value = min(v, value)

        map[key] = (value, wire)

    def loadData():

        with open('data/day3.data', 'rt') as file:
            wire = 0
            for line in file:
                wire += 1

                x, y, step  = 0, 0, 0

                for move, value in ( (x[0], int(x[1:])) for x in line.split(',') ):
                    xx = -1 if move == 'L' else 1 if move == 'R' else 0
                    yy = -1 if move == 'U' else 1 if move == 'D' else 0
                    if xx == 0 and yy == 0:
                        raise Exception('Invalid move')

                    for _ in range(0, value):
                        step += 1
                        y += yy
                        x += xx
                        addPoint(x, y, step, wire)

    def part1():
        return min(( abs(x)+abs(y) for x, y in intersections ))

    def part2():
        return min(( s for s ,_ in ( map.get((x, y)) for x, y in intersections )))

    print("")
    print("*******************************")
    print("* Advent of Code 2019 - Day 3 *")
    print("*******************************")
    print("")

    loadData()

    print("Answer part 1 is", part1())
    print("Answer part 2 is", part2())

    print("")
