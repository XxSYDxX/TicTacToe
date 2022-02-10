from engine import Engine

markups = True
# make this False if the code prints gibberish for you

ptype = 'X'
etype = 'O'

class markups:
    bcyan = '\033[96m\033[1m' if markups else ''
    bred = '\033[91m\033[1m' if markups else ''
    normal = '\033[0m'


def ptab(table):
    row = ''
    for i in range(9):
        if table[i] == 0: row += ' ' + str(i+1)
        if table[i] == 1: row += markups.bcyan + ' ' + ptype + markups.normal
        if table[i] == 2: row += markups.bred + ' ' + etype + markups.normal
    
        if i in (2, 5, 8): 
            print(row)
            row = ''


def get_move():
    table = [0]*9
    move = input("Your move: [1-9] ")
    if move.isnumeric() and int(move) in range(1, 10):
        move = int(move) - 1
        if table[move] == 0:
            return move
        else:
            return get_move()
    else:
        return get_move()


def game():
    table = [0]*9
    global ptype
    global etype
    first = 1
    if input("Which X (first) or O (second)? [X/O] ").strip().upper() == 'O': 
        first = 2
        etype = 'X'
        ptype = 'O'

    e = Engine()
    
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
            if emove == -1:
                continue
            table[emove] = 2
            
        else:
            ptab(table)
            if finished == 1:
                print("You won. Dammit, how did you do that?")
            elif finished == 2:
                print("Engine wins.")
            else:
                print("Tie.")
            
            # Ask user if they want to play again
            if input("Play again? [Y/n] ").strip().lower() == 'y':
                ptype = 'X'
                etype = 'O'
                game()
                return
            else:
                return


if __name__ == '__main__':
    game()
