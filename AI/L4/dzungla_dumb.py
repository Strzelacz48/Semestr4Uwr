#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import copy
import random
from collections import namedtuple
import sys

board_width = 7
board_height = 9

board = [['.', '.', '#', '*', '#', '.', '.'],
         ['.', '.', '.', '#', '.', '.', '.'],
         ['.', '.', '.', '.', '.', '.', '.'],
         ['.', '~', '~', '.', '~', '~', '.'],
         ['.', '~', '~', '.', '~', '~', '.'],
         ['.', '~', '~', '.', '~', '~', '.'],
         ['.', '.', '.', '.', '.', '.', '.'],
         ['.', '.', '.', '#', '.', '.', '.'],
         ['.', '.', '#', '*', '#', '.', '.']]

bd0 = [['L', '.', '.', '.', '.', '.', 'T'],
       ['.', 'D', '.', '.', '.', 'C', '.'],
       ['R', '.', 'J', '.', 'W', '.', 'E'],
       ['.', '.', '.', '.', '.', '.', '.'],
       ['.', '.', '.', '.', '.', '.', '.'],
       ['.', '.', '.', '.', '.', '.', '.'],
       ['e', '.', 'w', '.', 'j', '.', 'r'],
       ['.', 'c', '.', '.', '.', 'd', '.'],
       ['t', '.', '.', '.', '.', '.', 'l']]

Stan = namedtuple('Stan', [
	'player', 'pieces', 'board_pieces', 'no_beats', 'who_moved_snd'
])
# e = ('.', '#', '*', '~', 'E', 'L', 'T', 'J', 'W', 'D', 'C', 'R')
piece_num = {'E': 0, 'L': 1, 'T': 2, 'J': 3, 'W': 4, 'D': 5, 'C': 6, 'R': 7,
             'e': 0, 'l': 1, 't': 2, 'j': 3, 'w': 4, 'd': 5, 'c': 6, 'r': 7}
piece_letter = [['E', 'L', 'T', 'J', 'W', 'D', 'C', 'R'], ['e', 'l', 't', 'j', 'w', 'd', 'c', 'r']]
P = namedtuple('P', ['E', 'L', 'T', 'J', 'W', 'D', 'C', 'R'])
elephant, lion, tiger, panther, wolf, dog, cat, rat = 0, 1, 2, 3, 4, 5, 6, 7
den = [(0, 3), (8, 3)]
player_0_start = [(2, 6), (0, 0), (0, 6), (2, 2), (2, 4), (1, 1), (1, 5), (2, 0)]  # 0 na górze
player_1_start = [(6, 0), (8, 6), (8, 0), (6, 4), (6, 2), (7, 5), (7, 1), (6, 6)]  # 1 na dole


def moves_gen(s):
	moves = []
	for p in range(8):
		if not s.pieces[s.player][p]:
			continue
		for m in ((0, 1), (1, 0), (0, -1), (-1, 0)):
			newp = (s.pieces[s.player][p][0] + m[0], s.pieces[s.player][p][1] + m[1])
			if valid_move(p, s.pieces[s.player][p], newp, s):
				moves.append((p, s.pieces[s.player][p], newp))
	for p in (lion, tiger):
		if not s.pieces[s.player][p]:
			continue
		for m in ((0, 1), (1, 0), (0, -1), (-1, 0)):
			x = jump(p, s.pieces[s.player][p], m, s)
			if x:
				moves.append((p, s.pieces[s.player][p], x))
	return moves

#sprawdza czy ruch nie wychodzi poza plansze i czy nie jest na polu z wlasnym pionkiem/ nie może zbić/ nie może wejść na pole
def valid_move(piece, prev_pos, new_pos, s):
	nx, ny = new_pos
	if not (0 <= nx < board_height and 0 <= ny < board_width):
		return False
	if is_mine(s.board_pieces[nx][ny], s.player):
		return False
	if new_pos == den[s.player]:
		return False
	if board[nx][ny] == '~' and piece != rat:
		return False
	if is_enemy(s.board_pieces[nx][ny], s.player) and not can_beat(s.board_pieces[nx][ny], piece, s.player, prev_pos, new_pos):
		return False
	return True


def is_mine(sgn, player):
	if sgn == '.':
		return False
	if player == 0:
		return sgn.isupper()
	else:
		return sgn.islower()


def is_enemy(sgn, player):
	if sgn == '.':
		return False
	if player == 0:
		return sgn.islower()
	else:
		return sgn.isupper()


