from IntCode import IntCode
from typing import Iterator, Callable

class IntCodeDecoder(IntCode):
    def __init__(self, program: IntCode) -> None:
        self.program = program.program
        self.memory  = program.program

        self.nextLabel = 1
        self.instructions = {}
        self.data = set()
        self.labels = {}
        self.defaults = {}
        self.variables = {}

    def step(self) -> int:
        self.ip = -1
        return 99 # halt

    def Debug(self) -> None:
        pass # does nothing

    def initialize(self, input: Iterator[int], output: Callable[[int], None]) -> None:
        pass # does nothing

    def execute(self, debug: bool) -> None:
        pass # does nothing

    def poke(self, address: int, value: int) -> None:
        # does nothing
        pass

    def peek(self, address: int) -> int:
        if address >= len(self.program):
            return 0
        return super().peek(address)

    def addLabel(self, ip) -> None:
        if not ip in self.labels:
            self.labels[ip] = f"L{ip}" if ip != 0 else "main"
            self.nextLabel += 1

    def variableName(self, value: int, gbl: bool) -> str:
        name  = chr(ord('a') + (value % 10))
        v = value // 10

        while v > 0:
            name += chr(ord('a') + (v % 10))
            v = v // 10

        if gbl and value not in self.variables:
            if value == 0:
                value = 0
            self.variables[value] = name

        return name

    def getParameter(self, mode: int, passe: int, goto: bool = False) -> (str, int):
        ip    = self.ip
        value = self.readNext()
        if mode == 0:
            if passe == 3 and ip in self.variables and ip != 0:
                return (f"[_{self.variables[ip]}]", mode)
            else:
                return ("_" + self.variableName(value, True), mode)
        elif mode == 2:
            if value == 0:
                return ("[sp]", mode)
            if value > 0:
                return (f"[sp+{ value }]", mode)
            else:
                return (f"{self.variableName(-value, False)}(sp-{-value})", mode) # local variables name
        # elif passe == 3 and ip in self.variables:
        #     self.defaults[ip] = value
        #     return ("*_" + self.variables[ip], 0)
        else:
            return (value, mode)

    def decode(self):
        ips = [0]
        self.addLabel(0) # main entry point

        while len(ips) > 0:
            for ip in ips:
                self.pass1(ip)
            ips = [i for i in self.instructions if self.instructions[i] == None]

        self.pass3()

        if len(self.defaults) > 0:
            print("defaults variables:")
            for d in self.defaults:
                print(f"{self.variables[d]} = {self.defaults[d]}")
            print("")

        print("main:")
        skip = False
        for ip in sorted(self.instructions.keys()):
            if not skip:
                if ip != 0 and ip in self.labels:
                    if self.labels[ip] == None:
                        skip = True
                        continue

                    print(f"\n{self.labels[ip]}:")

                if self.instructions[ip] != None:
                    print(f"    {self.instructions[ip]}")

            else:
                if ip in self.labels and self.labels[ip] != None:
                    skip = False
                    print(f"\n{self.labels[ip]}:")

    def pass1(self, ip: int) -> int:
        self.ip    = ip
        self.base  = 0

        while self.ip >= 0 and self.ip < len(self.program):
            ip = self.ip
            if ip in self.instructions and self.instructions[ip] != None:
                break

            opcode, mode1, mode2, mode3 = self.getNextInstruction()

            if opcode == 99:
                self.instructions[ip] = 1
                self.ip = -1

            elif opcode in (1,2,7,8):
                self.instructions[ip] = 4 # length of the instruction
                self.getParameter(mode1, 1)
                self.getParameter(mode2, 1)
                self.getParameter(mode3, 1)

            elif opcode in (5, 6):
                self.instructions[ip] = 3 # length of the instruction
                self.getParameter(mode1, 1)
                p2, mode2 = self.getParameter(mode2, 1)
                if mode2 == 1 and p2 != 0:
                    if p2 not in self.instructions:
                        self.instructions[p2] = None
                    self.addLabel(p2)

            elif opcode in (3, 4, 9):
                self.instructions[ip] = 2
                self.getParameter(mode1, 1)
            else: # invalid opcode
                self.ip = -1

    def pass3(self) -> None:
        previous    = None
        usedLabels  = {}
        instructions = {}

        ip = 0
        previous = None
        while ip < len(self.program):
            if not ip in self.instructions:
                self.data.add(ip)
                ip += 1
                previous = None
                continue

            self.ip   = ip

            opcode, mode1, mode2, mode3 = self.getNextInstruction()

            if opcode == 99:
                instructions[ip] = 'halt'

            elif opcode == 1: # add
                p1, mode1 = self.getParameter(mode1, 3)
                p2, mode2 = self.getParameter(mode2, 3)
                p3, mode3 = self.getParameter(mode3, 3)
                if mode1 == 1 and mode2 == 1:
                    instructions[ip] = f"{p3} = {p1+p2}"
                else:
                    sign = ' + '
                    if mode2 == 1 and p2 == 0:
                        sign = ''
                        p2   = ''
                    elif mode1 == 1 and p1 == 0:
                        sign = ''
                        p1   = ''
                    elif mode2 == 1 and p2 < 0:
                        sign = ' - '
                        p2 = -p2
                    elif mode1 == 1 and p1 < 0:
                        p1, p2 = p2, -p1

                    if p1 == p3 and p2 != 0:
                        sign = sign.strip()
                        instructions[ip] = f"{p3} {sign}= {p2}"
                    elif p2 == p3 and p1 != 0:
                        sign = sign.strip()
                        instructions[ip] = f"{p3} {sign}= {p1}"
                    else:
                        instructions[ip] = f"{p3} = {p1}{sign}{p2}"

            elif opcode == 2: # multiply
                p1, mode1 = self.getParameter(mode1, 3)
                p2, mode2 = self.getParameter(mode2, 3)
                p3, mode3 = self.getParameter(mode3, 3)
                if mode1 == 1 and mode2 == 1:
                    instructions[ip] = f"{p3} = {p1*p2}"
                elif (mode1 == 1 and p1 == 0) or (mode2 == 1 and p2 == 0):
                    instructions[ip] = f"{p3} = 0"
                elif mode1 == 1 and p1 == 1:
                    instructions[ip] = f"{p3} = {p2}"
                elif mode2 == 1 and p2 == 1:
                    instructions[ip] = f"{p3} = {p1}"
                else:
                    instructions[ip] = f"{p3} = {p1} * {p2}"

            elif opcode == 3: # input
                p1, mode1 = self.getParameter(mode1, 3)
                instructions[ip] = f"{p1} = read()"

            elif opcode == 4: # output
                p1, mode1 = self.getParameter(mode1, 3)
                instructions[ip] = f"send({p1})"

            elif opcode in (5, 6): # jump
                p1, mode1 = self.getParameter(mode1, 3)
                p2, mode2 = self.getParameter(mode2, 3, True)

                action = "goto"
                if previous != None and instructions[previous] == f"[sp] = { ip + self.instructions[ip] }":
                    instructions[previous] = None # cannot remove or label aren't rendered
                    previous = None
                    action = "call"

                if mode2 == 1 and p2 in self.labels:
                    usedLabels[p2] = self.labels[p2]
                    action = f"{action} {self.labels[p2]}"
                elif mode2 == 2 and p2 == "[sp]":
                    action = "return"
                    if self.ip not in self.labels:
                        usedLabels[self.ip] = None
                else:
                    action = f"{action} {p2}"

                condition = f"{p1} { '==' if opcode == 6 else '!='} 0"

                if opcode == 5: # jump if not 0
                    if mode1 == 1 and p1 != 0:
                        condition = None
                else: # jump if false
                    if mode1 == 1 and p1 == 0:
                        condition = None

                if condition != None:
                    instructions[ip] = f"{action} if {condition}"
                else:
                    instructions[ip] = action

            elif opcode == 7: # less than
                p1, mode1 = self.getParameter(mode1, 3)
                p2, mode2 = self.getParameter(mode2, 3)
                p3, mode3 = self.getParameter(mode3, 3)
                if mode1 == 1 and mode2 == 1:
                    instructions[ip] = f"{p3} = { 1 if p1 < p2 else 0}"
                else:
                    instructions[ip] = f"{p3} = ({p1} < {p2})"

            elif opcode == 8: # equals
                p1, mode1 = self.getParameter(mode1, 3)
                p2, mode2 = self.getParameter(mode2, 3)
                p3, mode3 = self.getParameter(mode3, 3)
                if mode1 == 1 and mode2 == 1:
                    instructions[ip] = f"{p3} = { 1 if p1 == p2 else 0}"
                else:
                    instructions[ip] = f"{p3} = ({p1} == {p2})"

            elif opcode == 9: # adjusts the relative base
                p1, mode1 = self.getParameter(mode1, 3)
                if mode1 == 1 and p1 <= 0:
                    instructions[ip] = f"sp = sp-{-p1}"
                else:
                    instructions[ip] = f"sp = sp+{p1}"

            previous = ip
            ip += self.instructions[ip]

        self.labels = usedLabels
        self.instructions = instructions
