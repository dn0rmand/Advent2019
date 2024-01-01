from IntCode import IntCode

def day7():

    def run(programs: [IntCode], phases: [int]) -> int:

        current = 0
        outputs = [0, 0, 0, 0, 0]

        def input(phase: int, amplifier: int):
            yield phase
            while True:
                yield outputs[amplifier]

        def output(x):
            nonlocal outputs
            nonlocal current

            outputs[current] = x
            current = (current + 1) % 5

        programs[0].initialize(input(phases[0], 4), output)
        programs[1].initialize(input(phases[1], 0), output)
        programs[2].initialize(input(phases[2], 1), output)
        programs[3].initialize(input(phases[3], 2), output)
        programs[4].initialize(input(phases[4], 3), output)

        while programs[current].ip >= 0:
            p = programs[current]
            p.step()

        return outputs[-1]

    def execute(programs: [IntCode], offset: int) -> int:

        bestValue = 0
        bestPhases= None

        used    = [0, 0, 0, 0, 0]
        phases  = []

        def inner():
            nonlocal bestValue
            nonlocal used
            nonlocal phases
            nonlocal bestPhases

            if len(phases) == 5:
                out = run(programs, phases)
                if out > bestValue:
                    bestValue = out
                    bestPhases = [c for c in phases]
            else:
                for i in (j for j in range(0, 5) if used[j] == 0):
                    used[i] = 1
                    phases.append(i+offset)
                    inner()
                    phases.pop()
                    used[i] = 0

        inner()

        return bestValue

    def part1(programs: [IntCode]) -> int:

        bestValue = execute(programs, 0)

        return bestValue

    def part2(programs: [IntCode]) -> int:

        bestValue = execute(programs, 5)

        return bestValue

    print("")
    print("*******************************")
    print("* Advent of Code 2019 - Day 7 *")
    print("*******************************")
    print("")

    program = IntCode('data/day7.data')
    programs = [program, program.clone(), program.clone(), program.clone(), program.clone() ]

    print("Answer part 1 is", part1( programs ))
    print("Answer part 2 is", part2( programs ))

    print("")
