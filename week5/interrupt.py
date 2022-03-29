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

def cpu_handle_interrupt():
    global interrupt

    if interrupt == True:
      print("############## INTERRUPT ###############")
      # now act on the interrupt...
      interrupt = False

class CPU():
    
    def __init__(self, ram):
        self.pc = 0
        self.ram = ram

    def execute(self):
        while True:
            if self.pc < len(self.ram):

                # Read command
                cmd = self.ram[self.pc]
                print(f"pc: {self.pc} cmd: {cmd}")

                # Evaluate command
                if cmd == "NOP":
                    self.pc += 1
                else:
                    print(f"Unknown command {cmd}")
                    self.pc +=1
            else:
                self.pc = 0
            time.sleep(.5)

            # Interrupt handler
            cpu_handle_interrupt()

ram = ["NOP", "NOP", "NOP", "NOP", "NOP", "NOP"]
cpu = CPU(ram)

cpu_thread = threading.Thread( target = cpu.execute )
interrupt_thread = threading.Thread( target = interrupt_controller_thread)
cpu_thread.start()
interrupt_thread.start()
