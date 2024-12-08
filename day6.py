import math

def day6():

    def loadData():
        orbits = {}
        orbited= {}

        with open('data/day6.data', 'rt') as data:

            for line in data:
                center, orbit = line.strip().split(')')
                orbits[orbit] = center
                if center in orbited:
                    orbited[center].append(orbit)
                else:
                    orbited[center] = [orbit]

        return orbits, orbited

    def part1(orbits):
        visited = {}

        def countOrbits(value):
            if value in visited:
                return visited[value]
            count = 0 if value not in orbits else 1 + countOrbits(orbits[value])
            visited[value] = count
            return count

        return sum(( countOrbits(c) for c in orbits ))

    def part2(orbits, orbited):
        answer = 0

        if 'YOU' not in orbits or 'SAN' not in orbits:
            raise Exception('Not fair')

        if orbits['YOU'] == orbits['SAN']:
            return 0

        states  = set([orbits['YOU']])
        visited = set()
        visited.add('YOU')
        visited.add('SAN')

        moves = 0
        while orbits['SAN'] not in states:
            moves += 1
            newStates = set()
            for s in states:
                visited.add(s)

                if s in orbits and orbits[s] not in visited:
                    newStates.add(orbits[s])

                if s in orbited:
                    newStates.update((t for t in orbited[s] if t not in visited))

            states = newStates

        return moves

    print("")
    print("*******************************")
    print("* Advent of Code 2019 - Day 6 *")
    print("*******************************")
    print("")

    orbits, orbited = loadData()
    print("Answer part 1 is", part1(orbits))
    print("Answer part 2 is", part2(orbits, orbited))

    print("")
