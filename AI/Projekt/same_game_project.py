import random
import copy
from copy import deepcopy
from math import sqrt,log
from tqdm import tqdm
from time import time
from random import choice
#create 16x12 board
main_board = []
colors = ['R', 'G', 'B', 'Y', 'P', '-']#red, green, blue, yellow, purple
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q"]
'''
for i in range(0, 12):
    pom = []
    for j in range(0, 16):
        pom.append("-")
    board.append(pom)
'''
#print(board)

visited_columns = list()
# game implementation ==============================================================================
def game_init(diff : int, board):#diff = 1, 2, 3
    for i in range(0, 16):
        pom = []
        for j in range(0, 12):
            pom.append(random.choice(colors[0:diff+2]))#random color from colors[0:diff+2] + 1 for testing
            #board[j][i] = random.choice(colors[0:diff+1])#random color from colors[0:diff+2] + 1 for testing
        board.append(pom)

def print_board(cur_board):
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q"]
    print("  ", end = " ")
    for i in range(0, 16):
        print(letters[i], end = " ")
    print()
    for i in range(0, 12):
        if i < 10:
            print(i, end = "  ")
        else:
            print(i, end = " ")
        for j in range(0, 16):
            print(cur_board[j][i], end = " ")
        print()

def can_make_a_move(cur_board):
    for i in range(0, 11):
        for j in range(0, 15):
            if cur_board[j][i] != colors[5] and (cur_board[j][i] == cur_board[j+1][i] or cur_board[j][i] == cur_board[j][i+1]):
                #print("Can make a move at ", j, " ", i)
                return True
    return False
            
def points(n : int):
    return (n-2)*(n-2)

def move_blocks_up(x : int, cur_board):#Works
    finished = False
    while not finished:
        finished = True
        for i in range(0, 11):
            if cur_board[x][i] == colors[5] and cur_board[x][i+1] != colors[5]:
                finished = False
                for j in range(i, 11):
                    cur_board[x][j] = cur_board[x][j+1]
                cur_board[x][11] = colors[5]

def move_blocks_left(cur_board):#DZIAŁA
    finished = False
    while not finished:
        finished = True
        for i in range(0, 15):
            if cur_board[i][0] == colors[5] and cur_board[i+1][0] != colors[5]:
                finished = False
                for k in range(0, 12):
                    cur_board[i][k] = cur_board[i+1][k]
                    cur_board[i+1][k] = colors[5]
                    '''
            if not finished:
                for i in range(0, 12):
                    board[15][i] = colors[5]
                    '''

def delete_blocks_rek(x : int, y : int, cur_board):
    total_deleted = 0
    remember = cur_board[x][y]
    #print("x: ", x, " y: ", y, " remember: ", remember)
    if x not in visited_columns:
        visited_columns.append(x)
    cur_board[x][y] = colors[5]
    if x < 15 and remember == cur_board[x+1][y]:
        total_deleted += delete_blocks_rek(x+1, y, cur_board)
    if y < 11 and remember == cur_board[x][y+1]:
        total_deleted += delete_blocks_rek(x, y+1, cur_board)
    if x > 0 and remember == cur_board[x-1][y]:
        total_deleted += delete_blocks_rek(x-1, y, cur_board)
    if y > 0 and remember == cur_board[x][y-1]:
        total_deleted += delete_blocks_rek(x, y-1, cur_board)
    #board[x][y] = 0
    return total_deleted + 1

def delete_blocks(x : int, y : int, cur_board):
    if x == -1 or y == -1:
        return -1
    if cur_board[x][y] == colors[5]:
        return -1
    else:
        n = delete_blocks_rek(x, y, cur_board)
        #print("Deleted: ", n)
        #print_board()
        for i in visited_columns:
            move_blocks_up(i, cur_board)
        #print_board()
        move_blocks_left(cur_board)
        visited_columns.clear()
        return points(n)

def valid_move(x : int, y : int, cur_board):
    if x == -1 or y == -1:
        return False
    if cur_board[x][y] == colors[5]:
        return False
    else:
        return True

