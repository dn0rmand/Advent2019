from day1 import day1
from day2 import day2
from day3 import day3
from day4 import day4
from day5 import day5
from day6 import day6
from day7 import day7
from day8 import day8
from day9 import day9
from day10 import day10
from day11 import day11
from day12 import day12
from day13 import day13
from day14 import day14
from day15 import day15
from day16 import day16
from day17 import day17
from day18 import day18
from day19 import day19
from day20 import day20
from day21 import day21
from day22 import day22
from day23 import day23
from day24 import day24
from day25 import day25

import sys, time

def day0():
    pass

days = [day0, day1,  day2,  day3,  day4,  day5,  day6,  day7,  day8,  day9,  day10,
              day11, day12, day13, day14, day15, day16, day17, day18, day19, day20,
              day21, day22, day23, day24, day25]

timings = True

def run(day: int) -> float:
    if day < 1 or day > 25:
        return 0

    start = time.perf_counter()
    days[day]()
    end   = time.perf_counter() - start
    if timings:
        t = int(end * 100)/100
        if t > 1:
            print(f"Day {day} executed in {t} seconds")
    return end

daysToRun = []

for arg in sys.argv:
    try:
        if arg.lower() == "time":
            timings = True

        day = int(arg)
        if day >= 1 and day <= 25 and day not in daysToRun:
            daysToRun.append(day)
    except:
        day = None

totalTime = 0

if len(daysToRun) > 0:
    for day in daysToRun:
        totalTime += run(day)
else:
    for day in range(0, 25):
        totalTime += run(day+1)

if timings:
    t = int(totalTime * 100)/100
    print(f"Total execution time is {t} seconds")
