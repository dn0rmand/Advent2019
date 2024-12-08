import math

def day10():

    def loadMap() -> []:
        map = []
        with open('data/day10.data', 'rt') as file:
            for data in file:
                line = [c for c in data.rstrip('\n')]
                map.append(line)

        return map

    def getAsteroidInSight(map: [], x: int, y: int, ox: int, oy: int) -> (int, int):
        HEIGHT = len(map)
        WIDTH  = len(map[0])

        x += ox
        y += oy
        while x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT:
            if not map[y][x] == '.':
                return (x, y)

            x += ox
            y += oy

        return None

    def getAsteroidsInSight(map: [], x: int, y: int):
        HEIGHT = len(map)
        WIDTH  = len(map[0])

        for ox in range(0, WIDTH):
            oxx = (oy for oy in range(0, HEIGHT) if ox+oy != 0 and math.gcd(ox, oy) == 1)
            for oy in oxx:
                r = getAsteroidInSight(map, x, y, ox, oy)
                if not r == None:
                    yield (r[0], r[1], ox, oy, 1)

                if ox > 0:
                    r = getAsteroidInSight(map, x, y, -ox, oy)
                    if not r == None:
                        yield (r[0], r[1], ox, oy, 2)

                if oy > 0:
                    r = getAsteroidInSight(map, x, y, ox, -oy)
                    if not r == None:
                        yield (r[0], r[1], ox, oy, 0)

                if oy > 0 and ox > 0:
                    r = getAsteroidInSight(map, x, y, -ox, -oy)
                    if not r == None:
                        yield (r[0], r[1], ox, oy, 3)

    def part1(map: []) -> int:
        HEIGHT = len(map)
        WIDTH  = len(map[0])

        best = (0, -1, -1)

        for x in range(0, HEIGHT):
            for y in range(0, WIDTH):
                if map[y][x] == '.':
                    continue
                v = len([a for a in getAsteroidsInSight(map, x, y)])
                if v > best[0]:
                    best = (v, x, y)

        return best

    def part2(map : [], centerX: int, centerY: int) -> int:
        def sortKey(asteroid):
            _,_,ox, oy, q = asteroid
            key = q * 10000
            if q == 0:
                key += (ox / oy)

            elif q == 1:
                if not ox == 0:
                    key += (oy / ox)
                else:
                    key += 9000

            elif q == 2:
                if not oy == 0:
                    key += (ox / oy)
                else:
                    key += 9000

            elif q == 3:
                key += oy/ox

            return key

        count = 0
        asnwer = 0
        while count < 200:
            asteroids = [a for a in getAsteroidsInSight(map, centerX, centerY)]
            if len(asteroids) == 0:
                raise Exception("No more asteroids but didn't reach 200 yet")

            ast = sorted(asteroids, key=sortKey)
            for a in ast:
                count += 1
                x,y,ox,oy,q = a
                # print(f"{count} = ({x}, {y}) - dx={ox}, dy={oy}, quadrant: {q+1}")
                if count == 200:
                    answer = x*100 + y
                    break
                map[y][x] = '.'

        return answer

    print("")
    print("********************************")
    print("* Advent of Code 2019 - Day 10 *")
    print("********************************")
    print("")

    map = loadMap()

    count, x, y = part1(map)

    print("Answer part 1 is", count)
    print("Answer part 2 is", part2(map, x, y))

    print("")