def translate(x : int, y : int):
    if x in letters:
        x = ord(x) - 97
    else:
        x = int(x)
    y = int(y)
    return x,y

def game_loop(draw_board : bool):
    points = 0
    #can_make_a_move(main_board)
    while(can_make_a_move(main_board)):
        if draw_board:
            print_board(main_board)
        x = -1
        y = -1
        while not valid_move(x, y, main_board):
            print("Possible moves:")
            print(possible_moves(copy.deepcopy(main_board)))
            x,y = input("Podaj koordynaty x, y: ").split()
            x,y = translate(x,y)
        points += delete_blocks(x, y, main_board)
        print("Points: ", points)
    print("Game over! Your score: ", points)
#===================================================================================================
#MCTS
#returns list of possible moves given current board
def possible_moves(cur_board):
    moves = []
    for i in range(0, 11):
        for j in range(0, 15):
            if cur_board[j][i] != colors[5] and (cur_board[j][i] == cur_board[j+1][i] or cur_board[j][i] == cur_board[j][i+1]):
                move_score = points(delete_blocks_rek(j, i, cur_board))
                moves.append((j, i, move_score))
    return moves

#returns true if game is over
def game_over(cur_board):
    return len(possible_moves(deepcopy(cur_board))) == 0

#returns random x, y from possible moves
def random_move(cur_board):
    moves = possible_moves(deepcopy(cur_board))
    if len(moves) == 0:
        return -1, -1
    else:
        return random.choice(moves)[0:3]#
    
c = sqrt(2)


class Node:
    def __init__(self, board, added_score, parent=None, moves_made=[]):
        self.parent = parent
        self.board = board
        self.moves_made = moves_made #needed?
        self.children = {}
        self.best_score = 0
        self.score = added_score
        self.sum_of_scores = 0
        self.games = 0
        self.game_over = False
        self.expanded = False

    def get_UCB(self, root):
        return self.best_score + c * sqrt(log(root.games) / (self.games + 1))

    def expand(self):
        assert not self.expanded # should be good
        p_moves = possible_moves(copy.deepcopy(self.board))
        if len(p_moves) > 0:# [1,2,3]
            for move in p_moves:
                board_copy = copy.deepcopy(self.board)
                delete_blocks(move[0], move[1], board_copy)
                test1 = move[2] + self.score
                test2 = deepcopy(self.moves_made)
                test2.append(move)
                test3 = Node(board_copy, test1, self, test2)#Very important
                self.children[move] = test3
        else:
            self.children = None
            self.game_over = True
        self.expanded = True

    def update(self, score):#should be good
        current = self
        while current is not None:
            if score > current.best_score:
                current.best_score = score
            current.sum_of_scores += score
            current.games += 1
            current = current.parent

    def simulate(self):
        simulated_game = deepcopy(self.board)
        sim_score = self.score
        while can_make_a_move(simulated_game):
            move = random_move(simulated_game)
            delete_blocks_rek(move[0], move[1], simulated_game)#also have to move the blocks
            for i in visited_columns:
                move_blocks_up(i, simulated_game)
            #print_board()
            move_blocks_left(simulated_game)
            visited_columns.clear()
            sim_score += move[2]
        return sim_score
    
class MCTS:# WIP
    def __init__(self, board):
        self.root = Node(board, 0, None)
        
    def select(self):
        selected = self.root
        while selected.expanded:
            if selected.children is None:
                return False
            if all(n.expanded for n in selected.children.values()):
                selected = max(selected.children.values(), key=lambda x: x.get_UCB(self.root))
            else:
                selected = choice([n for n in selected.children.values() if not n.expanded])#losowo wybrany nie rozszerzony node
        return selected
            
    def run(self, iterations):
        for _ in range(iterations):
            selected = self.select()
            if not selected:
                continue
            selected.expand()
            score = selected.simulate()
            selected.update(score)
    
    def get_move(self):
        if not self.root.children:
            return None
        return max(self.root.children, key=lambda k: self.root.children[k].games)
    
    def make_move(self, move):
        self.root = self.root.children[move]


