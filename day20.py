def day20():

    LETTERS = set([chr(ord('A')+c) for c in range(0, 26)])

    class Maze:
        def load():
            data  = []
            with open("data/day20.data", 'rt') as file:
                for line in file:
                    line = line.strip('\n')
                    data.append([c for c in line])

            Maze.closeDeadEnds(data)
            m = Maze(data)
            # Maze.dump(m.data)
            return m

        def __init__(self, data: [[chr]]) -> None:
            self.data   = data
            self.entry  = None
            self.portals = {}

            portals = {}
            # find portals
            for y in range(0, len(data)):
                for x in (z for z in range(1, len(data[y])) if self.get(z-1, y) in LETTERS and self.get(z, y) in LETTERS):
                    key = self.get(x-1, y) + self.get(x, y)
                    if self.get(x+1, y) == '.':
                        portals[(x, y)] = (key, x+1, y)
                    else:
                        portals[(x-1, y)] = (key, x-2, y)

            for y in range(1, len(data)):
                for x in (z for z in range(0, len(data[y])) if self.get(z, y-1) in LETTERS and self.get(z, y) in LETTERS):
                    key = self.get(x, y-1) + self.get(x, y)
                    if self.get(x, y+1) == '.':
                        portals[(x, y)] = (key, x, y+1)
                    else:
                        portals[(x, y-1)] = (key, x, y-2)

            # calculate portals

            for k1 in portals:
                key, x1, y1 = portals[k1]
                if key == 'AA':
                    self.entry = (x1, y1, 0)
                elif key == 'ZZ':
                    self.exit  = (x1, y1, 0)
                else:
                    x, y = k1
                    data[y][x] = '.'
                    count = 0
                    for k2 in ( k for k in portals if k1 != k and portals[k][0] == key):
                        count += 1

                        _, x2, y2 = portals[k2]
                        self.portals[k1] = (x2, y2)
                        self.portals[k2] = (x1, y1)

                    if count != 1:
                        raise Exception("Something's wrong with the maze")

            if self.entry == None:
                raise Exception("Maze has no entry")
            if self.exit == None:
                raise Exception("Maze has no exit")

            pass

        def get(self, x: int, y: int) -> chr:
            return '#' if y < 0 or x < 0 or y >= len(self.data) or x >= len(self.data[y]) else self.data[y][x]

        def move(self, x: int, y: int, depth: int = None):

            def usePortal(a:int, b:int):
                if (a, b) not in self.portals:
                    yield (a, b, depth)
                else:
                    x, y = self.portals[(a, b)]

                    if self.useDepth:
                        d = depth + (-1 if a <= 1 or b <= 1 or b >= len(self.data)-2 or a >= len(self.data[3])-2 else 1)
                        if d >= 0:
                            yield (x, y, d)
                    else:
                        yield (x, y, depth)

            if self.get(x-1, y) == '.':
                yield from usePortal(x-1, y)
            if self.get(x, y-1) == '.':
                yield from usePortal(x, y-1)
            if self.get(x+1, y) == '.':
                yield from usePortal(x+1, y)
            if self.get(x, y+1) == '.':
                yield from usePortal(x, y+1)

        def dump(data: [[chr]]) -> None:
            for row in data:
                print("".join(row))

        def closeDeadEnds(data: [[chr]]) -> None:
            reset = True
            while reset:
                reset = False
                for y in range(1, len(data)-1):
                    for x in (z for z in range(1, len(data[y])-1) if data[y][z] == '.'):
                        c = 1 if data[y-1][x] == '#' else 0
                        c+= 1 if data[y+1][x] == '#' else 0
                        c+= 1 if data[y][x-1] == '#' else 0
                        c+= 1 if data[y][x+1] == '#' else 0
                        if c >= 3:
                            data[y][x] = '#'
                            reset = True
                            # break
                    if reset:
                        break

    def solve(maze: Maze) -> int:
        states = set([maze.entry])
        visited= set()
        steps  = 0

        while maze.exit not in states:
            if len(states) == 0:
                raise Exception("Didn't find the path :(")
            steps += 1

            newStates = set()

            # add current states to the list of visited
            visited.update(states)

            for x, y, depth in states:
                newStates.update((k for k in maze.move(x, y, depth) if k not in visited))

            states = newStates

        return steps

    def part1(maze: Maze) -> int:
        maze.useDepth = False
        return solve(maze)

    def part2(maze : Maze) -> int:
        maze.useDepth = True
        return solve(maze)

    print("")
    print("********************************")
    print("* Advent of Code 2019 - Day 20 *")
    print("********************************")
    print("")

    maze = Maze.load()

    print("Answer part 1 is", part1(maze))
    print("Answer part 2 is", part2(maze))