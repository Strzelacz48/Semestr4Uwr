from cmath import inf
from types import NoneType
import chess
import chess.engine
from random import randint
from util import timeit
from tqdm import tqdm

errors = 0
black_pieces = 'qrbnp'
pieces = {
    'q': 9,
    'r': 5,
    'b': 3,
    'n': 3,
    'p': 1,
}    
engine = chess.engine.SimpleEngine.popen_uci("stockfish_15_win_x64_avx2/stockfish_15_x64_avx2.exe")

def stockfish_evaluation(board, time_limit = 0.01):
    result = engine.analyse(board, chess.engine.Limit(time=time_limit))
    res = result['score']
    return res.relative.score()
        

class Player:
    def __init__(self, board, color, weigths, alpha):
        self.board = board
        if color == 'white':
            self.color = 'white'
            self.opp_color = 'black'
        else:
            self.color = 'black'
            self.opp_color = 'white'
        self.pieces_weights = weigths
        self.alpha = alpha
        self.my_pieces = 8 + 2*(weigths['n'] + weigths['b'] + weigths['r']) + weigths['q']
        self.opp_pieces = 8 + 2*(weigths['n'] + weigths['b'] + weigths['r']) + weigths['q']

    #@timeit
    def get_moves(self):
        return list(self.board.legal_moves)
                
    def checkmate(self, move: chess.Move):
        self.board.push(move)
        res = self.board.is_checkmate()
        self.board.pop()
        return res
    
    #@timeit
    def pieces_value(self, move: chess.Move):
        try:
            prev_move = self.board.pop()
        except:
            return
        
        if self.board.is_capture(prev_move):
            piece = self.board.piece_at(prev_move.to_square)
            if piece is not None:
                piece = piece.symbol().lower()
                if piece == 'p':
                    self.my_pieces -= 1
                else:
                    self.my_pieces -= self.pieces_weights[piece]
                
        self.board.push(prev_move)
        
        if self.board.is_capture(move):
            piece = self.board.piece_at(move.to_square)
            if piece is not None:
                piece = piece.symbol().lower()
                if piece == 'p':
                    self.opp_pieces -= 1
                else:
                    self.opp_pieces -= self.pieces_weights[piece]

    #@timeit
    def count_moves(self, move: chess.Move):
        self.board.push(move)
        opp_moves = self.board.legal_moves.count()
        self.board.turn = not self.board.turn
        my_moves = self.board.legal_moves.count()
        self.board.turn = not self.board.turn
        self.board.pop()
        return my_moves, opp_moves
    
    # waga moich bierek
    # waga bierek przeciwnika
    # liczba moich ruchow
    # liczba ruchow przeciwnika
    def heuristic(self, move: chess.Move):
        if self.checkmate(move):
            return inf
        my_moves, opp_moves = self.count_moves(move)    
        self.pieces_value(move)
        return self.my_pieces - self.opp_pieces + self.alpha*my_moves - self.alpha*opp_moves
            
    def move(self):
        moves = self.get_moves()
        best_score = -inf
        best_move = None
        
        for move in moves:
            score = self.heuristic(move)
            if score > best_score:
                best_score = score
                best_move = move
        
        self.board.push(best_move)

class Agent:
    def __init__(self, weigths, alpha):
        self.weights = weigths
        self.alpha = alpha 
    
    def __str__(self) -> str:
        return f'Pieces: {self.weights}, alpha: {self.alpha}'

class Game:
    def __init__(self, white: Agent, black: Agent, stockfish_time_limit = 0.01):
        self.board = chess.Board()
        self.white = Player(self.board, 'white', white.weights, white.alpha)
        self.black = Player(self.board, 'black', black.weights, black.alpha)
        self.limit = stockfish_time_limit
        
        
    def play(self, k):
        global errors
        end = False
        for i in range(k):
            self.white.move()
            if self.board.is_checkmate():
                return 'white'
            if self.board.is_stalemate():
                break
            
            self.black.move()
            if self.board.is_checkmate():
                return 'black'
            if self.board.is_stalemate():
                break
        
        result = stockfish_evaluation(self.board, self.limit)
        if type(result) is NoneType:
            errors += 1
            return 'white'
        if result >= 0:
            return 'white'
        else:
            return 'black'
            
      
             

def draw_weights(a, b):
    weights = {
        'n': randint(a, b),
        'b': randint(a, b),
        'r': randint(a, b),
        'q': randint(a, b),
    }
    return weights


def draw_alpha(a, b):
    return randint(a, b)
     
            
def generate_agents(n, bounds1, bounds2):
    agents = {}
    # slownik postaci {agent: [wins, loses]}
    for _ in range(n):
        agent = Agent(draw_weights(*bounds1), draw_alpha(*bounds2))
        agents[agent] = [0, 0]
    return agents


def play_2_games(agents, agent1, agent2, k, stockfish):
    # pierwsza gra
    game = Game(white= agent1, black= agent2, stockfish_time_limit= stockfish)
    winner = game.play(k)
    match(winner):
        case 'white':
            agents[agent1][0] += 1
            agents[agent2][1] += 1
        case 'black':
            agents[agent1][1] += 1
            agents[agent2][0] += 1
        case _:
            raise Exception('Unknown winner')
        
        #case 'draw':
            #agents[agent1][1] += 1
            #agents[agent2][1] += 1
    # druga gra
    """ game = Game(white= agent2, black= agent1, stockfish_time_limit= stockfish)
    winner = game.play(k)
    match(winner):
        case 'white':
            agents[agent2][0] += 1
            agents[agent1][1] += 1
        case 'black':
            agents[agent2][1] += 1
            agents[agent1][0] += 1
        case _:
            raise Exception('Unknown winner') """            
               
    
def everyone_vs_everyone(agents, k, stockfish):
    agents_list = list(agents.keys())
    for i in tqdm(range(len(agents))):
        for j in tqdm(range(i+1, len(agents))):
            play_2_games(agents, agents_list[i], agents_list[j], k, stockfish)
 
            
def print2file(agents, number_of_games, alpha_bound, filename):
    offset = 5
    id = len(str(len(agents))) + offset
    num = len(str(number_of_games)) + offset
    al = len(str(alpha_bound)) + offset
    with open(filename, 'w') as f:
        f.write(f"{'id':<{id}} {'wins':<{num}} {'loses':<{num}} {'alpha':<{al}} {'weights'}\n")
        for enum, agent in enumerate(agents):
            wins, loses = agents[agent]
            f.write(f'{enum+1: <{id}} {wins:<{num}} {loses:<{num}} {agent.alpha: <{al}} {str(agent.weights)}\n')

alpha_bounds = (1, 100)
weights_bounds = (1, 100)
stockfish_time_limit = 0.01
moves = 50
num_agents = 100
number_of_games = num_agents - 1


def main():
    agents = generate_agents(num_agents, weights_bounds, alpha_bounds)
    everyone_vs_everyone(agents, moves, stockfish_time_limit)
    agents = {k: v for k, v in sorted(agents.items(), key=lambda item: item[1], reverse=True)}
    print2file(agents, number_of_games, alpha_bounds[1], 'agents.txt')
    engine.close()

#timeit("START")
main()
#print(f'Errors: {errors}')
#timeit("SHOW")
""" b = chess.Board()
b.push(chess.Move.from_uci('e2e4'))
b.push(chess.Move.from_uci('d7d5'))
t = chess.Move.from_uci('e4d5')
b.push(t)
print(b)
b.pop()
print(b)
print(b.is_capture(t)) """
""" board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
res = stockfish_evaluation(board, stockfish_time_limit)
print(int(res)) """