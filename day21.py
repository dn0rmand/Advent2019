from IntCode import IntCode
import sys

def day21():

    DEBUG = False
    for arg in sys.argv:
        if arg.lower() == "debug":
            DEBUG = True
            break

    def getDamage(program, solution, speed) -> int:

        damage  = 0
        message = []

        def input():
            for l in solution:
                if len(l) == 0:
                    continue
                for c in l:
                    yield ord(c)
                yield 10
            for c in speed:
                yield ord(c)
            yield 10

        def output(code: int) -> None:
            nonlocal damage

            if code > 255:
                damage = code
            elif code == 10:
                msg = "".join(message)
                if DEBUG:
                    print(msg)
                if msg != "Input instructions:" and msg != "Walking..." and msg != "Running..." and len(msg) > 0:
                    print(msg)
                message.clear()
            else:
                message.append(chr(code))

        program.initialize(input(), output)
        program.execute()

        return damage

    def part1(program: IntCode) -> int:
        solution = [
            "NOT C J",

            "AND D J", # need somewhere to land
            "NOT A T", # last resort ... Jump or fall in hole
            "OR T J"
        ]

        return getDamage(program, solution, "WALK")

    def part2(program: IntCode) -> int:
        solution = [
            "NOT C J",
            "AND H J", # NOT(C) AND H

            "NOT B T",
            "AND C T",
            "AND A T", # NOT(B) AND C AND A

            "OR T J", # (NOT(C) AND H) OR (NOT(B) AND C AND A)

            "AND D J", # need somewhere to land
            "NOT A T", # last resort ... Jump or fall in hole
            "OR T J",
        ]

        return getDamage(program, solution, "RUN")

    print("")
    print("********************************")
    print("* Advent of Code 2019 - Day 21 *")
    print("********************************")
    print("")

    program = IntCode('data/day21.data')

    print("Answer part 1 is", part1(program))
    print("Answer part 2 is", part2(program))

