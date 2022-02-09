from engine import Engine

table = [0]*9
ptype = 'X'
etype = 'O'

def ptab(table):
    row = ''
    for i in range(9):
        if table[i] == 0: row += ' ' + str(i+1)
        if table[i] == 1: row += '\033[1m\033[96m ' + ptype + '\033[0m'
        if table[i] == 2: row += '\033[1m\033[91m ' + etype + '\033[0m'
        if i in (2, 5, 8): 
            print(row)
            row = ''

first = 1
if input("Which X (first) or O (second)? [X/O] ").strip().upper() == 'O': 
    first = 2
    etype = 'X'
    ptype = 'O'

e = Engine()

if first == 1:
    ptab(table)
    pmove = int(input("Your move: [1-9] "))-1
    while pmove < 0 or pmove > 8:
        pmove = int(input("Your move: [1-9] "))-1
    table[pmove] = 1
    table[e.engine_move(table)] = 2
else:
    table[e.engine_move(table)] = 2

while 1:
    finished = e.state(table)
    if not finished:
        ptab(table)
        pmove = int(input("Your move: [1-9] "))-1
        while pmove < 0 or pmove > 8 or table[pmove]:
            pmove =int(input("Your move: [1-9] "))-1
        table[pmove] = 1
        emove = e.engine_move(table)
        table[emove] = 2
        
    else:
        ptab(table)
        if finished == 1:
            print("You won. Dammit, how did you do that?")
        elif finished == 2:
            print("Engine wins.")
        else:
            print("Tie.")
        
        input("Hit ENTER.")
        break