def day4():

    MIN = 134564
    MAX = 585159

    def isValid(password, part):
        if password < MIN or password > MAX:
            return False

        previous = 0
        count    = 0

        while password > 0:
            y = password % 10
            password = int((password - y)/10)

            if y == previous:
                count += 1
                if part == 1 and count >= 2:
                    return True
            else:
                if part == 2 and count == 2:
                    return True
                count = 1
                previous = y

        if part == 2:
            return count == 2
        else:
            return count >= 2

    def calculate(current, len, part):
        if len == 6:
            if isValid(current, part):
                return 1
            else:
                return 0

        first = 1 if current == 0 else 3 if current == 1 else 4 if current == 13 else 5 if current == 134 else 6 if current == 1345 else current % 10
        last = 8 if current == 5 else 5 if current == 0 or current == 58 or current == 5851 else 1 if current == 585 else 9

        return sum( ( calculate(current * 10 + c, len+1, part) for c in range(first, last+1) )  )

    def part1():
        return calculate(0, 0, 1)

    def part2():
        return calculate(0, 0, 2)

    print("")
    print("*******************************")
    print("* Advent of Code 2019 - Day 4 *")
    print("*******************************")
    print("")

    print("Answer part 1 is", part1())
    print("Answer part 2 is", part2())

    print("")