def can_beat(sgn, piece, player, prev_pos, new_pos):
	if not is_enemy(sgn, player):
		return False
	if board[new_pos[0]][new_pos[1]] == '#':
		return True
	if piece == rat:
		if board[prev_pos[0]][prev_pos[1]] == '~' and board[new_pos[0]][new_pos[1]] != '~':
			return False
		if piece_num[sgn] == elephant:
			return True
	if piece == elephant:
		if piece_num[sgn] == rat:
			return False
	if piece_num[sgn] >= piece:
		return True
	return False


def sth_to_beat(ps, s):
	for m in ps:
		piece, prev, newp = m
		nx, ny = newp
		if can_beat(s.board_pieces[nx][ny], piece, s.player, prev, newp):
			return True
	return False


def jump(piece, pos, move, s):
	dx, dy = move[0], move[1]
	nx, ny = pos[0] + dx, pos[1] + dy
	if not (0 <= nx < board_height and 0 <= ny < board_width):
		return False
	if board[nx][ny] != '~':
		return False
	while board[nx][ny] == '~':
		if s.board_pieces[nx][ny].lower() == 'r' and is_enemy(s.board_pieces[nx][ny], s.player):# and piece != enemy rat:
			return False
		nx += dx
		ny += dy
	if valid_move(piece, pos, (nx, ny), s):
		return nx, ny
	return False


def make_move(m, s):
	player, pieces, board_pieces, no_beats, wms = s
	if not m:
		return Stan(1 - player, pieces, board_pieces, no_beats + 1, wms)
	piece, prev, newp = m
	nx, ny = newp
	if can_beat(board_pieces[nx][ny], piece, player, prev, newp):
		pieces[1 - player][piece_num[board_pieces[nx][ny]]] = ()
		no_beats = 0
	else:
		no_beats += 1
	board_pieces[prev[0]][prev[1]] = '.'
	board_pieces[nx][ny] = piece_letter[player][piece]
	pieces[player][piece] = newp
	return Stan(1 - player, pieces, board_pieces, no_beats, wms)


def print_board(s):
	print(f'player = {s.player}, last beat {s.no_beats} ago')
	for line in s.board_pieces:
		for i in line:
			print(i, end="")
		print()

# 
def endgame(s):
	# print(s.no_beats)
	if s.board_pieces[den[0][0]][den[0][1]] != '.' or s.board_pieces[den[1][0]][den[1][1]] != '.':
		# print(':)')
		return True
	if s.no_beats >= 30:# 30 ruchow bez bicia
		return True
	o = True
	for p in (0, 1):# sprawdza czy ktorys z graczy nie ma juz pionkow
		for i in s.pieces[p]:
			if i:
				o = False
				break
	return o


def agent_move(s, pick):
	m = pick(s)
	return make_move(m, s)


def pick_random(possibles, s):
	return random.choice(possibles)


def winner(s):
	if s.board_pieces[den[0][0]][den[0][1]] != '.':
		# print('base 1')
		return 1, 'base'
	if s.board_pieces[den[1][0]][den[1][1]] != '.':
		# print('base 0')
		return 0, 'base'
	for i in range(8):
		if s.pieces[0][i] and not s.pieces[1][i]:
			return 0, 'best piece'
		if s.pieces[1][i] and not s.pieces[0][i]:
			return 1, 'best piece'
	return s.who_moved_snd, 'player 1'


########################################################################################################################


def pick_move_fast(s):
	possibles = moves_gen(s)
	if not possibles:
		return ()
	me = s.player
	if me != ja:
		print("ivnsfkgcvgctxtchgvnake")
		exit()
	#ss = Stan(s.player, copy.deepcopy(s.pieces), copy.deepcopy(s.board_pieces), 0, s.who_moved_snd)
	vals = []
	for m in possibles:
		new_s = copy.deepcopy(s)
		new_s = make_move(m, new_s)
		value = eval_board(new_s, me)
		vals.append((m, value))
	# print_board(ss)
	# print((m, value))
	return max(vals, key=lambda v: v[1])[0]


def pick_move(s):
	possibles = moves_gen(s)
	if not possibles:
		return ()
	me = s.player
	vals = []
	for m in possibles:
		new_s = copy.deepcopy(s)
		new_s = make_move(m, new_s)
		# value = eval_board(new_s, me)
		# vals.append((m, value))
		vals.append((m, minmax(new_s, me, 0)))
	# print_board(ss)
	# print((m, value))
	return max(vals, key=lambda v: v[1])[0]


def minmax(s, me, d):
	if endgame(s):
		w, cs = winner(s)
		if cs == 'player 1' and w == me:
			return 100
		if cs == 'best piece' and w == me:
			return 200
		if cs == 'base' and w == me:
			return 1000
		else:
			return -1000
	if end_minmax(s, d):
		return eval_board(s, me)

	values = []
	ps = moves_gen(s)
	for i in ps:
		new_s = copy.deepcopy(s)
		new_s = make_move(i, new_s)
		values.append(minmax(new_s, me, d + 1))

	if not values:
		if s.player == me:
			return -100
		else:
			return 100
	if s.player == me:
		return max(values)
	else:
		return min(values)


