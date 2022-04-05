#!/usr/bin/python3

import threading
import time

interrupt_interval=2 # in Sekunden

# ACHTUNG:
# * `interrupt` ist "Shared State"!
# * ... und ist *nicht* synchronisiert!
# * -> das ist *nicht* korrekt!
#
interrupt=False

def interrupt_controller_thread():
  while True:
    global interrupt
    time.sleep(interrupt_interval)
    print("Triggering interrupt")
    interrupt=True


class CPU():
    
    def __init__(self, ram):
        self.ram = ram
        self.schedulerSwitch = True

    def cpu_handle_interrupt(self, current_pc):
        global interrupt

        if interrupt == True:
            print("############## INTERRUPT ###############")
            # Scheduler
            if self.schedulerSwitch:
                pc = 6
            else:
                pc = 9
            # Execute interrupt command
            self.excute(pc)
            interrupt = False
            self.schedulerSwitch = not self.schedulerSwitch

        # Return pc to the value before interrup
        return current_pc

    def execute(self, pc):
        while True:
            cmd = self.ram[pc]
            print(f"pc: {pc} cmd: {cmd}")
            # NOOP
            if cmd[0] == "NOP":
                pc += 1
                # Interrupt handler
                pc = self.cpu_handle_interrupt(pc)
            # JMP
            elif cmd[0] == "JMP":
                try:
                    pc = cmd[1]
                except (IndexError, TypeError):
                    print("JMP requires one argument of type integer")
                # Interrupt handler
                pc = self.cpu_handle_interrupt(pc)
            # Interrupt instructions
            elif cmd[0].startswith("INR"):
                pc += 1
            # End of interrupt
            elif cmd[0] == "IRET":
                return
            else:
                print(f"Unknown command {cmd}")
                pc +=1
            time.sleep(.5)


ram = [["NOP"], ["NOP"], ["JMP", 3], ["NOP"], ["NOP"], ["JMP", 0], ["INR1"], ["INR1"], ["IRET"], ["INR2"], ["IRET"]]
cpu = CPU(ram)

cpu_thread = threading.Thread( target = cpu.execute(0) )
interrupt_thread = threading.Thread( target = interrupt_controller_thread)
#cpu_thread.start()
interrupt_thread.start()
# cpu_thread.join()
# interrupt_thread.join()

