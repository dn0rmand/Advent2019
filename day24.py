def day24():

    class LifeGame:
        def get(self,  x: int, y: int, ox: int = 0, oy: int = 0) -> int:
            if ox == 0 and oy == 0:
                return 1 if self.data[y][x] == '#' else 0

            xx = x+ox
            yy = y+oy
            if xx < 0:
                return 0 if self.outer == None else self.outer.get(1, 2)
            elif xx >= 5:
                return 0 if self.outer == None else self.outer.get(3, 2)
            elif yy < 0:
                return 0 if self.outer == None else self.outer.get(2, 1)
            elif yy >= 5:
                return 0 if self.outer == None else self.outer.get(2, 3)
            elif self.part2 and xx == 2 and yy == 2:
                if self.inner == None:
                    return 0

                if ox == -1:
                    return sum((self.inner.get(4, y) for y in range(0,5)))
                elif ox == 1:
                    return sum((self.inner.get(0, y) for y in range(0,5)))
                elif oy == -1:
                    return sum((self.inner.get(x, 4) for x in range(0,5)))
                elif oy == 1:
                    return sum((self.inner.get(x, 0) for x in range(0,5)))
                else:
                    assert abs(ox)+abs(oy) == 1
            else:
                return 1 if self.data[yy][xx] == '#' else 0

        def rating(self) -> int:
            if self.part2:
                return 0 # we don't care!
            m = 1
            value = 0
            for y in range(0, 5):
                for x in range(0, 5):
                    if self.data[y][x] == '#':
                        value += m
                    m <<= 1
            return value

        def count(self) -> int:
            total = 0 if self.inner == None else self.inner.count()
            for y in range(0, 5):
                total += sum((1 for c in self.data[y] if c == '#'))
            return total

        def __init__(self, data: [[chr]], part2: bool = False) -> None:
            self.data  = data
            self.part2 = part2
            self.inner = None
            self.outer = None

        def initPart2(self):
            empty = [['.']*5]*5
            self.part2 = True
            self.inner = LifeGame.createEmpty()
            self.outer = LifeGame.createEmpty()

            self.outer.inner = self
            self.inner.outer = self

            return self.root()

        def createEmpty():
            empty = [['.']*5]*5
            g = LifeGame(empty, True)
            return g

        def process(self) -> None:
            data = [[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0]]
            data[2][2] = '.'

            for y in range(0, 5):
                for x  in range(0, 5):
                    if self.part2 and x == 2 and y == 2:
                        continue

                    c = self.get(x, y, -1, 0)+self.get(x, y, 1, 0)+self.get(x, y, 0, -1)+self.get(x, y, 0, 1)
                    if self.data[y][x] == '#' and c != 1:
                        data[y][x] = '.'
                    elif self.data[y][x] == '.' and c in (1, 2):
                        data[y][x] = '#'
                        if self.inner == None:
                            self.inner = LifeGame.createEmpty()
                            self.inner.outer = self
                        if self.outer == None:
                            self.outer = LifeGame.createEmpty()
                            self.outer.inner = self
                    else:
                        data[y][x] = self.data[y][x]

            if self.inner != None:
                self.inner.process()

            self.data = data

        def root(self):
            g = self
            while g.outer != None:
                g = g.outer
            return g

        def dump(self) -> None:
            for d in self.data:
                print("".join(d))
            print("")

        def load():
            data = []
            with open("data/day24.data", 'rt') as file:
                for line in file:
                    data.append([c for c in line.strip('\n')])

            return LifeGame(data)

    def part1() -> int:
        game = LifeGame.load()
        visited = set()
        value = game.rating()
        while value not in visited:
            visited.add(value)
            game.process()
            value = game.rating()

        return value

    def part2() -> int:
        game = LifeGame.load()
        game = game.initPart2()

        for _ in range(0, 200):
            game.process()
            game = game.root()

        total = game.count()
        return total

    print("")
    print("********************************")
    print("* Advent of Code 2019 - Day 24 *")
    print("********************************")
    print("")

    print("Answer part 1 is", part1())
    print("Answer part 2 is", part2())
