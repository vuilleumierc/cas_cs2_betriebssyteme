def execute(cmd):
    # NOOP
    if cmd == 0:
        pass
    # # ADD
    # elif cmd == 1:
    #     pass

speicher = [0, 0, 0]
program_counter = 0
register = []

while program_counter < len(speicher):
    instruction = speicher[program_counter]
    result = execute(instruction)
    register.append(result)
    program_counter += 1

print(register)