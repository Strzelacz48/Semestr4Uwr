import chess
import chess.svg
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget

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

def update_row(boardstate, piece, column):# do zmiany stringa 
    

def FEN_Gen(piece,position,board):# do dolozenia bierki na szachownice
    column = ord(position[0]) - 97 
    line = int(position[1]) - 1
    dirty = " ".join(board.split(" ")[1:])
    boardstate = board.split("/")
    update_row(boardstate[line], piece, column)


    start = input(" Enter starting positions : ")
White_First = (input(" Who moves first?  : ") == "white")
print(White_First)
WK = start.split(" ")[0]
WR = start.split(" ")[1]
BK = start.split(" ")[2]

board = chess.Board("8/8/8/8/8/8/8/8 w - - 0 1")
print(WK)
print(WR)
print(BK)
#print(start)
GUI(board)



#while board.is_checkmate() == False:
#    print(board)
    #black move
#    move = input()
#    board.push_san(move)
    #white move
#    move = input()
#    board.push_san(move)