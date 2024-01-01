from IntCode import IntCode
from typing import NamedTuple

def day11():

    class Direction:
        x: int
        y: int

        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

        def turn(self, direction: int) -> None:
            if direction == 0:
                if self.x == 0 and self.y == -1:
                    self.x = -1
                    self.y = 0
                elif self.x == -1 and self.y == 0:
                    self.x = 0
                    self.y = 1
                elif self.x == 0 and self.y == 1:
                    self.x = 1
                    self.y = 0
                else:
                    self.x = 0
                    self.y = -1
            else:
                if self.x == 0 and self.y == -1:
                    self.x = 1
                    self.y = 0
                elif self.x == 1 and self.y == 0:
                    self.x = 0
                    self.y = 1
                elif self.x == 0 and self.y == 1:
                    self.x = -1
                    self.y = 0
                else:
                    self.x = 0
                    self.y = -1

    class Position:
        x: int
        y: int

        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

        def max(self, o) -> None:
            self.x = max(self.x, o.x)
            self.y = max(self.y, o.y)

        def min(self, o) -> None:
            self.x = min(self.x, o.x)
            self.y = min(self.y, o.y)

        def __add__(self, o : Direction):
            return Position(self.x + o.x, self.y + o.y)

        def __key(self):
            return (self.x, self.y)

        def __hash__(self):
            return hash((self.x, self.y))

        def __eq__(self, other):
            return self.__key() == other.__key()

    class Robot:
        def __init__(self) -> None:
            self.map = {}
            self.pos = Position(0, 0)
            self.direction = Direction(0, -1)
            self.state = 0
            self.minpos= Position(0, 0)
            self.maxpos= Position(0, 0)

        def processCommand(self, command: int) -> None:
            if self.state == 0:
                self.state = 1
                self.setColor(command)
            else:
                self.state = 0
                self.turn(command)

        def setColor(self, color: int) -> None:
            self.map[self.pos] = color

        def getColor(self, x: int = None, y:int = None) -> int:
            pos = self.pos

            if not (x == None and y == None):
                pos = Position(x, y)

            if self.map.get(pos) == None:
                return 0
            else:
                return self.map.get(pos)

        def turn(self, direction: int) -> None:
            self.direction.turn(direction)
            self.pos = self.pos + self.direction
            self.maxpos.max(self.pos)
            self.minpos.min(self.pos)

    def part1(program: IntCode) -> int:
        robot = Robot()

        output = lambda color: robot.processCommand(color)

        def input():
            while True:
                yield robot.getColor()

        program.initialize(input(), output)
        program.execute()

        answer = len(robot.map)
        return answer

    def part2(program: IntCode) -> None:
        robot = Robot()
        robot.setColor(1) # start on white

        output = lambda color: robot.processCommand(color)

        def input():
            while True:
                yield robot.getColor()

        program.initialize(input(), output)
        program.execute()

        for y in range(robot.minpos.y, robot.maxpos.y+1):
            for x in range(robot.minpos.x, robot.maxpos.x+1):
                print(' ' if robot.getColor(x, y) == 0 else '#', end="")
            print("")

    print("")
    print("********************************")
    print("* Advent of Code 2019 - Day 11 *")
    print("********************************")
    print("")

    program = IntCode('data/day11.data')

    print("Answer part 1 is", part1(program))
    print("Answer part 2 is")
    part2(program)

    print("")
