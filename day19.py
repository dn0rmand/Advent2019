from IntCode import IntCode

def day19():

    def checkPoint(program: IntCode, x: int, y: int) -> bool:
        result = 0

        def output(code):
            nonlocal result
            result = code

        def input():
            yield x
            yield y

        program.initialize(input(), output)
        program.execute()

        return result

    def part1(program: IntCode, dump: bool = False) -> int:
        count = 0

        for y in range(0, 50):
            for x in range(0, 50):
                c = checkPoint(program, x, y)
                if dump:
                    print('X' if c == 1 else '.', end="")
                count += c
            if dump:
                print("")

        return count

    def part2(program: IntCode) -> int:

        def check(x: int, y: int) -> bool:
            if y < 0:
                return False

            return checkPoint(program, x, y) == 1

        y = None
        x = 50

        for yy in range(49, 0, -1):
            if checkPoint(program, x, yy):
                y = yy
                break

        while True:
            if check(x, y-99) and check(x+99, y-99):
                return x*10000 + (y-99)
            x += 1
            while checkPoint(program, x, y+1):
                y += 1

    print("")
    print("********************************")
    print("* Advent of Code 2019 - Day 19 *")
    print("********************************")
    print("")

    program = IntCode('data/day19.data')

    print("Answer part 1 is", part1(program))
    print("Answer part 2 is", part2(program))