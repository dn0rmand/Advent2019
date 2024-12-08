from IntCode import IntCode
from enum import Enum
import curses
import sys

def day13():

    DEBUG = False
    for arg in sys.argv:
        if arg.lower() == "debug":
            DEBUG = True
            break

    class Tile(Enum):
        EMPTY = 0 # empty tile. No game object appears in this tile.
        WALL  = 1 # wall tile. Walls are indestructible barriers.
        BLOCK = 2 # block tile. Blocks can be broken by the ball.
        PADDLE= 3 # horizontal paddle tile. The paddle is indestructible.
        BALL  = 4 #  ball tile. The ball moves diagonally and bounces off objects.
        SCORE = 5

    TILES = [' ', ' ', ' ', '▔', '◉' ]

    class Game:
        def __init__(self) -> None:
            self.score   = 0
            self.screen  = {}
            self.state   = 0
            self.window  = None

        def getScreenSize(self) -> (int, int):
            maxX = max((x for x, _ in self.screen.keys()))
            maxY = max((y for _, y in self.screen.keys()))

            return (maxX, maxY)

        def setTile(self, x: int, y: int, tile: Tile) -> None:
            self.screen[(self.x, self.y)] = tile
            if self.window != None:
                t = tile.value
                ch = TILES[t]
                color = curses.color_pair(t+1)
                self.window.addstr(y+3, x+5, ch, color)

        def processInput(self, code: int) -> None:
            if self.state == 0:
                self.x = code
            elif self.state == 1:
                self.y = code
            else:
                if self.x == -1 and self.y == 0:
                    self.diff = code - self.score
                    self.score = code
                else:
                    tile = Tile(code)
                    self.setTile(self.x, self.y, tile)
                    if tile == Tile.PADDLE:
                        self.paddleX = self.x
                    elif tile == Tile.BALL:
                        self.ballX = self.x

            self.state = (self.state+1) % 3

        def getJoystick(self) -> int:
            if self.window == None:
                return self.getPaddleExpectedMove()

            self.window.addstr(3, 7, f"Score: {self.score} (+{self.diff})        ", curses.color_pair(Tile.SCORE.value + 1))
            self.window.refresh()
            time.sleep(0.005)
            return self.getPaddleExpectedMove()

        def getPaddleExpectedMove(self) -> int:
            if self.ballX > self.paddleX:
                return 1
            elif self.ballX < self.paddleX:
                return -1
            else:
                return 0

        def countTiles(self, code: Tile) -> int:
            result = sum((1 for tile in self.screen.values() if tile == code))
            return result

    def part1(program: IntCode) -> int:

        game = Game()

        output = lambda code: game.processInput(code)

        def input():
            yield 0

        program.initialize(input(), output)
        program.execute()

        return game.countTiles(Tile.BLOCK)

    def part2(program: IntCode) -> int:
        game = Game()

        output = lambda code: game.processInput(code)

        def input():
            while True:
                yield game.getPaddleExpectedMove()

        program.initialize(input(), output)
        program.memory[0] = 2
        program.execute()

        return game.score

    def play(program: IntCode) -> int:
        game = Game()

        youWin = [
            "                                        ",
            "   ,--.   ,--..-'),-----.  ,--. ,--.    ",
            "    \  `.'  /( OO'  .-.  ' |  | |  |    ",
            "  .-')     / /   |  | |  | |  | | .-')  ",
            " (OO  \   /  \_) |  |\|  | |  |_|( OO ) ",
            "  |   /  /\_   \ |  | |  | |  | | `-' / ",
            "  `-./  /.__)   `'  '-'  '('  '-'(_.-'  ",
            "    `--'          `-----'   `-----'     ",
            "                                        ",
            "      (`\ .-') /`            .-') _     ",
            "       `.( OO ),'           ( OO ) )    ",
            "    ,--./  .--.  ,-.-') ,--./ ,--,'     ",
            "    |      |  |  |  |OO)|   \ |  |\     ",
            "    |  |   |  |, |  |  \|    \|  | )    ",
            "    |  |.'.|  |_)|  |(_/|  .     |/     ",
            "    |         | ,|  |_.'|  |\    |      ",
            "    |   ,'.   |(_|  |   |  | \   |      ",
            "    '--'   '--'  `--'   `--'  `--'      ",
            "                                        "
        ]

        output = lambda code: game.processInput(code)
        def input():
            while True:
                yield game.getJoystick()

        def runLoop(stdscr) -> None:
            curses.curs_set(0)
            curses.init_pair(1+Tile.WALL.value  , curses.COLOR_CYAN, curses.COLOR_CYAN)
            curses.init_pair(1+Tile.BALL.value  , curses.COLOR_RED  , curses.COLOR_WHITE)
            curses.init_pair(1+Tile.BLOCK.value , curses.COLOR_GREEN, curses.COLOR_GREEN)
            curses.init_pair(1+Tile.PADDLE.value, curses.COLOR_BLUE, curses.COLOR_WHITE)
            curses.init_pair(1+Tile.EMPTY.value , curses.COLOR_WHITE, curses.COLOR_WHITE)
            curses.init_pair(1+Tile.SCORE.value,  curses.COLOR_WHITE, curses.COLOR_CYAN)
            curses.init_pair(20, curses.COLOR_RED, curses.COLOR_WHITE)

            stdscr.timeout(0)
            game.window = stdscr

            program.initialize(input(), output)
            program.memory[0] = 2
            program.execute()
            maxX, maxY = game.getScreenSize()
            h = len(youWin)
            w = len(youWin[0])
            x = max(0, (maxX-w)//2)
            y = max(0, (maxY-h)//2)

            color = curses.color_pair(20)

            for l in youWin:
                stdscr.addstr(y+3, x+6, l, color)
                y+=1

            l = "Press Enter to quit"
            x = (w - len(l)) // 2
            color = curses.color_pair(1+Tile.PADDLE.value)
            stdscr.addstr(maxY+3, x+6, l, color)
            stdscr.refresh()

            while True:
                key = stdscr.getch()
                if key == curses.KEY_ENTER or key in [10, 13]:
                    break

        curses.wrapper(runLoop)
        return game.score

    print("")
    print("********************************")
    print("* Advent of Code 2019 - Day 13 *")
    print("********************************")
    print("")

    program = IntCode('data/day13.data')

    if DEBUG:
        play(program)

    print("Answer part 1 is", part1(program))
    print("Answer part 2 is", part2(program))
