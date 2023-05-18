#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import copy
import sys
import math
import random


class Game:
    def __init__(self, ini):
        self.n = 8
        self.history = []
        self.fliplist = []
        self.cur_player = 0
        self.free = set()
        self.board = []
        if ini:
            self.board = [['.' for _ in range(self.n)] for _ in range(self.n)]
            self.board[3][4], self.board[4][3], self.board[3][3], self.board[4][4] = 0, 0, 1, 1
            for i in range(self.n):
                for j in range(self.n):
                    if (i, j) not in ((3, 4), (4, 3), (3, 3), (4, 4)):
                        self.free.add((i, j))

    def moves_gen(self):
        me, him = self.cur_player, 1 - self.cur_player
        moves = []
        for (px, py) in self.free:
            for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)):
                x, y, i = px + dx, py + dy, 0
                while 0 <= x < self.n and 0 <= y < self.n and self.board[x][y] == him:
                    x += dx
                    y += dy
                    i += 1
                if 0 <= x < self.n and 0 <= y < self.n and i > 0 and self.board[x][y] == me:
                    moves.append((px, py))
                    break
        return moves

    def make_move(self, move):
        me, him = self.cur_player, 1 - self.cur_player
        self.history.append((me, move))
        self.cur_player = 1 - self.cur_player
        if not move:
            self.fliplist.append([])
            return
        xm, ym = move
        self.board[xm][ym] = me
        self.free.remove(move)
        fl = []
        for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            x, y = xm + dx, ym + dy
            to_flip = []
            while 0 <= x < self.n and 0 <= y < self.n and self.board[x][y] == him:
                to_flip.append((x, y))
                x += dx
                y += dy
            if 0 <= x < self.n and 0 <= y < self.n and self.board[x][y] == me:
                for (a, b) in to_flip:
                    self.board[a][b] = me
                fl += to_flip
        self.fliplist.append(fl)

    def undo_move(self):
        if not self.history:
            return
        me, move = self.history[-1]
        him = 1 - me
        to_flip = self.fliplist[-1]
        self.fliplist = self.fliplist[:-1]
        self.history = self.history[:-1]
        self.cur_player = 1 - self.cur_player
        if not move:
            return
        xm, ym = move
        self.board[xm][ym] = '.'
        self.free.add(move)
        for (a, b) in to_flip:
            self.board[a][b] = him

    def print_board(self):
        print(f'player {self.cur_player} moves')
        for line in self.board:
            for x in line:
                print(x, end="")
            print()

    def endgame(self):
        if len(self.history) < 2:
            return False
        if not self.free:
            return True
        if not self.history[-1][1] and not self.history[-2][1]:
            return True
        return False

    def board_count(self, a, b):
        ac, bc = 0, 0
        for line in self.board:
            for i in line:
                if i == a:
                    ac += 1
                elif i == b:
                    bc += 1
        return ac, bc

    def copy_game(self):
        g = Game(False)
        g.board = [[self.board[i][j] for j in range(len(self.board[0]))] for i in range((len(self.board)))]
        g.history = [i for i in self.history]
        g.cur_player = self.cur_player
        g.free = copy.deepcopy(self.free)
        g.fliplist = [[(self.fliplist[a][b][c] for c in range(2)) for b in range(len(self.fliplist[a]))] for a in
                      range(len(self.fliplist))]
        return g


########################################################################################################################
# AGENT
########################################################################################################################

# alfa beta search - kolejność znajdywania

n = 8
inf = 999999
pos_worth = [[99, -8, 8, 6, 6, 8, -8, 99],
             [-8, -24, -4, -3, -3, -4, -24, -8],
             [8, -4, 7, 4, 4, 7, -4, 8],
             [6, -3, 4, 0, 0, 4, -3, 6],
             [6, -3, 4, 0, 0, 4, -3, 6],
             [8, -4, 7, 4, 4, 7, -4, 8],
             [-8, -24, -4, -3, -3, -4, -24, -8],
             [99, -8, 8, 6, 6, 8, -8, 99]]

me = 1
d_max = 3


def pick_move(s, my_sgn):
    possibles = s.moves_gen()
    global me, d_max
    me = my_sgn

    if not possibles:
        return ()

    elif len(possibles) == 1:
        return possibles[0]

    val = []
    for move in possibles:
        s.make_move(move)
        val.append((move, min_value(s, -inf, inf, 0)))
        #print(val[-1])
        s.undo_move()
    return max(val, key=lambda v: v[1])[0]


def max_value(s, alpha, beta, d):
    if s.endgame():
        a, b = s.board_count(me, 1-me)
        return inf if a >= b else -inf
    elif d >= d_max:
        return heur_val(s)
    value = -inf
    pss = s.moves_gen()
    for m in pss:
        s.make_move(m)
        minval = min_value(s, alpha, beta, d + 1)
        s.undo_move()
        if value < minval:
            value = minval
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value


