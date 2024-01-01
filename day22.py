from collections import deque

def day22():

    REVERSE   = 1
    INCREMENT = 2
    CUT       = 3

    def load():
        operations  = []
        with open("data/day22.data", 'rt') as file:
            for line in file:
                line = line.split(' ')
                operation = None
                if line[0] == "cut":
                    operation = (CUT, int(line[1]))
                elif line[1] == "into":
                    operation = (REVERSE, 0)
                else:
                    assert line[1] == "with"
                    operation = (INCREMENT, int(line[3]))

                operations.append(operation)

        return operations

    def matPro(m1 : [ [] ], m2 : [ [] ], modulo: int) -> [ [] ]:
        m = [[0, 0], [0, 0]]

        for i in range(0, 2):
            for j in range(0, 2):
                v = 0
                for k in range(0, 2):
                    v = (v + (m1[i][k] * m2[k][j])) % modulo
                m[i][j] = v

        return m

    def matPow(m : [ [] ], power: int, modulo: int) -> [ [] ]:
        if power == 1:
            return m
        r = None
        while power > 1:
            if power % 2 == 0:
                m = matPro(m, m, modulo)
                power //= 2
            else:
                if r != None:
                    r = matPro(r, m, modulo)
                else:
                    r = m
                power -= 1

        if r != None:
            m = matPro(r, m, modulo)

        return m

    def shuffle(operations: [], index: int, deckSize: int = 10) -> int:
        for op, size in operations:
            if op == REVERSE:
                index = deckSize-1-index
            elif op == CUT and size != 0:
                if size < 0:
                    size = abs(size)
                    index = (index + size) % deckSize
                else:
                    if index < size:
                        index = index+deckSize-size
                    else:
                        index -= size
            elif size != 0:
                index = (index * size) % deckSize

        return index

    def reverseShuffle(operations: [], index: int, deckSize: int = 10) -> int:
        for op, size in (operations[i-1] for i in range(len(operations), 0, -1)):
            if op == REVERSE:
                # same effect
                index = deckSize-1-index
            elif op == CUT and size != 0:
                # reverse = size*-1
                size = -size
                if size < 0:
                    size = abs(size)
                    index = (index + size) % deckSize
                else:
                    if index < size:
                        index = index+deckSize-size
                    else:
                        index -= size
            elif size != 0:
                while (index % size) != 0:
                    index += deckSize
                index = index//size

        return index

    def part1(operations: []) -> int:
        answer = shuffle(operations, 2019, 10007)
        return answer

    def part2(operations: []) -> int:
        deckSize     = 119315717514047
        shuffleCount = 101741582076661

        v1 = reverseShuffle(operations, 0, deckSize)
        v2 = reverseShuffle(operations, 1, deckSize)

        increment = v2-v1
        while increment < 0:
            increment += deckSize

        m = [[increment, 0],
            [v1, 1]]

        m = matPow(m, shuffleCount, deckSize)

        increment = m[0][0]
        start     = m[1][0]
        for idx in range(0, 2020):
            start = (start+increment) % deckSize
        return start

    def test():
        m = [ [4730, 0],
            [9122, 1] ]
        r = matPow1(m, 124, 10007)
        print(f"{r[0][0]} {r[0][1]}") # 1408
        print(f"{r[1][0]} {r[1][1]}") # 435
        r = matPow(m, 124, 10007)
        print(f"{r[0][0]} {r[0][1]}") # 1408
        print(f"{r[1][0]} {r[1][1]}") # 435

    print("")
    print("********************************")
    print("* Advent of Code 2019 - Day 22 *")
    print("********************************")
    print("")

    # test()

    operations = load()

    print("Answer part 1 is", part1(operations))
    print("Answer part 2 is", part2(operations))

    # test(operations, 10007)

