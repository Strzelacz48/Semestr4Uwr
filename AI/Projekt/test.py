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

a = {[1, 2, 3], [4, 5, 6], [0, 0, 0]}
print(a)
if any(a[k][2] > 0 for k in a):
    print(a)
else:
    print("none")