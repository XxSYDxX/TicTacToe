from engine import Engine

markups = True
# make this False if the code prints gibberish for you

table = [0]*9
ptype = 'X'
etype = 'O'

class Markups:
    bcyan = '\033[96m\033[1m' if markups else ''
    bred = '\033[91m\033[1m' if markups else ''
    byellow = '\033[93m\033[1m' if markups else ''
    normal = '\033[0m'


def ptab(table, matched_line = []):
    row = ''
    for i in range(9):
        if table[i] == 0: row += ' ' + str(i+1)
        if table[i] == 1: row += (Markups.byellow if i in matched_line else Markups.bcyan) + ' ' + ptype + Markups.normal
        if table[i] == 2: row += (Markups.byellow if i in matched_line else Markups.bred) + ' ' + etype + Markups.normal
    
        if i in (2, 5, 8): 
            print(row)
            row = ''


def get_move():
    table = [0]*9
    move = input("Your move: [1-9/q] " + Markups.bcyan)
    print(Markups.normal, end='')
    if move.lower().strip() == 'q':
        exit()
    if move.isnumeric() and int(move) in range(1, 10):
        move = int(move) - 1
        if table[move] == 0:
            return move
        else:
            return get_move()
    else:
        return get_move()


def game():
    global table; global ptype; global etype
    table = [0]*9
    ptype = 'X'
    etype = 'O'
    e = Engine()
    
    first = 1   # Who goes first (1: Player, 2: Engine)
    if input("Which X (first) or O (second)? [X/O] " + Markups.bcyan).strip().upper() == 'O': 
        first = 2
        etype = 'X'
        ptype = 'O'
    print(Markups.normal, end='')
        
    if first == 1:
        ptab(table)
        table[get_move()] = 1
        table[e.engine_move(table)] = 2
    else:
        table[e.engine_move(table)] = 2

    while 1:
        finished = e.state(table)
        if not finished:
            ptab(table)
            table[get_move()] = 1
            emove = e.engine_move(table)
            if emove == 9:
                continue
            table[emove] = 2
        else:
            if finished == 1:
                ptab(table, e.checked_indices(table))
                print(Markups.byellow + "You won. Dammit, how did you do that?")
            elif finished == 2:
                ptab(table, e.checked_indices(table))
                print(Markups.byellow + "Engine wins.")
            else:
                ptab(table)
                print(Markups.byellow + "Tie.")
            print(Markups.normal, end='')
            # Ask user if they want to play again
            if input("Play again? [Y/n] ").strip().lower() == 'y':
                game()
            else:
                exit()


if __name__ == '__main__':
    game()
