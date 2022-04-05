#!/usr/bin/python3

import threading
import time

interrupt_interval=5 # in Sekunden

# ACHTUNG:
# * `interrupt` ist "Shared State"!
# * ... und ist *nicht* synchronisiert!
# * -> das ist *nicht* korrekt!
#
interrupt = False
schedulerSwitch = True

def interrupt_controller_thread():
  while True:
    global interrupt
    time.sleep(interrupt_interval)
    print("Triggering interrupt")
    interrupt=True

def cpu_handle_interrupt(ram, current_pc):
    global interrupt
    global schedulerSwitch

    if interrupt == True:
        print("############## INTERRUPT ###############")
        # Scheduler
        if schedulerSwitch:
            pc = 6
        else:
            pc = 9
        # Execute interrupt command
        cpu_execute(ram, pc)
        interrupt = False
        schedulerSwitch = not schedulerSwitch

    # Return pc to the value before interrupt
    return current_pc

def cpu_execute(ram, pc):
    while True:
        cmd = ram[pc]
        print(f"pc: {pc} cmd: {cmd}")
        # NOOP
        if cmd[0] == "NOP":
            pc += 1
            # Interrupt handler
            pc = cpu_handle_interrupt(ram, pc)
        # JMP
        elif cmd[0] == "JMP":
            try:
                pc = cmd[1]
            except (IndexError, TypeError):
                print("JMP requires one argument of type integer")
            # Interrupt handler
            pc = cpu_handle_interrupt(ram, pc)
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
#      | program 1                   | program 2                   | interrupt 1                 | interrupt 2     |

cpu_thread = threading.Thread(target = cpu_execute, args=(ram, 0))
interrupt_thread = threading.Thread(target = interrupt_controller_thread)
cpu_thread.start()
interrupt_thread.start()
cpu_thread.join()
interrupt_thread.join()
