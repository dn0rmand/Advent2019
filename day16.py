import sys

def loadData(prefix: str):
    prefix = "--- " + prefix + " ---"
    with open("data/day16.data", 'rt') as file:
        foundPrefix = False
        for line in file:
            line = line.strip('\n')
            if not foundPrefix:
                if line == prefix:
                    foundPrefix = True
            else:
                values = [int(c) for c in line]
                return values

    raise Exception(f"No data for {prefix}")

def getData(data, repeat):
    for _ in range(0, repeat):
        yield from data

buffer1 = []
buffer2 = []

sumCache = None

def initBuffers(data) -> None:
    global buffer1, buffer2, sumCache

    sumCache = None
    buffer1 = [a for a in data]
    buffer2 = [0]*len(buffer1)
    return buffer1, len(buffer1)

def buildSums(data, offset) -> [int]:
    global sumCache

    size = len(data)
    if sumCache == None:
        sumCache = [0]*(size-offset)

    total = 0
    for i in range(size-1, offset-1, -1):
        total += data[i]
        sumCache[i-offset] = total

def processPhase(data, size, offset) -> [int]:

    buildSums(data, offset)

    def getSum(start, end):
        if start >= size:
            return 0
        total = sumCache[start-offset]
        if end < size:
            total -= sumCache[end-offset]
        return total

    destin = buffer1 if data == buffer2 else buffer2

    for i in range(offset, size):
        digit = 0
        steps = (i+1)*4
        halfSteps = steps // 2

        for j in range(i, size, steps):
            digit += getSum(j, j+i+1) - getSum(j+halfSteps, j+halfSteps+i+1)

        destin[i] = abs(digit) % 10

    return destin

def execute(data, offset, repeat) -> int:

    data, size = initBuffers(getData(data, repeat))

    for phase in range(0, 100):
        data = processPhase(data, size, offset)

    answer = 0

    for digit in data[offset:offset+8]:
        answer = (answer * 10) + digit

    return answer

def part1(data: [int]) -> int:
    return execute(data, 0, 1)

def part2(data: [int]) -> int:
    offset = 0
    for digit in data[:7]:
        offset = (offset * 10) + digit

    return execute(data, offset, 10000)

def runTest(name: str, expected1: int, expected2: int = None) -> None:
    data = loadData(name)
    if expected1 != None:
        assert part1(data) == expected1
    if expected2 != None:
        assert part2(data) == expected2
    print(name, "passed")

def day16():
    print("")
    print("********************************")
    print("* Advent of Code 2019 - Day 16 *")
    print("********************************")
    print("")

    DEBUG = False
    for arg in sys.argv:
        if arg.lower() == "debug":
            DEBUG = True
            break

    if DEBUG:
        runTest("TEST1", 24176176)
        runTest("TEST2", 73745418)
        runTest("TEST3", 52432133)
        runTest("TEST4", None, 84462026)

    puzzle = loadData("PUZZLE")

    print("Answer part 1 is", part1(puzzle))
    print("Answer part 2 is", part2(puzzle))

    print("")
