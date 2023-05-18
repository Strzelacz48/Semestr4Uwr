from cmath import inf
import chess
import chess.svg
from random import choice
from tqdm import tqdm
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget
from util import timeit


pieces = {
    'q': 9,
    'r': 5,
    'b': 3,
    'n': 3,
    'p': 1,
}        
count_moves = 0

        
class RandomPlayer:
    def __init__(self, board):
        self.board = board
    
    def move(self):
        m = choice(list(self.board.legal_moves))
        self.board.push(m)

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
            
    #@timeit
    def move(self):
        global count_moves
        moves = self.get_moves()
        best_score = -inf
        best_move = None
        
        for move in moves:
            score = self.heuristic(move, capture, check, safety, number_of_next_moves)
            if score > best_score:
                best_score = score
                best_move = move
        
        count_moves += 1
        self.board.push(best_move)
        
capture = 2
check = 5
safety = 3
number_of_next_moves = 4

        
class MainWindow(QWidget):
    def __init__(self, board):
        super().__init__()

        self.setGeometry(100, 100, 800, 800)

        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10, 10, 780, 780)

        self.chessboard = board

        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)     
 
        
def single_game():
    board = chess.Board()
    player = Player(board)
    opp = RandomPlayer(board)
    for _ in range(100):#tqdm(range(100)):
        player.move()
        if board.is_checkmate():
            print(board.peek())
            print("White wins")
            break
        opp.move()
        if board.is_checkmate():
            print("Black wins")
            break
    app = QApplication([])
    window = MainWindow(board)
    window.show()
    app.exec()

single_game()
    
def multiple_games(n):
    board = chess.Board()
    player = Player(board)
    opp = RandomPlayer(board)
    score = 0
    white, black, draws, not_finished = 0, 0, 0, 0
    for game in tqdm(range(n)):
        end = False
        board.reset()
        for moves in range(100):
            player.move()
            if board.is_checkmate():
                #print(board.peek())
                #print("White wins")
                white += 1
                score += 100 - (moves + 1)
                end = True
                break
            if board.is_stalemate():
                draws += 1
                score -= 100
                end = True
                break
            opp.move()
            if board.is_checkmate():
                #print("Black wins")
                black += 1
                score -= 1000
                end = True
                break
            if board.is_stalemate():
                draws += 1
                score -= 100
                end = True
                break

        if not end:
            #print("Game not finished")
            not_finished += 1
            score -= 100
            
    print("White wins:", white)
    print("Black wins:", black)
    print("Draws:", draws)
    print("Not finished:", not_finished)
    print("Moves:", count_moves)
    print("Score:", score)
    print("Average score:", score/n)
    print("Extra points:", score/(n*75) * 2)
    
timeit("START")
multiple_games(50)
timeit("SHOW")

    