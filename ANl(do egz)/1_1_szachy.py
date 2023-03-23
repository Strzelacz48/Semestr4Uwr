import queue
from typing import Set, Any


class Board:
    def __init__(self, turn, k0, t0, k1, prev, num):
        self.turn = turn
        self.t0 = t0
        self.k0 = k0
        self.k1 = k1
        self.prev = prev
        self.num = num


def string(board):
    k = (board.turn, board.t0[0], board.t0[1], board.k0[0], board.k0[1], board.k1[0], board.k1[1])
    return k


def posx(pos):
    return ord(pos[0]) - ord('a')


def posy(pos):
    return int(pos[1]) - 1


def read_board(line):
    if line[:5] == "black":
        turn = 1
    else:
        turn = 0
    kb = line[6:8]
    tow = line[9:11]
    kc = line[12:14]
    k0 = (posx(kb), posy(kb))
    t0 = (posx(tow), posy(tow))
    k1 = (posx(kc), posy(kc))
    return Board(turn, k0, t0, k1, None, 0)


def possible_moves(board):
    possibles = []
    if board.turn == 1:
        for df in range(-1, 2):
            for ds in range(-1, 2):
                if df == ds == 0:
                    continue
                k_new = (board.k1[0] + df, board.k1[1] + ds)
                b = Board(board.turn ^ 1, board.k0, board.t0, k_new, board, board.num + 1)
                if allowed(b):
                    possibles.append(b)

    else:
        for df in range(-1, 2):
            for ds in range(-1, 2):
                if df == ds == 0:
                    continue
                k_new = (board.k0[0] + df, board.k0[1] + ds)
                b = Board(board.turn ^ 1, k_new, board.t0, board.k1, board, board.num + 1)
                if allowed(b):
                    possibles.append(b)

        for f in range(8):
            if f == board.t0[0]:
                continue
            t_new = (f, board.t0[1])
            b = Board(board.turn ^ 1, board.k0, t_new, board.k1, board, board.num + 1)
            if allowed(b):
                possibles.append(b)

        for s in range(8):
            if s == board.t0[1]:
                continue
            t_new = (board.t0[0], s)
            b = Board(board.turn ^ 1, board.k0, t_new, board.k1, board, board.num + 1)
            if allowed(b):
                possibles.append(b)

    return possibles


def same_spot(fig1, fig2):
    if fig1[0] == fig2[0] and fig1[1] == fig2[1]:
        return True
    else:
        return False


def out_of_board(fig):
    if fig[0] < 0 or fig[1] < 0 or fig[0] > 7 or fig[1] > 7:
        return True
    else:
        return False


def allowed(board):
    if board.turn == 0 and out_of_board(board.k1):
        return False
    elif board.turn == 1 and (out_of_board(board.k0) or out_of_board(board.t0)):
        return False
    elif abs(board.k1[0] - board.k0[0]) <= 1 and abs(board.k1[1] - board.k0[1]) <= 1:
        return False
    elif same_spot(board.t0, board.k0) or same_spot(board.t0, board.k1):
        return False
    elif board.turn == 1 and abs(board.k1[0] - board.t0[0]) <= 1 and abs(board.k1[1] - board.t0[1]) <= 1:
        return False
    elif board.turn == 0 and szach(board):
        return False
    else:
        return True


def szach(board):
    if board.t0[0] == board.k1[0]:
        return True
    elif board.t0[1] == board.k1[1]:
        return True
    else:
        return False


def mat(board, possibles):
    # jest ruch czarnych
    # jest szach
    # wszystkie mozliwe ruchy to szach
    if board.turn == 1 and len(possibles) == 0:
        if szach(board):
            print_moves(board)
            #print("SZACH MAT")
        else:
            fout.write("INF\n")
            #print("INF")
        return True


def print_board(board, dest):
    ss = "R" + str(board.num)
    if board.turn:
        ss += ": black\n"
    else:
        ss += ": white\n"
    if szach(board):
        ss += "*szach*\n"
    tab = []
    for i in range(8):
        t = []
        for j in range(8):
            t.append(".")
        t.append("\n")
        tab.append(t)
    tab[board.k0[0]][board.k0[1]] = 'K'
    tab[board.k1[0]][board.k1[1]] = '#'
    tab[board.t0[0]][board.t0[1]] = 'T'
    if dest == "file":
        fout.write(ss)
        for t in tab:
            for s in t:
                fout.write(s)
        fout.write('\n')
    else:
        print(turn, end="")
        for t in tab:
            for s in t:
                print(s, end="")
        print()


def print_moves(koniec):
    if wypisuj:
        print_board(koniec, "file")
        b = koniec.prev
        ile = 0
        while b:
            print_board(b, "file")
            b = b.prev
            ile += 1
    fout.write(str(koniec.num))


def bfs(start):
    que = queue.Queue()
    que.put(start)
    done.add(string(start))
    while not que.empty():
        now = que.get()
        if now in done:
            continue
        possibles = possible_moves(now)
        if mat(now, possibles):
            break
        for move in possibles:
            if string(move) not in done:
                que.put(move)
                done.add(string(move))


###############################################################
###############################################################
wypisuj = 1
# 1 - wypisuje kolejne ruchy
# 0 - działa w sprawdzarce
###############################################################

fin = open("zad1_input.txt", 'r')
fout = open("zad1_output.txt", 'w')
line_in = fin.readline()
done: set[tuple] = set()
while line_in:
    pos_start = read_board(line_in)
    bfs(pos_start)
    line_in = fin.readline()
fin.close()
fout.close()
