from typing import Iterator, Callable
from IntCode import IntCode
from collections import deque

def day23():

    def execute(master: IntCode, callback: Callable[[int, int], bool]) -> int:
        finished = False
        programs = [ master.clone() for _ in range(0, 50) ]

        current = None

        def input():
            yield current.address

            while True:
                if len(current.inputQueue) == 0:
                    yield -1
                else:
                    x, y = current.inputQueue.popleft()
                    yield x
                    yield y

        def output(code: int) -> None:
            nonlocal finished

            current.outputQueue.append(code)
            while len(current.outputQueue) >= 3:
                target  = current.outputQueue.popleft()
                x       = current.outputQueue.popleft()
                y       = current.outputQueue.popleft()
                if target == 255:
                    if callback(x, y):
                        finished = True
                else:
                    programs[target].inputQueue.append((x, y))

        programs[0] = master
        for address in range(0, 50):
            prog = programs[address]
            prog.address      = address
            prog.inputQueue   = deque()
            prog.outputQueue  = deque()
            prog.initialize(input(), output)

        while not finished:
            for p in programs:
                current = p

                op = None
                while op not in [3, 4] and not finished:
                    op = p.step()
                    if op == 4:
                        p.idle = False
                    elif op == 3:
                        p.idle = p.lastInput == -1

            if finished:
                break

            if sum((1 for p in programs if p.idle)) == 50:
                if callback(None, None):
                    break

    def part1(master: IntCode) -> int:
        answer   = None

        def nat(x, y) -> bool:
            nonlocal answer
            if y  == None:
                return False
            answer = y
            return True

        execute(master, nat)

        return answer

    def part2(program: IntCode) -> int:

        lastSent = None
        natValue = None

        def nat(x, y) -> bool:
            nonlocal natValue, lastSent
            if x == None and y == None: # idle
                if natValue == None:
                    # raise Exception("Didn't receive a value yet")
                    return False
                elif natValue[1] == lastSent:
                    return True

                program.inputQueue.append(natValue)
                lastSent = natValue[1]
            else:
                natValue = (x, y)
            return False

        execute(program, nat)

        return lastSent

    print("")
    print("********************************")
    print("* Advent of Code 2019 - Day 23 *")
    print("********************************")
    print("")

    program = IntCode('data/day23.data')

    print("Answer part 1 is", part1(program))
    print("Answer part 2 is", part2(program))