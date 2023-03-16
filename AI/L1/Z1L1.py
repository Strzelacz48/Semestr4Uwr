import chess
import chess.svg
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget

#BFS tworzymy sobie drzewo z KAŻDYM RUCHEM ale na każej szachownicy robimy 1 ruch, a potem ustawiamy dzieci tej szachownicy na końcu kolejki z innymi

KING = 6
ROOK = 4
class MainWindow(QWidget):
    def __init__(self, board):
        super().__init__()

        self.setGeometry(100, 100, 800, 800)

        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10, 10, 780, 780)

        self.chessboard = board

        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg) 

def GUI(board):
    app = QApplication([])
    window = MainWindow(board)
    window.show()
    app.exec()

#def update_row(boardstate, piece, column):# do zmiany stringa
    

def FEN_Gen(piece,position,board):# do dolozenia bierki na szachownice
    column = ord(position[0]) - 97 
    line = int(position[1]) - 1
    dirty = " ".join(board.split(" ")[1:])
    boardstate = board.split("/")
    #update_row(boardstate[line], piece, column)

def postranslate(position):
    return (ord(position[0]) - 97)  + (int(position[1]) - 1) * 8 

'''
def whereto_naive(board, position, moves, color):
    if (moves >= 100):
        return 100
    
    column = ord(position[0]) - 97 
    line = int(position[1]) - 1
    if(column < 4 and )
'''

start = input(" Enter starting positions : ")
White_First = (input(" Who moves first?  : ") == "white")
print(White_First)
WK = start.split(" ")[0]
WR = start.split(" ")[1]
BK = start.split(" ")[2]
WKint = postranslate(WK)
WRint = postranslate(WR)
BKint = postranslate(BK)
basicboardw = "8/8/8/8/8/8/8/8 w - - 0 1"
basicboardb = "8/8/8/8/8/8/8/8 b - - 0 1"
if(White_First):
    board = chess.Board(basicboardw)
else:
    board = chess.Board(basicboardb)

board._set_piece_at(WKint, KING, True)
board._set_piece_at(WRint, ROOK, True)
board._set_piece_at(BKint, KING, False)
#while(!is_mat):
      #if
#print(update_row("8", "K", 0))
print(WK)
print(WR)
print(BK)
#print(start)
GUI(board)

board._set_piece_at(BKint+3, KING, False)

'''
#GUI(board)
while (board.is_checkmate() == False):
    if(White_First):
        if(BKint < 8 or BKint > 55 or BKint % 8 == 0 or BKint % 8 == 7):
            if(WKint )
    else:

'''
 
#    print(board)
    #black move
#    move = input()
#    board.push_san(move)
    #white move
#    move = input()
#    board.push_san(move)
