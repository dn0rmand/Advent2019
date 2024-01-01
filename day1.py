import math

def day1():
    def loadData():
        with open('data/day1.data', 'rt') as file:
            return [int(line) for line in file]

    def part1(masses):
        return sum((math.floor(mass/3) - 2 for mass in masses))

    def getFuel(mass):
        fuel = 0 if mass < 1 else math.floor(mass/3) - 2
        return 0 if fuel < 1 else fuel + getFuel(fuel)

    def part2(masses):
        return sum((getFuel(mass) for mass in masses))

    print("")
    print("*******************************")
    print("* Advent of Code 2019 - Day 1 *")
    print("*******************************")
    print("")

    masses = loadData()
    print("Answer part 1 is", part1(masses))
    print("Answer part 2 is", part2(masses))

    print("")