def main(board, iterations, verbose=True):
    #game_init(1, board)
    mcts = MCTS(board)
    print(f'\nStart board:\n')
    print_board(board)
    print('\nMoves:')
    #list_of_moves = []
    score = 0
    while True:
        if verbose:
            print_board(board)
            moves = possible_moves(deepcopy(board))#game.get_moves()
            print('\nAvailable moves:')
            print(moves)
        mcts.run(iterations)
        move = mcts.get_move()
        if verbose:
            print(f'\nBest move: {move}')
        #pom = can_make_a_move(board)
        if mcts.root.game_over or move == None:
            print(f'\nGame over!\nEnd board:\n')
            print_board(board)
            break
        score += move[2]
        if valid_move(move[0], move[1], board):
            delete_blocks(move[0], move[1], board)
        mcts.make_move(move)
        #list_of_moves.append(move)
        #print(move)
        if verbose:
            print(f'Score: {score}')
            #print(f'\n{game}')

    print('\nFinal score:', score)
    #return list_of_moves
        
if __name__ == '__main__':
    start = time()
    game_init(3,main_board)
    game = deepcopy(main_board)
    #sgame = deepcopy(game)
    #mcts = MCTS(game)
    #mcts.run(1000)
    #print(f'\nFinal score: {mcts.root.best_score}')
    main(game, 500)#TODO
    end = time()
    t = end - start
    print(f'\nTime: {t: .2f} s')
    print('Czy potrafisz lepiej?')
    game_loop(True)
    # for move in moves:
    #     sgame.move(move)
    # print(f'\nFinal board:\n{sgame}')
    # print(f'\nFinal score: {sgame.score}')
#===================================================================================================

#MAIN
#game_init(1)
#print_board()
#game_loop(True)

'''
#Stolen code



class NodeA:
    def __init__(self, game: SameGame, parent=None):
        self.game = game
        self.parent = parent
        self.children = {}
        self.best_score = 0
        self.sum_of_scores = 0
        self.games = 0
        self.expanded = False
        
    def get_avg_score(self):
        if self.games == 0:
            return 0
        return self.sum_of_scores / self.games

    def get_UCB(self, root):
        return self.best_score + c * sqrt(log(root.games) / (self.games + 1))
    
    def expand(self):
        assert not self.expanded
        moves = self.game.get_moves()
        if any(k != [] for k in moves.values()):
            for color, moves in moves.items():
                for move in moves:
                    game_copy = deepcopy(self.game)
                    game_copy.move(move[0])
                    self.children[move[0]] = NodeA(game_copy, self)
        else:
            self.children = None
            self.game.game_over = True
        self.expanded = True
    
    def update(self, score):
        current = self
        while current is not None:
            if score > current.best_score:
                current.best_score = score
            current.sum_of_scores += score
            current.games += 1
            current = current.parent
        
    def simulate(self):
        simulated_game = deepcopy(self.game)
        while not simulated_game.game_over:
            simulated_game.random_move()
        return simulated_game.score
    

class MCTSA:
    def __init__(self, game: SameGame):
        self.root = NodeA(game, None)
        
    def select(self):
        selected = self.root
        while selected.expanded:
            if selected.children is None:
                return False
            if all(n.expanded for n in selected.children.values()):
                selected = max(selected.children.values(), key=lambda x: x.get_UCB(self.root))
            else:
                selected = choice([n for n in selected.children.values() if not n.expanded])
        return selected
            
    def run(self, iterations):
        for _ in range(iterations):
            selected = self.select()
            if not selected:
                continue
            selected.expand()
            score = selected.simulate()
            selected.update(score)
    
    def get_move(self):
        if not self.root.children:
            return None
        return max(self.root.children, key=lambda k: self.root.children[k].games)
    
    def make_move(self, move):
        self.root = self.root.children[move]
    
        '''