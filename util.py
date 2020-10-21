
def transition_program(old, new):
    yellow = False
    program = []

    for idx in range(len(old)):
        if old[idx] == new[idx]:
            program.append(old[idx])
        
        elif new[idx] == 'r':
            yellow = True
            program.append('y')

        else:
            program.append(old[idx])

    if yellow:
        return "".join(program)
    return None # no change