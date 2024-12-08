import sys

def day18():

    DEBUG = False
    for arg in sys.argv:
        if arg.lower() == "debug":
            DEBUG = True
            break

    KEY_MASK = {}

    for i in range(0, 26):
        k = chr(ord('a') + i)
        KEY_MASK[k] = 2**i

    class Map:
        def __init__(self, data: [[chr]]) -> None:
            self.data = data
            self.entry = None
            self.allKeys = 0

            keys  = []
            doors = []

            for y in range(0, len(data)):
                for x in range(0, len(data[y])):
                    c = data[y][x]
                    if c == '@':
                        if self.entry != None:
                            raise Exception("Multiple entries found")
                        self.entry = (x, y)
                        data[y][x] = '.'
                    if c >= 'a' and c <= 'z':
                        self.allKeys |= KEY_MASK[c]
                        if c in keys:
                            raise Exception(f"key {c} found multiple times")
                        keys.append(c)
                    if c >= 'A' and c <= 'Z':
                        if c in doors:
                            raise Exception(f"door {c} found multiple times")
                        doors.append(c)

            self.keyCount = len(keys)

            if self.entry == None:
                raise Exception("No entries found")
            if len(keys) < len(doors):
                raise Exception("Less keys than doors")
            for k in doors:
                if not k.lower() in keys:
                    raise Exception(f"No key for door {k}")

        def get(self, x: int, y: int, keys: int) -> chr:
            if y < 0 or x < 0 or y >= len(self.data) or x >= len(self.data[y]):
                return '#'

            c = self.data[y][x]
            if c in ['.', '#']:
                return c
            if c == c.upper(): # it's a door
                if (KEY_MASK[c.lower()] & keys) != 0: # but I have the key
                    return '.'
                else:
                    return '#' # door is locked

            return c

        def dump(self) -> None:
            for row in self.data:
                print("".join(row))

        def closeDeadEnds(self, entries) -> None:
            reset = True
            while reset:
                reset = False
                for y in range(1, len(self.data)-1):
                    row = self.data[y]
                    for x in range(1, len(self.data[y])-1):
                        if (x, y) in entries:
                            continue
                        if self.data[y][x] == '.':
                            c = 1 if self.data[y-1][x] == '#' else 0
                            c+= 1 if self.data[y+1][x] == '#' else 0
                            c+= 1 if self.data[y][x-1] == '#' else 0
                            c+= 1 if self.data[y][x+1] == '#' else 0
                            if c >= 3:
                                self.data[y][x] = '#'
                                reset = True
                                break
                    if reset:
                        break

    class State:
        def addKey(keys: int, keyCount: int, key: chr) -> (int, int):
            if key >= 'a' and key <= 'z':
                m = KEY_MASK[key]
                if (keys & m) == 0:
                    keys |= m
                    keyCount += 1
            return keys, keyCount

    class State1:
        def __init__(self, x: int, y: int, keys: int = 0, keyCount: int = 0):
            self.x = x
            self.y = y
            self.keys = keys
            self.keyCount = keyCount
            self.hash = (x, y, keys).__hash__()

        def __eq__(self, other):
            if self.hash != other.hash:
                return False
            return self.x == other.x and self.y == other.y and self.keys == other.keys

        def __hash__(self):
            return self.hash

        def move(self, map: Map):
            yield from self.__move__(0, -1, map)
            yield from self.__move__(0,  1, map)
            yield from self.__move__(-1, 0, map)
            yield from self.__move__( 1,  0, map)

        def __move__(self, dx: int, dy: int, map: Map):
            x = self.x + dx
            y = self.y + dy

            c = map.get(x, y, self.keys)
            if c != '#':
                keys, keyCount = State.addKey(self.keys, self.keyCount, c)
                s = State1(x, y, keys, keyCount)
                yield s

    class State2:

        def __init__(self, robots: [(int, int)], activeRobot: int = -1, keys: int = 0, keyCount: int = 0):
            self.robots = robots
            self.keys = keys
            self.keyCount = keyCount
            self.activeRobot = activeRobot
            self.hash = (robots, keys, activeRobot).__hash__()

        def start(x: int, y: int):
            return State2(((x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)))

        def __hash__(self):
            return self.hash

        def __eq__(self, other):
            if self.hash != other.hash:
                return False

            return self.robots == other.robots and self.keys == other.keys

        def move(self, map: Map):

            def __move__(map: Map, dx: int, dy: int, robot):
                x, y = self.robots[robot]
                x += dx
                y += dy

                c = map.get(x, y, self.keys)
                if c == '#':
                    return

                active = robot
                oldCount = self.keyCount
                keys, keyCount = State.addKey(self.keys, self.keyCount, c)
                if oldCount != keyCount:
                    active = -1

                robots = list(self.robots)
                robots[robot] = (x, y)

                s = State2(tuple(robots), active, keys, keyCount)
                yield s

            if self.activeRobot == -1:
                for i in range(0, len(self.robots)):
                    yield from __move__(map, 0,-1, i)
                    yield from __move__(map, 0, 1, i)
                    yield from __move__(map,-1, 0, i)
                    yield from __move__(map, 1, 0, i)
            else:
                    yield from __move__(map, 0,-1, self.activeRobot)
                    yield from __move__(map, 0, 1, self.activeRobot)
                    yield from __move__(map,-1, 0, self.activeRobot)
                    yield from __move__(map, 1, 0, self.activeRobot)

    def loadData(prefix: str) -> Map:
        map  = [[]]
        prefix = "--- " + prefix + " ---"
        with open("data/day18.data", 'rt') as file:
            foundPrefix = False
            for line in file:
                line = line.strip('\n')
                if not foundPrefix:
                    if line == prefix:
                        foundPrefix = True
                elif line.startswith("--- "):
                    break
                else:
                    map.append([c for c in line])

            if not foundPrefix:
                raise Exception(F"map for {prefix} not found")
        return Map(map)

    def solve(map: Map, start, trace: bool = False) -> int:
        steps     = 0
        count     = 1
        visited   = set()
        states    = set([start])
        newStates = set()

        keysFound = 0

        while len(states) > 0:
            if trace:
                print(f"\r{steps} - {keysFound} - {len(states)} ", end="")

            for state in states:
                visited.add(state)
                if state.keys == map.allKeys:
                    if trace:
                        print("\r                                          \r", end="")
                    return steps

                for s in state.move(map):
                    if not s in newStates and not s in visited:
                        if s.keyCount > keysFound:
                            keysFound = s.keyCount
                        newStates.add(s)

            steps += 1
            states.clear()
            states, newStates = newStates, states

        raise Exception("No solution found")

    def part1(map: Map, trace: bool = False) -> int:
        map.closeDeadEnds([map.entry])
        return solve(map, State1(*map.entry), trace)

    def part2(map: Map, trace: bool = False) -> int:
        x, y = map.entry
        map.data[y][x]   = '#'
        map.data[y][x+1] = '#'
        map.data[y][x-1] = '#'
        map.data[y-1][x] = '#'
        map.data[y+1][x] = '#'
        start = State2.start(x, y)

        map.closeDeadEnds(start.robots)
        answer = solve(map, start, trace)
        return answer

    def runTest(name: str, expected1: int, expected2: int = None) -> None:
        if expected1 != None:
            map = loadData(name)
            assert part1(map) == expected1
        if expected2 != None:
            map = loadData(name)
            assert part2(map) == expected2

    print("")
    print("********************************")
    print("* Advent of Code 2019 - Day 18 *")
    print("********************************")
    print("")

    if DEBUG:
        runTest("TEST1", 132)
        runTest("TEST2", 136)
        runTest("TEST3", 81)
        runTest("TEST4", None, 32)

        print("All tests passed")

    map = loadData('PUZZLE')
    print("Answer part 1 is", part1(map, DEBUG))

    map = loadData('PUZZLE')
    print("Answer part 2 is", part2(map, DEBUG))
