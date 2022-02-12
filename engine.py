from random import choice


class Engine:
    def __init__(self, initial_config = [0]*9):
        """Initiates the engine

        Args:
            initial_config (list, optional): Initial tictactoe board configuration. Defaults to [0]*9.
            The list can only have 9 integer elements of magnitude 0/1/2 where, 0 = No move, 1 = Player's Move, 2 = Engine's Move
        """
        is_valid(initial_config)
        global table
        table = initial_config
        
        
    def engine_move(self, config):
        """Finds the best next move for a given tictactoe board configuration

        Args:
            config (list): tictactoe board configuration
            The list can only have 9 integer elements of magnitude 0/1/2 where, 0 = No move, 1 = Player's Move, 2 = Engine's Move

        Returns:
            int: index of engine's move
                 [0-8]: Valid move which exists
                 -10: When no move exists
        """
        is_valid(config)
        global table
        table = config
        return next_move()
    
    
    def state(self, config):
        """Determines the state of the game

        Args:
            config (list): tictactoe board configuration
            The list can only have 9 integer elements of magnitude 0/1/2 where, 0 = No move, 1 = Player's Move, 2 = Engine's Move

        Returns:
            int: 0 = Game running, 1 = Player Wins, 2 = Engine wins, 3 = Tie
        """
        is_valid(config)
        c = check(config)
        if not c:
            if 0 in config: return 0
            else: return 3
        elif table[c[0]] == 1: return 1
        elif table[c[0]] == 2: return 2

            
    def checked_indices(self, config):
        """Checks which line indices matched if any did

        Args:
            config (list): tictactoe board configuration
            The list can only have 9 integer elements of magnitude 0/1/2 where, 0 = No move, 1 = Player's Move, 2 = Engine's Move

        Returns:
            False: If no line exists
            [int, int, int]: matched indices
        """
        is_valid(config)
        return check(config)


# TicTacToe Board Configuration
table = [
    2,1,1,
    1,2,2,
    1,2,1,
]
# 0 = Empty square
# 1 = Move by player
# 2 = Move by engine

corners = [0, 2, 6, 8]
edge_middles=[1, 3, 5, 7]
opposite_corner = {2:6, 6:2, 0:8, 8:0}
adjacent_corners = {0:[2,6], 2:[0,8], 6:[0,8], 8:[2,6]}


def is_valid(config):
    if len(config) != 9:
        raise Exception("config has to have 9 elements")
    for e in config:
        if e != 0 and e != 1 and e != 2:
            raise Exception("config can only contain values 0, 1 or 2")


# Return the next move for the engine
def next_move():
    if 0 in table and not check(table):
        my_checks = checked_at(table, 2)
        opponent_checks = checked_at(table, 1)
        if my_checks:
            return choice(my_checks)
        if opponent_checks:
            return choice(opponent_checks)
        
        # Hardcoded strats for offence
        if table.count(0) == 9:
            return choice(corners)
        if table.count(1) == 1 and table.count(2) == 1:
            i2 = table.index(2)
            if i2 in corners:
                i1 = table.index(1)
                if i1 in edge_middles or i1 == opposite_corner[i2]:
                    return choice(adjacent_corners[i2])
                if i1 in adjacent_corners[i2]:
                    return opposite_corner[i2]
        
        # Hardcoded strats for defense
        if table.count(1) == 1 and table.count(0) == 8:
            if table.index(1) in corners:
                return 4
        if table.count(1) == 2 and table.count(2) == 1:
            t = table.index(1)
            if t in corners:
                if table[opposite_corner[t]] == 1 and table.index(2) == 4:
                    return choice(edge_middles)
        
        # Bruteforced best-move deduction
        stats = {}
        for i in range(9):
            if table[i] == 0:
                stats[i] = [0, 0, 0]
                investgating = i
                sim_table = table.copy()
                sim_table[i] = 2
                search(investgating, sim_table, stats, False)
                    
        return choice(best_moves(stats))
    
    else:
        return -10


def check(table): 
    if table[0] == table[1] == table[2] and table[2]:
        return [0, 1, 2]
    if table[3] == table[4] == table[5] and table[5]:
        return [3, 4, 5]
    if table[6] == table[7] == table[8] and table[8]:
        return [6, 7, 8]
    if table[0] == table[3] == table[6] and table[6]:
        return [0, 3, 6]
    if table[1] == table[4] == table[7] and table[7]:
        return [1, 4, 7]
    if table[2] == table[5] == table[8] and table[8]:
        return [2, 5, 8]
    if table[0] == table[4] == table[8] and table[8]:
        return [0, 4, 8]
    if table[2] == table[4] == table[6] and table[6]:
        return [2, 4, 6]
   
    return False


def checked_at(table, checker_type):
    stable = table.copy()
    checks = []
    for i in range(9):
        if stable[i]  == 0:
            stable[i] = checker_type
            if check(stable):
                checks.append(i)
            stable[i] = 0
    return checks


def search(invsgt, stable, stats, my_turn):
    type_ = 2 if my_turn else 1
    
    if 0 not in stable:
        stats[invsgt][1] += 1
        
    i_checked = checked_at(stable, type_)
    if i_checked:
        stable[i_checked[0]] = type_
        search(invsgt, stable, stats, not my_turn)
        stable[i_checked[0]] = 0
        return
    
    if my_turn:
        checks = checked_at(stable, 1)
        if len(checks) == 1:
            stable[checks[0]] = type_
            search(invsgt, stable, stats, not my_turn)
            stable[checks[0]] = 0
            return
        elif len(checks) > 1:
            stats[invsgt][2] += 1
            return
        
    if not my_turn:
        checks = checked_at(stable, 2)
        if len(checks) == 1:
            stable[checks[0]] = type_
            search(invsgt, stable, stats, not my_turn)
            stable[checks[0]] = 0
            return
        elif len(checks) > 1:
            stats[invsgt][0] += 1
            return
            
    for i in range(9):
        if not stable[i]:
            stable[i] = type_
            search(invsgt, stable, stats, not my_turn)
            stable[i] = 0
        

def best_moves(stats):
    not_losing_rates = {k: 1-d/(w+t+d) for k, (w, t, d) in stats.items()}
    # moves with the least possibility of losing
    max_not_losing_rate = max(not_losing_rates.values())
    least_loosing_moves = [k for k, v in not_losing_rates.items() if v == max_not_losing_rate]

    win_rates = {k: stats[k][0]/sum(stats[k]) for k in least_loosing_moves}
    # moves with the best probability of winning as opposed to drawing
    max_win_rate = max(win_rates.values())
    most_win_moves = [k for k, v in win_rates.items() if v == max_win_rate]

    return most_win_moves
    
    
# print(next_move())
