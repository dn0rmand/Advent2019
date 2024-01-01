def day14():

    class Formula:
        def __init__(self, name: str, count: int) -> None:
            self.name = name
            self.count= count
            self.components = {}

        def addComponent(self, name: str, count: int) -> None:
            assert not name in self.components
            self.components[name] = count

    class NanoFactory:
        def __init__(self, formulas, getORE) -> None:
            self.formulas = formulas
            self.getORE   = getORE
            self.stocks   = {}
            for name in formulas.keys():
                self.stocks[name] = 0
            self.stocks["FUEL"] = 0
            self.stocks["ORE"]  = 0

        def generate(self, name: str, count: int) -> None:
            if name == "ORE":
                self.getORE(count)
                return

            c = self.stocks[name]
            if c >= count:
                self.stocks[name] = c - count
                return

            self.stocks[name] = 0
            count -= c
            formula = self.formulas[name]
            while count > 0:
                required = count // formula.count
                while required*formula.count < count:
                    required += 1

                for n in formula.components:
                    self.generate(n, formula.components[n] * required)
                c = formula.count * required
                if c >= count:
                    self.stocks[name] = c-count
                    count = 0
                else:
                    count -= c

    def loadData(prefix: str):
        formulas = { }

        prefix = "--- " + prefix + " ---"
        with open("data/day14.data", 'rt') as file:
            foundPrefix = False
            for line in file:
                line = line.strip('\n')
                if not foundPrefix:
                    if line == prefix:
                        foundPrefix = True
                elif line.startswith("--- "):
                    break
                else:
                    values = line.split(' => ')
                    assert len(values) == 2
                    data = values[1].split(' ')
                    formula = Formula(data[1], int(data[0]))

                    for c in values[0].split(','):
                        c = c.strip().split(' ')
                        formula.addComponent(c[1], int(c[0]))

                    assert not formula.name in formulas
                    formulas[formula.name] = formula

        return formulas

    def part1(formulas) -> int:
        oreUsed = 0

        def getORE(count: int) -> None:
            nonlocal oreUsed
            oreUsed += count

        factory = NanoFactory(formulas, getORE)
        factory.generate("FUEL", 1)
        return oreUsed

    def part2(formulas) -> int:
        TARGET = 1000000000000

        ore = TARGET
        def getORE(count: int) -> None:
            nonlocal ore
            ore -= count

        max = TARGET
        min = 1
        answer = 0
        while max > min:
            old = answer
            answer = (max+min)//2
            if answer == old:
                break
            ore = TARGET
            factory = NanoFactory(formulas, getORE)
            factory.generate("FUEL", answer)
            if ore == 0:
                return answer
            if ore < 0:
                max = answer
            else:
                min = answer

        return min

    def runTest(name: str, expected1: int, expected2: int = None) -> None:
        formulas = loadData(name)
        assert part1(formulas) == expected1
        if expected2 != None:
            assert part2(formulas) == expected2
        # print(name, "passed")

    print("")
    print("********************************")
    print("* Advent of Code 2019 - Day 14 *")
    print("********************************")
    print("")

    runTest("TEST1", 165)
    runTest("TEST2", 13312, 82892753)
    runTest("TEST3", 180697, 5586022)
    runTest("TEST4", 2210736, 460664)

    puzzle = loadData("PUZZLE")

    print("Answer part 1 is", part1(puzzle))
    print("Answer part 2 is", part2(puzzle))

    print("")
