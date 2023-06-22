import random
import copy
from math import sqrt,log
from util import Pos
from tqdm import tqdm
from time import time
#create 16x12 board
board = []
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
def game_init(diff : int):#diff = 1, 2, 3
    for i in range(0, 16):
        pom = []
        for j in range(0, 12):
            pom.append(random.choice(colors[0:diff+1]))#random color from colors[0:diff+2] + 1 for testing
            #board[j][i] = random.choice(colors[0:diff+1])#random color from colors[0:diff+2] + 1 for testing
        board.append(pom)

def print_board():
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
            print(board[j][i], end = " ")
        print()

def can_make_a_move():
    for i in range(0, 11):
        for j in range(0, 15):
            if board[j][i] != colors[5] and (board[j][i] == board[j+1][i] or board[j][i] == board[j][i+1]):
                #print("Can make a move at ", j, " ", i)
                return True
    return False
            
def points(n : int):
    return (n-2)*(n-2)

def move_blocks_up(x : int):#Works
    finished = False
    while not finished:
        finished = True
        for i in range(0, 11):
            if board[x][i] == colors[5] and board[x][i+1] != colors[5]:
                finished = False
                for j in range(i, 11):
                    board[x][j] = board[x][j+1]
                board[x][11] = colors[5]

def move_blocks_left():#DZIALA
    finished = False
    while not finished:
        finished = True
        for i in range(0, 15):
            if board[i][0] == colors[5] and board[i+1][0] != colors[5]:
                finished = False
                for k in range(0, 12):
                    board[i][k] = board[i+1][k]
                    board[i+1][k] = colors[5]
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

def delete_blocks(x : int, y : int):
    if x == -1 or y == -1:
        return -1
    if board[x][y] == colors[5]:
        return -1
    else:
        n = delete_blocks_rek(x, y, board)
        print("Deleted: ", n)
        #print_board()
        for i in visited_columns:
            move_blocks_up(i)
        #print_board()
        move_blocks_left()
        visited_columns.clear()
        return points(n)

def game_loop(draw_board : bool):
    points = 0
    can_make_a_move()
    while(can_make_a_move()):
        if draw_board:
            print_board()
        #make a move
        #delete blocks
        #move blocks
        #add new blocks
        x = -1
        y = -1
        n = delete_blocks(x, y)
        while(n == -1):
            print("Possible moves:")
            print(possible_moves(copy.deepcopy(board)))
            x,y = input("Podaj koordynaty x, y: ").split()
            if x in letters:
                x = ord(x) - 97
            else:
                x = int(x)
            y = int(y)
            n = delete_blocks(x, y)
        points += n
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
                moves.append([j, i, move_score])
    return moves
#returns random x, y from possible moves
def random_move(cur_board):
    moves = possible_moves(cur_board.deepcopy())
    if len(moves) == 0:
        return -1, -1
    else:
        return random.choice(moves)[0:2]#
    
c = sqrt(2)

class Node:
    def __init__(self, parent=None):
        self.parent = parent
        self.board = copy.deepcopy(parent.board)
        self.moves_made = []
        self.children = {}
        self.best_score = 0
        self.sum_of_scores = 0
        self.games = 0
        self.expanded = False

    def get_UCB(self, root):
        return self.best_score + c * sqrt(log(root.games) / (self.games + 1))

    def expand(self):#WIP
        assert not self.expanded
        moves = possible_moves(copy.deepcopy(self.board))#
        if any(k != [] for k in moves.values()):
            for color, moves in moves.items():
                for move in moves:
                    game_copy = copy.deepcopy(self.game)
                    game_copy.move(move[0])
                    self.children[move[0]] = Node(game_copy, self)
        else:
            self.children = None
            self.game.game_over = True
        self.expanded = True

def mcts(cur_board):
    return

#Stolen code



class Node:
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
                    self.children[move[0]] = Node(game_copy, self)
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
    

class MCTS:
    def __init__(self, game: SameGame):
        self.root = Node(game, None)
        
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
    
        
def main(game: SameGame, iterations, verbose=False):
    mcts = MCTS(game)
    print(f'\nStart board:\n{game}')
    print('\nMoves:')
    #list_of_moves = []
    while True:
        if verbose:
            moves = game.get_moves()
            print('\nAvailable moves:')
            for color in range(5):
                print(f'{color}: ', end='')
                for move in moves[color]:
                    print(f'{move[0]} ', end='')
                print()
        mcts.run(iterations)
        move = mcts.get_move()
        if game.game_over or move == None:
            print(f'\nGame over!\nEnd board:\n{game}')
            break
        game.move(move)
        mcts.make_move(move)
        #list_of_moves.append(move)
        print(move)
        if verbose:
            print(f'Score: {game.score}')
            print(f'\n{game}')

    print('\nFinal score:', game.score)
    #return list_of_moves
        
if __name__ == '__main__':
    start = time()
    game = SameGame(15)
    sgame = deepcopy(game)
    #mcts = MCTS(game)
    #mcts.run(1000)
    #print(f'\nFinal score: {mcts.root.best_score}')
    main(game, 50)
    end = time()
    t = end - start
    print(f'\nTime: {t: .2f} s')
    # for move in moves:
    #     sgame.move(move)
    # print(f'\nFinal board:\n{sgame}')
    # print(f'\nFinal score: {sgame.score}')
#===================================================================================================
#MAIN
game_init(1)
#print_board()
game_loop(True)