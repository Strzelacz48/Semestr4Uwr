import copy
board = []
for i in range (3):
    pom_board = []
    for j in range (3):
        pom_board.append(i+j)
    board.append(pom_board)
print(board)


test1_board = copy.deepcopy(board)
test2_board = copy.copy(board)
test1_board[0][0] = 100
test2_board[0][0] = 3000
board[0][0] = 20000
print(board)
print(test1_board)
print(test2_board)