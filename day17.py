from IntCode import IntCode

def day17():

    UP   = '^'
    DOWN = 'v'
    LEFT = '<'
    RIGHT= '>'

    def part1(program: IntCode) -> (int, [[chr], int, int]):
        def input():
            while True:
                yield 0

        map = []

        previousLine = []
        currentLine  = []
        robotX, robotY = 0, 0
        x, y, total = 0, 0, 0

        def output(ch: int) -> None:
            nonlocal previousLine, currentLine, x, y, total, robotX, robotY

            if ch == 10:
                map.append(currentLine)
                previousLine = currentLine
                currentLine  = []
                y += 1
                x  = 0
            else:
                ch = chr(ch)
                currentLine.append(ch)
                if ch == '^' or ch == '<' or ch == '>' or ch == 'v':
                    robotX, robotY = x, y
                if y > 0 and ch != '.' and x > 1 and currentLine[x-1] != '.' and currentLine[x-2] != '.':
                    if previousLine[x-1] != '.':
                        total += y * (x-1)
                x += 1

        program.initialize(input(), output)
        program.execute()
        if len(currentLine) != 0:
            map.append(currentLine)

        return total, map, robotX, robotY

    def generatePath(map: [[chr]], x: int, y: int) -> [str]:
        robot = map[y][x]
        direction = (0, -1)
        if robot == UP:
            direction = (0, -1)
        elif robot == DOWN:
            direction = (0, 1)
        elif robot == LEFT:
            direction = (-1, 0)
        else:
            direction = (1, 0)

        def canGo(direction):
            xx = x + direction[0]
            yy = y + direction[1]
            if yy < 0 or yy >= len(map):
                return False
            if xx < 0 or xx >= len(map[yy]):
                return False
            return map[yy][xx] == '#'

        def turnRight(direction):
            if direction == (0, -1):
                return (1, 0)
            if direction == (0, 1):
                return (-1, 0)
            if direction == (1, 0):
                return (0, 1)
            if direction == (-1, 0):
                return (0, -1)
            raise Exception("Invalid direction")

        def turnLeft(direction):
            if direction == (0, -1):
                return (-1, 0)
            if direction == (0, 1):
                return (1, 0)
            if direction == (1, 0):
                return (0, -1)
            if direction == (-1, 0):
                return (0, 1)
            raise Exception("Invalid direction")

        moves = []
        while True:
            moveCount = 0
            while canGo(direction):
                x += direction[0]
                y += direction[1]
                moveCount += 1
            if moveCount > 0:
                moves.append(str(moveCount))

            if canGo(turnLeft(direction)):
                direction = turnLeft(direction)
                moves.append('L')
            elif canGo(turnRight(direction)):
                direction = turnRight(direction)
                moves.append('R')
            else:
                break

        return moves

    def shrinkPath(moves: [str]) -> (str, []):

        def cleanPath(path: str) -> str:
            bad = [',', '-']
            while len(path) > 0 and path[0] in bad:
                path = path[1:]
            while len(path) > 0 and path[-1] in bad:
                path = path[:-1]
            return path

        def shrink(path: str, key: chr, result: str, patterns: [str]) -> (str, [str]):
            path = cleanPath(path)
            if len(path) == 0:
                if len(result) > 20:
                    return None
                return result, patterns

            if key > 'C':
                return None

            i = path.find(',')
            while i < 20:
                p = path[0:i]
                if p.find('-') >= 0:
                    return None
                patterns.append(p)
                good = shrink(path.replace(p, '-'), chr(ord(key)+1), result.replace(p, key), patterns)
                if good != None:
                    return good
                patterns.pop()
                i = path.find(',', i+1)

            return None

        path = ','.join(moves)
        good = shrink(path, 'A', path, [])
        if good == None:
            raise Exception("No solution")

        return good

    def part2(program: IntCode, map: [[chr]], x: int, y: int) -> int:
        moves = generatePath(map, x, y)
        path, patterns = shrinkPath(moves)

        result = None

        def input():
            for c in path:
                yield ord(c)
            yield 10
            for s in patterns:
                for c in s:
                    yield ord(c)
                yield 10

            while True:
                yield ord('n')
                yield 10

        def output(code):
            nonlocal result

            if code > 256:
                result = code
            # else:
            #     print(chr(code), end="")

        program.initialize(input(), output)
        program.memory[0] = 2
        program.execute()

        return result

    print("")
    print("********************************")
    print("* Advent of Code 2019 - Day 17 *")
    print("********************************")
    print("")

    program = IntCode('data/day17.data')

    p1, map, robotX, robotY = part1(program)
    print("Answer part 1 is", p1)
    print("Answer part 2 is", part2(program, map, robotX, robotY))

