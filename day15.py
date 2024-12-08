from IntCode import IntCode
import curses
import time
import random
import sys

def day15():

    DEBUG = False
    for arg in sys.argv:
        if arg.lower() == "debug":
            DEBUG = True
            break

    NORTH = 1
    SOUTH = 2
    WEST  = 3
    EAST  = 4

    WALL    = 0
    MOVED   = 1
    OXYGEN  = 2
    DEADEND = 3
    ROBOT   = 4

    class Map:
        def __init__(self) -> None:
            self.map = {}
            self.minX, self.maxX, self.minY, self.maxY = 0,0,0,0
            self.oxygen = None
            self.map[(0, 0)] = MOVED

        def get(self, x: int, y: int, autoConvert: bool = True) -> int:
            p = (x, y)
            if not p in self.map:
                return None
            p = self.map[p]
            if autoConvert and p == DEADEND:
                p = WALL
            return p

        def set(self, x: int, y: int, value: int) -> None:
            self.maxX = max(x, self.maxX)
            self.minX = min(x, self.minX)
            self.maxY = max(y, self.maxY)
            self.minY = min(y, self.minY)

            self.map[(x, y)] = value
            if value == OXYGEN:
                self.oxygen = (x, y)

    class Screen:

        BLACK  = 16
        RED    = 196
        GREEN  = 40
        YELLOW = 190
        BLUE   = 24
        MAGENTA= 13
        CYAN   = 14
        WHITE  = 255

        TILES = ['  ', '  ', '  ', '  ', '  ']
        FILL  = '  '

        def __init__(self, stdscr) -> None:
            self.window = stdscr
            curses.curs_set(0)
            curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_WHITE)

            curses.init_pair(10 + WALL , Screen.BLACK, Screen.BLACK)
            curses.init_pair(10 + MOVED, Screen.WHITE, Screen.WHITE)
            curses.init_pair(10 + OXYGEN, Screen.BLUE, Screen.BLUE)
            curses.init_pair(10 + DEADEND, Screen.RED, Screen.WHITE)
            curses.init_pair(10 + ROBOT,  Screen.GREEN, Screen.GREEN)

            stdscr.bkgd(' ', curses.color_pair(5))

            maxY, maxX = stdscr.getmaxyx()
            self.centerX = maxX // 2
            self.centerY = maxY // 2

        def initPart2(self, map: Map) -> None:
            curses.init_pair(10 + OXYGEN, Screen.BLUE, Screen.BLUE)
            Screen.TILES[OXYGEN] = Screen.FILL
            self.write(map, map.oxygen[0], map.oxygen[1])

        def sleep(self) -> None:
            time.sleep(0.02)

        def waitForEnter(self) -> None:
            while True:
                key = self.window.getch()
                if key == curses.KEY_ENTER or key in [10, 13]:
                    break

        def write(self, map: Map, x: int, y: int, ch: chr = None) -> None:
            color = curses.color_pair(0)

            if ch == None:
                ch = '?'
                s = map.get(x, y, False)
                if s == WALL:
                    ch = Screen.TILES[WALL]
                    color = curses.color_pair(10+WALL)
                elif s == DEADEND:
                    ch = Screen.TILES[DEADEND]
                    color = curses.color_pair(10+DEADEND)
                elif s == OXYGEN:
                    ch = Screen.TILES[OXYGEN]
                    color = curses.color_pair(10+OXYGEN)
                elif s == MOVED:
                    ch = Screen.TILES[MOVED]
                    color = curses.color_pair(10+MOVED)

            if ch == 'R':
                ch = Screen.TILES[ROBOT]
                color = curses.color_pair(10+ROBOT)

            if (x, y) == map.oxygen:
                ch = Screen.TILES[OXYGEN]
                color = curses.color_pair(10+OXYGEN)

            self.window.addstr(y + self.centerY, x*2 + self.centerX, ch, color)
            self.window.refresh()

        def finishUp(self, map: Map) -> None:
            for y in range(map.minY, map.maxY+1):
                for x in range(map.minX, map.maxX+1):
                    if map.get(x, y, False) == None:
                        map.set(x, y, WALL)
                        self.write(map, x, y)
            self.window.refresh()

    class DummyScreen:
        def __init__(self) -> None:
            return
        def initPart2(self, map: Map) -> None:
            return
        def sleep(self) -> None:
            return
        def waitForEnter(self) -> None:
            return
        def write(self, map: Map, x: int, y: int, ch: chr = None) -> None:
            return
        def finishUp(self, map: Map) -> None:
            return

    def buildMap(program: IntCode, screen: Screen):

        map = Map()

        x, y, lastDirection = 0, 0, NORTH

        def get(direction: int) -> chr:
            xx, yy = x, y
            if direction == NORTH:
                yy -= 1
            elif direction == SOUTH:
                yy += 1
            elif direction == WEST:
                xx -= 1
            else:
                xx += 1

            return map.get(xx, yy)

        def set(direction: int, status: int) -> None:
            nonlocal x, y

            xx, yy = x, y

            if direction == NORTH:
                yy -= 1
            elif direction == SOUTH:
                yy += 1
            elif direction == WEST:
                xx -= 1
            else:
                xx += 1

            screen.write(map, x, y)
            map.set(xx, yy, status)

            if status == OXYGEN:
                x, y = xx, yy
            if status == MOVED:
                x, y = xx, yy

            screen.write(map, xx, yy)
            screen.write(map, x, y, 'R')

        def output(status: int) -> None:
            set(lastDirection, status)
            screen.sleep()

        def input():
            nonlocal lastDirection

            while True:
                n = get(NORTH)
                s = get(SOUTH)
                w = get(WEST)
                e = get(EAST)
                if n == None:
                    lastDirection = NORTH
                elif s == None:
                    lastDirection = SOUTH
                elif w == None:
                    lastDirection = WEST
                elif e == None:
                    lastDirection = EAST
                else:
                    if n+s+w+e < 2: # only one exit
                        map.set(x, y, DEADEND)

                    if n == MOVED:
                        lastDirection = NORTH
                    elif s == MOVED:
                        lastDirection = SOUTH
                    elif w == MOVED:
                        lastDirection = WEST
                    elif e == MOVED:
                        lastDirection = EAST
                    else:
                        if map.oxygen != None: # force halt of program
                            address = program.ip+1
                            program.memory[address] = 99
                            yield 0
                        else:
                            screen.waitForEnter()
                            raise Exception("I'm stuck")

                yield lastDirection

        screen.write(map, x, y)

        program.initialize(input(), output)
        program.execute()

        screen.finishUp(map)
        return map

    def part1(map: Map, screen: Screen) -> int:
        states = [(0, 0)]
        visited= {}
        steps  = 0

        def canGo(x, y):
            if (x, y) in visited:
                return False
            return map.get(x, y, False) != WALL

        while True:
            newStates = {}

            for x, y in states:
                visited[(x, y)] = 1
                if (x, y) == map.oxygen:
                    return steps

                if canGo(x, y-1):
                    newStates[(x, y-1)] = 1
                if canGo(x, y+1):
                    newStates[(x, y+1)] = 1
                if canGo(x-1, y):
                    newStates[(x-1, y)] = 1
                if canGo(x+1, y):
                    newStates[(x+1, y)] = 1

            states = newStates.keys()
            steps += 1

    def part2(map: Map, screen: Screen) -> int:

        def canGo(x, y):
            return not map.get(x, y, False) in [WALL, OXYGEN]

        minutes =  0
        states = [map.oxygen]
        hasStates = True
        while hasStates:
            newStates = {}

            for x, y in states:

                if canGo(x, y-1):
                    newStates[(x, y-1)] = 1
                if canGo(x, y+1):
                    newStates[(x, y+1)] = 1
                if canGo(x-1, y):
                    newStates[(x-1, y)] = 1
                if canGo(x+1, y):
                    newStates[(x+1, y)] = 1

            states = newStates.keys()
            hasStates = False
            for x, y in states:
                hasStates = True
                map.set(x, y, OXYGEN)
                screen.write(map, x, y)

            if hasStates:
                minutes += 1

            screen.sleep()

        return minutes

    print("")
    print("********************************")
    print("* Advent of Code 2019 - Day 15 *")
    print("********************************")
    print("")

    program = IntCode('data/day15.data')

    def executeDay15(stdscr) -> None:

        if stdscr == None:
            screen = DummyScreen()
        else:
            screen = Screen(stdscr)

        map = buildMap(program, screen)

        v1 = part1(map, screen)
        screen.waitForEnter()

        screen.initPart2(map)
        v2 = part2(map, screen)
        screen.waitForEnter()

        return v1, v2

    if DEBUG:
        p1, p2 = curses.wrapper(executeDay15)
    else:
        p1, p2 = executeDay15(None)

    print("Answer part 1 is", p1)
    print("Answer part 2 is", p2)
