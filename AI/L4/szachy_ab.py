# SZACHY Z ALFA BETA

import chess
import random
import sys

infinity = 999999
d_max = 1
me = True


def pick_move(game):
    global me
    me = game.board.turn
    moves = game.moves_gen()
    if not moves:
        printerr("no moves available")
        exit()
    if len(moves) == 1:
        return moves[0]

    best_moves, value = [], -infinity
    for m in moves:
        game.make_move(m)
        s = min_value(game, -infinity, infinity, 0)
        game.undo_move()
        if s == value:
            best_moves.append(m)
        elif s > value:
            value = s
            best_moves = [m]
    return random.choice(best_moves)


def max_value(game, alpha, beta, d):
    o = game.board.outcome()
    if o:
        if o.winner is None:
            return -1000
        elif o.winner == me:
            return infinity
        else:
            return -infinity
    elif d >= d_max:
        return score(game)
    value = -infinity
    pss = game.moves_gen()
    for m in pss:
        game.make_move(m)
        minval = min_value(game, alpha, beta, d + 1)
        game.undo_move()
        if value < minval:
            value = minval
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value


def min_value(game, alpha, beta, d):
    o = game.board.outcome()
    if o:
        if o.winner is None:
            return -1000
        elif o.winner == me:
            return infinity
        else:
            return -infinity
    elif d >= d_max:
        return score(game)
    value = infinity
    pss = game.moves_gen()
    for m in pss:
        game.make_move(m)
        maxval = max_value(game, alpha, beta, d + 1)
        game.undo_move()
        if maxval < value:
            value = maxval
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value


def score(game):
    o = game.board.outcome()
    if o:
        if o.winner is None:
            return -1000
        elif o.winner == me:
            return infinity
        else:
            return -infinity
    s = checks(game)
    s += material_val(game, me) - material_val(game, me ^ True)
    s += attacks(game, me) - attacks(game, me ^ True) - attackers(game, me) + attackers(game, me ^ True)
    return s


def checks(game):
    if game.board.is_check() and game.board.turn == me:
        return -100
    if game.board.is_check() and game.board.turn == me ^ True:
        return 100
    return 0


def material_val(game, player):
    chess = game.board
    val = 0
    for pos in range(64):
        p = chess.piece_type_at(pos)
        c = chess.color_at(pos)
        if c == player:
            if p == 1:
                val += 1
            elif p == 2 or p == 3:
                val += 3
            elif p == 4:
                val += 5
            elif p == 5:
                val += 9
    return val


def mobility(game, player):
    if player == game.board.turn:
        return game.board.legal_moves.count()
    else:
        return -game.board.legal_moves.count()


def attacks(game, player):
    chess = game.board
    val = 0
    for pos in range(64):
        p = chess.piece_type_at(pos)
        c = chess.color_at(pos)
        if c == player:
            if p == 1:
                val += len(list(chess.attacks(pos)))
            else:
                val += len(list(chess.attacks(pos)))*5
    return val/10


def attackers(game, player):
    chess = game.board
    val = 0
    for pos in range(64):
        p = chess.piece_type_at(pos)
        c = chess.color_at(pos)
        if c == player:
            if p == 1:
                val += len(list(chess.attackers(player ^ True, pos)))
            else:
                val += len(list(chess.attackers(player ^ True, pos)))*5
    return val/10


def printerr(what):
    sys.stderr.write('================================================\n')
    sys.stderr.write(str(what))
    sys.stderr.write('\n================================================\n')


# checkers() → chess.SquareSet
# Gets the pieces currently giving check.
# Returns a set of squares.
# is_check() → bool
# Tests if the current side to move is in check.
# gives_check(move: chess.Move) → bool
# Probes if the given move would put the opponent in check. The move must be at least pseudo-legal