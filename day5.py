from IntCode import IntCode

def day5():

    def part1(program: IntCode) -> int:
        def input():
            while True:
                yield 1

        lastValue = 0

        def output(value):
            nonlocal lastValue
            if not lastValue == 0:
                raise Exception("Tests failed")
            lastValue = value

        program.initialize(input(), output)
        program.execute()

        return lastValue

    def part2(program: IntCode) -> int:
        def input():
            while True:
                yield 5

        lastValue = None

        def output(value):
            nonlocal lastValue
            if not lastValue == None:
                raise Exception("Tests failed")
            lastValue = value

        program.initialize(input(), output)
        program.execute()

        return lastValue

    print("")
    print("*******************************")
    print("* Advent of Code 2019 - Day 5 *")
    print("*******************************")
    print("")

    program = IntCode('data/day5.data')

    print("Answer part 1 is", part1( program ))
    print("Answer part 2 is", part2( program ))

    print("")
