from collections import Counter

def day8():

    WIDTH = 25
    HEIGHT= 6
    SIZE  = WIDTH*HEIGHT

    def loadData() -> [[int]]:
        with open("data/day8.data", 'rt') as file:
            data = [int(c) for c in file.readline()]
            layers = [data[i:i + SIZE] for i in range(0, len(data), SIZE)]

        return layers

    def part1(layers: [[int]]) -> int:
        counts = [Counter(l) for l in layers]

        def get(counter: Counter, index: int) -> int:
            return 0 if index not in counter else counter[index]

        counts = sorted(counts, key=lambda c: get(c, 0))
        result = get(counts[0], 1) * get(counts[0], 2)
        return result

    def part2(layers: [[int]]) -> None:
        def get(l: int, x: int) -> int:
            if l >= len(layers):
                return 2
            pixel = layers[l][x]
            if pixel == 2:
                pixel = get(l+1, x)
            return pixel

        image = [get(0, x) for x in range(0, SIZE)]

        print("Answer part 2 is:")
        print("")

        for y in range(0, HEIGHT):
            for x in range(0, WIDTH):
                pixel = get(0, y*WIDTH + x)
                print("#" if pixel == 1 else " ", end="")
            print("")

    print("")
    print("*******************************")
    print("* Advent of Code 2019 - Day 8 *")
    print("*******************************")
    print("")

    layers = loadData()
    print("Answer part 1 is", part1(layers))
    part2(layers)

    print("")
