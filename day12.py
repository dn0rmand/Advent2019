import math
import sys

def day12():

    DEBUG = False
    for arg in sys.argv:
        if arg.lower() == "debug":
            DEBUG = True
            break

    class Velocity:
        def __init__(self, x: int, y: int, z: int) -> None:
            self.x = x
            self.y = y
            self.z = z

    class Position:
        def __init__(self, x: int, y: int, z: int) -> None:
            self.x = x
            self.y = y
            self.z = z

    class Moon:
        def __init__(self, x: int, y: int, z: int) -> None:
            self.position = Position(x, y, z)
            self.velocity = Velocity(0, 0, 0)

        def clone(self):
            m = Moon(self.position.x, self.position.y, self.position.z)
            m.velocity = Velocity(self.velocity.x, self.velocity.y, self.velocity.z)
            return m

        def potentialEnergy(self) -> int:
            return abs(self.position.x) + abs(self.position.y) + abs(self.position.z)

        def kineticEnergy(self) -> int:
            return abs(self.velocity.x) + abs(self.velocity.y) + abs(self.velocity.z)

        def totalEnergy(self) -> int:
            return self.potentialEnergy() * self.kineticEnergy()

        def dump(self) -> None:
            print(f"pos=<x={self.position.x}, y={self.position.y}, z={self.position.z}>, vel=<x={self.velocity.x}, y={self.velocity.y}, z={self.velocity.z}>")

        def move(self) -> None:
            self.position.x += self.velocity.x
            self.position.y += self.velocity.y
            self.position.z += self.velocity.z

        def applyGravity(moon1, moon2) -> None:
            if moon1.position.x < moon2.position.x:
                moon1.velocity.x += 1
                moon2.velocity.x -= 1
            elif moon1.position.x > moon2.position.x:
                moon1.velocity.x -= 1
                moon2.velocity.x += 1

            if moon1.position.y < moon2.position.y:
                moon1.velocity.y += 1
                moon2.velocity.y -= 1
            elif moon1.position.y > moon2.position.y:
                moon1.velocity.y -= 1
                moon2.velocity.y += 1

            if moon1.position.z < moon2.position.z:
                moon1.velocity.z += 1
                moon2.velocity.z -= 1
            elif moon1.position.z > moon2.position.z:
                moon1.velocity.z -= 1
                moon2.velocity.z += 1

    def loadData() -> [Moon]:
        moons = []
        with open("data/day12.data", 'rt') as file:
            for line in file:
                line = line.strip('\n')
                values = line[1:-1].split(',')
                assert len(values) == 3
                x = int(values[0].split('=')[1].strip(' '))
                y = int(values[1].split('=')[1].strip(' '))
                z = int(values[2].split('=')[1].strip(' '))
                moons.append(Moon(x, y, z))

        return moons

    def processStep(moons: [Moon]) -> None:
        count = len(moons)
        # apply gravity to all moons
        for i in range(0, count):
            for j in range(i+1, count):
                Moon.applyGravity(moons[i], moons[j])
        # move the moons
        for i in range(0, count):
            moons[i].move()

    def getXState(moons: [Moon]):
        def loop():
            for i in range(0, len(moons)):
                m = moons[i]
                yield m.position.x
                yield m.velocity.x
        return tuple(loop())

    def getYState(moons: [Moon]):
        def loop():
            for i in range(0, len(moons)):
                m = moons[i]
                yield m.position.y
                yield m.velocity.y
        return tuple(loop())

    def getZState(moons: [Moon]):
        def loop():
            for i in range(0, len(moons)):
                m = moons[i]
                yield m.position.z
                yield m.velocity.z
        return tuple(loop())

    def part1(moons: [Moon], steps: int) -> int:
        count = len(moons)
        for step in range(0, steps):
            processStep(moons)

        energy = 0
        for i in range(0, count):
            energy += moons[i].totalEnergy()
        return energy

    def part2(moons: [Moon], trace: bool = False) -> int:
        answer = None
        step   = 0
        count  = len(moons)
        xStates= {}
        yStates= {}
        zStates= {}

        xFrequency = None
        yFrequency = None
        zFrequency = None

        traceCount = 0
        while answer == None:
            if trace:
                if traceCount == 0:
                    print(f"\r{step}", end="")
                traceCount += 1
                if traceCount >= 1000:
                    traceCount = 0

            if xFrequency == None:
                key = getXState(moons)
                if xStates.get(key) == None:
                    xStates[key] = step
                else:
                    xFrequency = step - xStates.get(key)

            if yFrequency == None:
                key = getYState(moons)
                if yStates.get(key) == None:
                    yStates[key] = step
                else:
                    yFrequency = step - yStates.get(key)

            if zFrequency == None:
                key = getZState(moons)
                if zStates.get(key) == None:
                    zStates[key] = step
                else:
                    zFrequency = step - zStates.get(key)

            if xFrequency != None and yFrequency != None and zFrequency != None:
                break

            processStep(moons)
            step += 1

        v1 = math.gcd(xFrequency, yFrequency)
        a = int(yFrequency / v1) * xFrequency
        v2 = math.gcd(a, zFrequency)
        answer = int(a / v2) * zFrequency

        if trace:
            print("\r               \r", end="")
        return answer

    print("")
    print("********************************")
    print("* Advent of Code 2019 - Day 12 *")
    print("********************************")
    print("")

    testData1 = [
        Moon(-8, -10,  0),
        Moon( 5,   5, 10),
        Moon( 2,  -7,  3),
        Moon( 9,  -8, -3)
    ]
    testData2 = [
        Moon(-1,  0,  2),
        Moon( 2,-10, -7),
        Moon( 4, -8,  8),
        Moon( 3,  5, -1)
    ]
    testData3 = [
        Moon(-8,-10,  0),
        Moon( 5,  5, 10),
        Moon( 2, -7,  3),
        Moon( 9, -8, -3)
    ]

    assert part1(testData1, 100) == 1940
    assert part2(testData2) == 2772
    assert part2(testData3) == 4686774924

    puzzle = loadData()

    print("Answer part 1 is", part1(puzzle, 1000))
    print("Answer part 2 is", part2(puzzle, DEBUG))

    print("")