def min_value(s, alpha, beta, d):
    if s.endgame():
        a, b = s.board_count(me, 1-me)
        return inf if a >= b else -inf
    elif d >= d_max:
        return heur_val(s)
    value = inf
    pss = s.moves_gen()
    for m in pss:
        s.make_move(m)
        maxval = max_value(s, alpha, beta, d + 1)
        s.undo_move()
        if maxval < value:
            value = maxval
            best_move = m
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value


def heur_val(s):
    rund = len(s.history)
    if rund < 20:
        return pos_worth_cnt(s) + stable_disc_cnt(s) + frontier_cnt(s)
    elif rund < 56:
        return stable_disc_cnt(s) + frontier_cnt(s) + stable_pos_cnt(s)
    else:
        return gain_cnt(s) + frontier_cnt(s)


def stable_pos_cnt(s):
    if s.cur_player != me:
        return 0

    val = 0
    mg = s.moves_gen()
    for m in mg:
        val += stable_pos(m, s)
    if s.cur_player == me:
        return val
    else:
        return -val


def gain_cnt(s):
    val = 0
    for x in range(n):
        for y in range(n):
            if s.board[x][y] == me:
                val += 1
            elif s.board[x][y] == 1-me:
                val -= 1
    return val


def frontier_cnt(s):
    front = 0
    mg = s.moves_gen()
    if s.cur_player == me:
        if len(mg) == 0:
            front -= 200
        front += len(mg)
    else:
        if len(mg) == 0:
            front += 200
        front -= len(mg)

    return front


def stable_disc_cnt(s):
    val = 0
    for x in range(n):
        for y in range(n):
            if s.board[x][y] == me:
                val += stable_disc((x, y), s, me)
            elif s.board[x][y] == 1-me:
                val -= stable_disc((x, y), s, 1-me)
    return val


def pos_worth_cnt(s):
    val = 0
    for x in range(n):
        for y in range(n):
            if s.board[x][y] == me:
                val += pos_worth[x][y]
            elif s.board[x][y] == 1-me:
                val -= pos_worth[x][y]
    return val


def stable_pos(m, s):
    stable = True
    xm, ym = m
    for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        x, y = xm + dx, ym + dy
        if 0 <= x < s.n and 0 <= y < s.n and s.board[x][y] != 1 - s.cur_player:
            stable = False
    if stable:
        return 20
    return 0


def stable_disc(m, s, player):
    x, y = m

    a, b = True, True
    for i in range(1, min(x, y) + 1):
        if s.board[x - i][y - i] != player:
            a = False
            break
    for i in range(1, min(n - x, n - y)):
        if s.board[x + i][y + i] != player:
            b = False
            break
    if not a and not b:
        return 0

    a, b = True, True
    for i in range(1, min(n - 1 - x, y) + 1):
        if s.board[x + i][y - i] != player:
            a = False
            break
    for i in range(1, min(x, n - 1 - y) + 1):
        if s.board[x - i][y + i] != player:
            b = False
            break
    if not a and not b:
        return 0

    a, b = True, True
    for i in range(1, x + 1):
        if s.board[x - i][y] != player:
            a = False
            break
    for i in range(1, n - x):
        if s.board[x + i][y] != player:
            b = False
            break
    if not a and not b:
        return 0

    a, b = True, True
    for i in range(1, y + 1):
        if s.board[x][y - i] != player:
            a = False
            break
    for i in range(1, n - y):
        if s.board[x][y + i] != player:
            b = False
            break
    if not a and not b:
        return 0

    return 100


########################################################################################################################
# DUELLER
########################################################################################################################


def write(what):
    sys.stdout.write(what)
    sys.stdout.write('\n')
    sys.stdout.flush()


def read():
    line = sys.stdin.readline().split()
    return line[0], line[1:]


def printerr(what):
    sys.stderr.write(what)
    sys.stderr.write('\n')


game = Game(True)
ja = 1
write('RDY')
game_num = 1
while True:
    cmd, args = read()
    if cmd == 'HEDID':
        move = tuple((int(m) for m in args[2:]))
        if move == (-1, -1):
            move = ()
        else:
            yd, xd = move
            move = (xd, yd)
        game.make_move(move)
        m = pick_move(game, ja)
        game.make_move(m)
        if m:
            write(f'IDO {m[1]} {m[0]}')
        else:
            write('IDO -1 -1')
    elif cmd == 'UGO':
        ja = 0
        m = pick_move(game, ja)
        game.make_move(m)
        if m:
            write(f'IDO {m[1]} {m[0]}')
        else:
            write('IDO -1 -1')
    elif cmd == 'ONEMORE':
        game = Game(True)
        ja = 1
        game_num += 1
        write('RDY')
    elif cmd == 'BYE':
        break
    else:
        pass
