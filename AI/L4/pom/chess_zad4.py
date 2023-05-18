from cmath import inf
import chess
import chess.svg
import chess.engine
from random import choice
from tqdm import tqdm

pieces = {
    'q': 9,
    'r': 5,
    'b': 3,
    'n': 3,
    'p': 1,
}       
player_total_moves = 0
stockfish_total_moves = 0 

engine = chess.engine.SimpleEngine.popen_uci("stockfish_15_win_x64_avx2/stockfish_15_x64_avx2.exe")
        
class RandomPlayer:
    def __init__(self, board):
        self.board = board
    
    def move(self):
        m = choice(list(self.board.legal_moves))
        self.board.push(m)

class StockfishPlayer:
    def __init__(self, board, time_limit):
        self.board = board
        self.time = time_limit
    
    def move(self):
        global stockfish_total_moves
        result = engine.play(self.board, chess.engine.Limit(time=self.time))
        stockfish_total_moves += 1
        self.board.push(result.move)

class Player:
    def __init__(self, board):
        self.board = board
        self.op_score = 39

    def get_moves(self):
        return list(self.board.legal_moves)
    
    def capture_piece(self, move):
        piece = self.board.piece_at(move.to_square)
        if piece is not None:
            return pieces[piece.symbol().lower()]
        return 0
                
    def check(self, move: chess.Move):
        self.board.push(move)
        res = self.board.is_check()
        self.board.pop()
        return res
    
    def checkmate(self, move: chess.Move):
        self.board.push(move)
        res = self.board.is_checkmate()
        self.board.pop()
        return res
    
    def after_move(self, move: chess.Move, piece):
        dest = move.to_square
        self.board.push(move)
        moves = list(self.board.legal_moves)
        
        for m in moves:
            if m.to_square == dest:
                self.board.pop()
                return pieces[piece.lower()]
        self.board.pop()
        return 0
    
    def count_moves(self, move: chess.Move):
        self.board.push(move)
        self.board.turn = not self.board.turn
        my_moves = self.board.legal_moves.count()
        self.board.turn = not self.board.turn
        self.board.pop()
        return my_moves
    
    # waga zbijanej bierki
    # czy szachuje
    # czy matuje
    # czy droga wymiana po ruchu bierki
    def heuristic(self, move: chess.Move, capture, check, safety, num_moves):
        mscore = 0
        piece = self.board.piece_at(move.from_square).symbol()
        if self.checkmate(move):
            return inf
        if self.check(move):
            mscore += check
        if c := self.capture_piece(move) > 0:
            mscore += c*capture
        if s := self.after_move(move, piece):
            mscore -= s*safety
        my_moves = self.count_moves(move)
        mscore += num_moves*my_moves
        
        
        return mscore
            
    def move(self):
        global player_total_moves
        moves = self.get_moves()
        best_score = -inf
        best_move = None
        
        for move in moves:
            score = self.heuristic(move, capture, check, safety, number_of_moves)
            if score > best_score:
                best_score = score
                best_move = move
        
        player_total_moves += 1
        self.board.push(best_move)
        
capture = 2
check = 5
safety = 3
number_of_moves = 4

#single_game()

time_of_move = 0.02

def multiple_games(n):
    p_score = 0
    s_score = 0
    # Player vs Random
    board = chess.Board()
    player = Player(board)
    opp = RandomPlayer(board)
    p_white, r_black, pr_draws, pr_not_finished = 0, 0, 0, 0
    print("Player vs Random")
    for game in tqdm(range(n)):
        end = False
        board.reset()
        for moves in range(100):
            player.move()
            if board.is_checkmate():
                p_white += 1
                p_score += 100 - (moves + 1)
                end = True
                break
            if board.is_stalemate():
                pr_draws += 1
                p_score -= 100
                end = True
                break
            opp.move()
            if board.is_checkmate():
                r_black += 1
                p_score -= 1000
                end = True
                break
            if board.is_stalemate():
                pr_draws += 1
                p_score -= 100
                end = True
                break

        if not end:
            p_score -= 100
            pr_not_finished += 1
          
    #Player vs Stockfish  
    board = chess.Board()
    player = StockfishPlayer(board, time_of_move)
    opp = RandomPlayer(board)
    s_white, rr_black, sr_draws, sr_not_finished = 0, 0, 0, 0
    print("Stockfish vs Random")
    for game in tqdm(range(n)):
        end = False
        board.reset()
        for moves in range(100):
            player.move()
            if board.is_checkmate():
                s_white += 1
                s_score += 100 - (moves + 1)
                end = True
                break
            if board.is_stalemate():
                sr_draws += 1
                s_score -= 100
                end = True
                break
            opp.move()
            if board.is_checkmate():
                rr_black += 1
                s_score -= 1000
                end = True
                break
            if board.is_stalemate():
                sr_draws += 1
                s_score -= 100
                end = True
                break

        if not end:
            s_score -= 100
            sr_not_finished += 1
    
    
    print(f'                 My Player  Stockfish')
    print(f'Player wins:     {p_white:<10} {s_white}')
    print(f'Random wins:     {r_black:<10} {rr_black}')
    print(f'Draws:           {pr_draws:<10} {sr_draws}')
    print(f'Not finished:    {pr_not_finished:<10} {sr_not_finished}')
    print(f'Total moves:     {player_total_moves:<10} {stockfish_total_moves}')
    print(f'Score:           {p_score:<10} {s_score}')
    print(f'Average score:   {p_score/n:<10} {s_score/n}')
    
multiple_games(50)
engine.close()

    