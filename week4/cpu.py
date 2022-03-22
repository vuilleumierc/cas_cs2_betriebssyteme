#!/usr/bin/python3

class CPU():
    
    def __init__(self):
        self.pc = 0
        self.ram = [0, 0, 4, 0, 0, 1]

    def execute(self):
        cmd = self.ram[self.pc]
        print(f"pc: {self.pc} cmd: {cmd}")
        # NOOP
        if cmd == 0:
            self.pc += 1
        # JMP
        else:
            self.pc = cmd-1

cpu = CPU()

while True:
    cpu.execute()