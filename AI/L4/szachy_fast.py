# SZACHY BŁYSKAWICZNE - TYLKO HEURYSTYKA, RÓŻNE PARAMETRY

import chess
import random
import sys

infinity = 999999
me = True
params = None


def pick_move(game, prr):
    global me, params
    me = game.board.turn
    params = prr
    moves = game.moves_gen()
    if not moves:
        exit()
    if len(moves) == 1:
        return moves[0]

    best_moves, value = [], -infinity
    for m in moves:
        game.make_move(m)
        s = score(game)
        game.undo_move()
        if s == value:
            best_moves.append(m)
        elif s > value:
            value = s
            best_moves = [m]
    return random.choice(best_moves)


def score(game):
    s = 0
    s += material_val(game, me) - material_val(game, me ^ True)
    s += params.alpha * mobility(game, me) - params.alpha * mobility(game, me ^ True)

    o = game.board.outcome()
    if o:
        if o.winner is None:
            return infinity/2 if s > 0 else -infinity/2
        elif o.winner == me:
            return infinity
        else:
            return -infinity

    return s


def material_val(game, player):
    chess = game.board
    val = 0
    for pos in range(64):
        p = chess.piece_type_at(pos)
        c = chess.color_at(pos)
        if c == player and p in range(1, 6):
            val += params[p]
    return val


def mobility(game, player):
    if player == game.board.turn:
        return game.board.legal_moves.count()
    else:
        game.board.turn ^= True
        v = game.board.legal_moves.count()
        game.board.turn ^= True
        return v

