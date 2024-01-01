from typing import Iterator, Callable
from collections import deque
from array import array

class IntCode:
    def __init__(self, filename: str = None) -> None:
        self.program    = []
        self.ip         = 0
        self.base       = 0
        self.lastInput  = None

        if not filename == None:
            with open(filename, 'rt') as data:
                for opcode in data.readline().split(','):
                    self.program.append(int(opcode))

    def save(self, filename: str) -> None:
        def pack(f):
            for c in self.memory:
                if c >= 0 and c < 256:
                    array('B', [c]).tofile(f)
                elif c < 0 and c > -128:
                    array('b', [c]).tofile(f)
                elif c > -32768 and c <= 32768:
                    array('i', [c]).tofile(f)
                else:
                    array('l', [c]).tofile(f)

        with open(filename, "wb") as data:
            pack(data)

    def clone(self):
        copy = IntCode()
        copy.program = self.program
        return copy

    def load(self) -> None:
        self.memory = [byte for byte in self.program]
        self.ip     = 0
        self.base   = 0

    def readNext(self) -> int:
        value = self.peek(self.ip)
        self.ip += 1
        return value

    def peek(self, address: int) -> int:
        if address < 0:
            raise Exception("invalid negative address")
        if address >= len(self.memory):
            extra = address+1-len(self.memory)
            self.memory.extend([0]*extra)
        return self.memory[address]

    def poke(self, address: int, value: int) -> None:
        if address < 0:
            raise Exception("invalid negative address")
        if address >= len(self.memory):
            extra = address+1-len(self.memory)
            self.memory.extend([0]*extra)

        self.memory[address] = value

    def getNextInstruction(self) -> (int, int, int, int):
        instruction = self.readNext()
        opcode = instruction % 100
        instruction = int((instruction-opcode)/100)

        modeA  = instruction % 10
        instruction = int((instruction-modeA)/10)
        modeB  = instruction % 10
        instruction = int((instruction-modeB)/10)
        modeC  = instruction % 10

        if not (modeA == 0 or modeA == 1 or modeA == 2):
            raise Exception("Mode not supported in IntCode")
        if not (modeB == 0 or modeB == 1 or modeB == 2):
            raise Exception("Mode not supported in IntCode")
        if not (modeC == 0 or modeC == 1 or modeC == 2):
            raise Exception("Mode not supported in IntCode")

        return (opcode, modeA, modeB, modeC)

    def readParameter(self, mode: int) -> int:
        address = self.readNext()
        if mode == 0:
            address = self.peek(address)
        elif mode == 2:
            address = self.peek(self.base+address)
        return address

    def writeParameter(self, mode: int, value: int) -> None:
        if not (mode == 0 or mode ==  2):
            raise Exception("Mode 1 not supported")
        address = self.readNext()
        if mode == 2:
            address += self.base
        self.poke(address, value)

    def step(self) -> int:
        opcode, mode1, mode2, mode3 = self.getNextInstruction()

        if opcode == 99: # halt
            self.ip = -1

        elif opcode == 1: # add
            a = self.readParameter(mode1)
            b = self.readParameter(mode2)

            self.writeParameter(mode3, a + b)

        elif opcode == 2: # multiply
            a = self.readParameter(mode1)
            b = self.readParameter(mode2)
            self.writeParameter(mode3, a * b)

        elif opcode == 3: # read input
            self.lastInput = next(self.input)
            self.writeParameter(mode1, self.lastInput)

        elif opcode == 4: # write output
            value = self.readParameter(mode1)
            self.output(value)

        elif opcode == 5: # jump if not 0
            v1 = self.readParameter(mode1)
            v2 = self.readParameter(mode2)
            if not v1 == 0:
                self.ip = v2

        elif opcode == 6: # jump if 0
            v1 = self.readParameter(mode1)
            v2 = self.readParameter(mode2)
            if v1 == 0:
                self.ip = v2

        elif opcode == 7: # less than
            v1 = self.readParameter(mode1)
            v2 = self.readParameter(mode2)
            self.writeParameter(mode3, 1 if v1 < v2 else 0)

        elif opcode == 8: # equals
            v1 = self.readParameter(mode1)
            v2 = self.readParameter(mode2)
            self.writeParameter(mode3, 1 if v1 == v2 else 0)

        elif opcode == 9: # adjusts the relative base
            v1 = self.readParameter(mode1)
            self.base += v1

        return opcode

    def initialize(self, input: Iterator[int], output: Callable[[int], None]) -> None:
        self.load()
        self.output = output
        self.input  = input

    def execute(self) -> None:
        self.ip   = 0
        self.base = 0
        while self.ip >= 0:
            self.step()
