from IntCode import IntCode
import sys

def day25():

    DEBUG = False
    for arg in sys.argv:
        if arg.lower() == "debug":
            DEBUG = True
            break

    killers = [
        "photons",
        "infinite loop",
        "molten lava",
        "giant electromagnet",
        "escape pod"
    ]

    class Room:
        def __init__(self):
            self.name  = None
            self.south = None
            self.north = None
            self.east  = None
            self.west  = None
            self.items = set()

    class Maze:
        def __init__(self):
            self.room   = Room()
            self.table  = {}

        def updateRoomName(self, name: str) -> None:
            if self.room.name == None:
                self.room.name = name
                self.table[name] = self.room
            elif self.room.name != name and name in self.table:
                self.room = self.table[name]
            else:
                assert name == self.room.name

        def findPath(self, target) -> [str]:
            commands = []
            visited = set()

            def inner(room: Room, direction: str):
                if room == None or room in visited:
                    return False

                if room.name == target:
                    if direction != None:
                        commands.append(direction)
                    return True

                visited.add(room)
                if direction != None:
                    commands.append(direction)
                if inner(room.east, "east"):
                    return True
                if inner(room.north, "north"):
                    return True
                if inner(room.west, "west"):
                    return True
                if inner(room.south, "south"):
                    return True
                if direction != None:
                    commands.pop()
                visited.remove(room)
                return False

            if not inner(self.room, None):
                raise Exception(f"Path to {target} not possible")

            return commands

        def addInfo(self, info: str) -> None:
            if info in ("east", "west", "north", "south"):
                if info == "east" and self.room.east == None:
                    r = Room()
                    self.room.east = r
                    r.west = self.room
                elif info == "west" and self.room.west == None:
                    r = Room()
                    self.room.west = r
                    r.east = self.room
                elif info == "north" and self.room.north == None:
                    r = Room()
                    self.room.north = r
                    r.south = self.room
                elif info == "south" and self.room.south == None:
                    r = Room()
                    self.room.south = r
                    r.north = self.room
            else:
                self.room.items.add(info)

    class State:
        def __init__(self, maze):
            self.inventory = set()
            self.maze      = maze
            self.visited   = set()
            self.lighter   = True
            self.track     = []

        def rejected(self, lighter: bool):
            self.lighter = lighter
            self.visited.add(self.maze.room)
            self.maze.room = self.track.pop()

        def pick(self, item: str) -> None:
            if item in self.maze.room.items:
                self.inventory.add(item)
                self.maze.room.items.remove(item)

        def drop(self, item: str) -> None:
            if item in self.inventory:
                self.inventory.remove(item)
                self.maze.room.items.add(item)

        def __pickAllItems__(self):
            for item in [i for i in self.maze.room.items if i not in killers]:
                self.pick(item)
                yield f"take {item}"

        def __move__(self, room: Room):
            if room == self.maze.room.north:
                self.maze.room = room
                yield "north"
            elif room == self.maze.room.south:
                self.maze.room = room
                yield "south"
            elif room == self.maze.room.east:
                self.maze.room = room
                yield "east"
            elif room == self.maze.room.west:
                self.maze.room = room
                yield "west"

        def getCommands(self) -> [str]:
            self.visited.add(self.maze.room)

            cmd1 = [cmd for cmd in self.__pickAllItems__()]

            room = self.maze.room

            if room.north and room.north not in self.visited:
                self.track.append(room)
                cmd1.extend((cmd for cmd in self.__move__(room.north)))
            elif room.east and room.east not in self.visited:
                self.track.append(room)
                cmd1.extend((cmd for cmd in self.__move__(room.east)))
            elif room.south and room.south not in self.visited:
                self.track.append(room)
                cmd1.extend((cmd for cmd in self.__move__(room.south)))
            elif room.west and room.west not in self.visited:
                self.track.append(room)
                cmd1.extend((cmd for cmd in self.__move__(room.west)))
            elif len(self.track) > 0:
                cmd1.extend((cmd for cmd in self.__move__(self.track.pop())))

            return cmd1

        def bruteForce(self):
            def sendCommand(cmd: str):
                for c in cmd:
                    yield ord(c)
                yield 10

            direction = "north"
            target    = self.maze.table["Pressure-Sensitive Floor"]
            if self.maze.room.north == target:
                direction = "north"
            elif self.maze.room.east == target:
                direction = "east"
            elif self.maze.room.south == target:
                direction = "south"
            elif self.maze.room.west == target:
                direction = "west"
            else:
                raise Exception("Room doesnt' connect to Pressure-Sensitive Floor")

            items = [i for i in self.inventory]

            for item in items:
                yield from sendCommand(f"drop {item}")

            self.inventory = set()

            def inner(index: int):
                self.track = [self.maze.room]
                if DEBUG:
                    yield from sendCommand("inv")
                yield from sendCommand(direction)

                if self.lighter:
                    return

                for i in range(index, len(items)):
                    item = items[i]
                    yield from sendCommand(f"take {item}")
                    yield from inner(i+1)
                    yield from sendCommand(f"drop {item}")

            yield from inner(0)

    def part1(program: IntCode) -> str:

        maze  = Maze()
        state = State(maze)

        currentString = ""
        answer = 0

        startMark = "Oh, hello! You should be able to get in by typing"
        endMark   = "on the keypad at the main airlock."

        def outputText(code: int) -> None:
            nonlocal currentString, answer

            if code != 10:
                currentString += chr(code)
                return

            if currentString.startswith("=="):
                maze.updateRoomName(currentString[3:-3])

            elif currentString.startswith("- "):

                maze.addInfo(currentString[2:])

            elif currentString.find("you are ejected back to the checkpoint") >= 0:

                state.rejected(currentString.find("are lighter than") >= 0)

            else:
                start = currentString.find(startMark)
                end   = currentString.find(endMark)
                if start >= 0 and end >= start:
                    s = currentString[start+len(startMark):end]
                    answer = int(s)

            if DEBUG and len(currentString) > 0:
                if currentString == "Command?":
                    currentString = ""
                print(currentString)

            currentString = ""

        def inputCommands():

            def sendCommand(cmd: str):
                for c in cmd:
                    yield ord(c)
                yield 10

            def sendCommands(commands: [str]):
                for cmd in commands:
                    yield from sendCommand(cmd)

            while True:
                commands = state.getCommands()

                if len(commands) == 0:
                    assert maze.room.name == "Hull Breach"
                    commands = maze.findPath("Security Checkpoint")
                    assert maze.room.name == "Hull Breach"
                    yield from sendCommands(commands)
                    assert maze.room.name == "Security Checkpoint"
                    yield from state.bruteForce()
                    assert answer != 0
                else:
                    yield from sendCommands(commands)

        program.initialize(inputCommands(), outputText)
        program.execute()

        return answer

    print("")
    print("********************************")
    print("* Advent of Code 2019 - Day 25 *")
    print("********************************")
    print("")

    program = IntCode('data/day25.data')

    print("Answer part 1 is", part1(program))