def end_minmax(s, d):
	if d >= 2:
		return True
	if d < 2:
		return False
	ps = moves_gen(s)
	if sth_to_beat(ps, s):
		return False
	return True


def eval_board(s, me):
	my_value = 0
	op_value = 0
	eps = 0.1
	fig_val = [11, 9, 7, 4, 3, 2, 1, 6]  # [14, 11, 10, 6, 5, 3, 2, 8]
	my_dists = []
	op_dists = []
	for p in range(8):#sumowanie odleglosci od nory i wartosci pionkow obu graczy
		if s.pieces[me][p]:
			my_value += fig_val[p]
			my_dists.append(dist(s.pieces[me][p], den[1 - me]))
		if s.pieces[1 - me][p]:
			op_value += fig_val[p]
			op_dists.append(dist(s.pieces[1 - me][p], den[me]))
	if my_dists:
		my_value -= min(my_dists)
	my_value -= sum(my_dists) * eps
	if op_dists:
		op_value -= min(op_dists)
	op_value -= sum(op_dists) * eps
	if s.player == me:#dodawanie wartosci mozliwych ruchow im wiecej tym lepiej
		my_value += len(moves_gen(s))
	else:
		op_value += len(moves_gen(s))
	value = my_value - op_value
	# print(sum(my_dists), sum(op_dists))
	# print(min(my_dists), min(op_dists))
	return value


def dist(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])


def pick_move_AB(s):
	return max_value(s, s.player, -1000000000, 1000000000, 0)[1]


def max_value(s, me, alpha, beta, d):
	if endgame(s):
		w, r = winner(s)
		if w == me:
			return 1000, ()
		else:
			return -1000, ()
	elif d > 2:
		return eval_board(s, me)
	value = -1000000000
	best_move = ()
	pss = moves_gen(s)
	for m in pss:
		s1 = make_move(m, copy.deepcopy(s))
		minval, bm = min_value(s1, me, alpha, beta, d+1)
		if value < minval:
			value = minval
			best_move = m
		if value >= beta:
			return value, best_move
		alpha = max(alpha, value)
	return value, best_move


def min_value(s, me, alpha, beta, d):
	if endgame(s):
		w, r = winner(s)
		if w == me:
			return 1000, ()
		else:
			return -1000, ()
	elif d > 2:
		return eval_board(s, me), ()
	value = 1000000000
	best_move = ()
	pss = moves_gen(s)
	for m in pss:
		s1 = make_move(m, copy.deepcopy(s))
		maxval, bm = max_value(s1, me, alpha, beta, d+1)
		if maxval < value:
			value = maxval
			best_move = m
		if value <= alpha:
			return value, best_move
		beta = min(beta, value)
	return value, best_move


def write(what):
	sys.stdout.write(what)
	sys.stdout.write('\n')
	sys.stdout.flush()


def read():
	line = sys.stdin.readline().split()
	return line[0], line[1:]


st = Stan(1, [copy.deepcopy(player_0_start), copy.deepcopy(player_1_start)], copy.deepcopy(bd0), 0, 0)
ja = 0
write('RDY')
while True:
	cmd, args = read()
	if cmd == 'HEDID':
		move = tuple((int(m) for m in args[2:]))
		if move == (-1, -1, -1, -1):
			move = ()
		else:
			ys, xs, yd, xd = move
			move = (piece_num[st.board_pieces[xs][ys]], (xs, ys), (xd, yd))
		st = make_move(move, st)
		m = pick_move_AB(st)
		if m:
			st = make_move(m, st)
			p, a, b = m
			write(f'IDO {a[1]} {a[0]} {b[1]} {b[0]}')
		else:
			write('IDO -1 -1 -1 -1')
	elif cmd == 'UGO':
		ja = 1
		m = pick_move_AB(st)
		if m:
			st = make_move(m, st)
			p, a, b = m
			write(f'IDO {a[1]} {a[0]} {b[1]} {b[0]}')
		else:
			write('IDO -1 -1 -1 -1')
	elif cmd == 'ONEMORE':
		st = Stan(1, [copy.deepcopy(player_0_start), copy.deepcopy(player_1_start)], copy.deepcopy(bd0), 0, 0)
		ja = 0
		write('RDY')
	elif cmd == 'BYE':
		break

# random vs fast 0-0-100
# baloo vs minmax 15-0-85
# baloo vs AB 37-0-963

