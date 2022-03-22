#!/usr/bin/python3

class CPU():
    
    def __init__(self, ram):
        self.pc = 0
        self.ram = ram

    def execute(self):
        cmd = self.ram[self.pc]
        print(f"pc: {self.pc} cmd: {cmd}")
        # NOOP
        if cmd[0] == "NOP":
            self.pc += 1
        # JMP
        elif cmd[0] == "JMP":
            try:
                self.pc = cmd[1]
            except (IndexError, TypeError):
                print("JMP requires one argument of type integer")
        else:
            print(f"Unknown command {cmd}")
            self.pc +=1

ram = [["NOP"], ["NOP"], ["JMP", 3], ["NOP"], ["NOP"], ["JMP", 0]]
cpu = CPU(ram)

while True:
    cpu.execute()
