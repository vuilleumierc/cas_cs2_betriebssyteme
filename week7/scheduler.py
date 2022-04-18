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
        print("Handling interrupt")
        interrupt = False
        # Go to interrupt handler
        pc = 11 + schedulerSwitch
        cpu_execute(ram, pc)
        schedulerSwitch = not schedulerSwitch

    # Return pc to the value before interrupt
    return current_pc

def cpu_execute(ram, pc):
    while True:
        cmd = ram[pc]
        print(f"pc: {pc} cmd: {cmd}")
        # No operation
        if cmd[0] == "NOP":
            pc += 1
        # Jump to some place in the memory
        elif cmd[0] == "JMP":
            try:
                pc = cmd[1]
            except (IndexError, TypeError):
                print("JMP requires one argument of type integer")
        # End of an interrupt
        elif cmd[0] == "IRET":
            print("Exiting interrupt")
            return
        # Change value of pc
        elif cmd[0] == "MOV":
            try:
                pc = cmd[1]
            except (IndexError, TypeError):
                print("JMP requires one argument of type integer")
        else:
            print(f"Unknown command {cmd}")
            pc +=1
        # Check for interrupt
        pc = cpu_handle_interrupt(ram, pc)
        time.sleep(.5)

ram = [["NOP"], ["NOP"], ["JMP", 3], ["NOP"], ["NOP"], ["JMP", 0], ["NOP"], ["NOP"], ["IRET"], ["NOP"], ["IRET"], ["MOV", 6], ["MOV", 9]]
#      | program 1                   | program 2                   | interrupt 1               | interrupt 2    | interrupt handler

cpu_thread = threading.Thread(target = cpu_execute, args=(ram, 0))
interrupt_thread = threading.Thread(target = interrupt_controller_thread)
cpu_thread.start()
interrupt_thread.start()
cpu_thread.join()
interrupt_thread.join()
