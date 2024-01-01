from IntCode import IntCode

def day9():

    def part1(program: IntCode) -> int:
        def input():
            yield 1
            raise Exception("Tests failed")

        lastValue = None

        def output(value):
            nonlocal lastValue
            if not lastValue == None:
                raise Exception("Tests failed")
            lastValue = value

        program.initialize(input(), output)
        program.execute()

        return lastValue

    def part2(program: IntCode) -> int:
        def input():
            yield 2
            raise Exception("Tests failed")

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
    print("* Advent of Code 2019 - Day 9 *")
    print("*******************************")
    print("")

    program = IntCode('data/day9.data')

    print("Answer part 1 is", part1( program ))
    print("Answer part 2 is", part2( program ))

    print("")
