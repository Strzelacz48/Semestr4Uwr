# SZACHY Z MONTE CARLO

import copy

import chess
import sys
import math
import random


class Node:
    def __init__(self, m, t, n, k, d):
        self.last_move = m
        self.score = t
        self.visits = n
        self.kids = k
        self.dad = d


me = True
games_per_roll = 10
mcts_iterations = 20
magical_const = 1
infinity = 999999


def pick_move(game0):
    game = copy.deepcopy(game0)
    global me
    me = game.board.turn
    tree = Node("", 0, 0, [], None)
    expand(tree, game)
    for k in tree.kids:
        k.score = get_move_value(k.last_move, game)
    to_undo = 0
    for n in range(mcts_iterations):
        cur = tree
        while cur.kids:
            vals = [(ucb(k, n), k) for k in cur.kids]
            cur = max(vals, key=lambda v: v[0])[1]
            game.make_move(cur.last_move)
            to_undo += 1
        if cur.visits != 0:
            expand(cur, game)
            if cur.kids:
                cur = random.choice(cur.kids)
                game.make_move(cur.last_move)
                to_undo += 1
        score = rollout(cur, game)
        backpr(score, cur)
        for _ in range(to_undo):
            game.undo_move()
        to_undo = 0
    t = []
    for k in tree.kids:
        if k.visits != 0 and k.last_move:
            t.append((k.score / k.visits, k.last_move))
    if t:
        m = max(t, key=lambda v: v[0])[1]
        # printerr(m)
        return m
    else:
        print("no moves found")
        exit()


def backpr(scr, node):
    while node.dad:
        node.score += scr
        node.visits += 1
        node = node.dad


def expand(node, state):
    possibles = state.moves_gen()
    for m in possibles:
        node.kids.append(Node(m, 0, 0, [], node))


def ucb(node, n):
    if node.visits == 0:
        return infinity+node.score
    return node.score / node.visits + magical_const * math.sqrt(math.log2(n) / node.visits)


def rollout(node, state):
    score = 0
    for _ in range(games_per_roll):
        s = copy.deepcopy(state)
        n = 0
        while True:
            n += 1
            mg = s.moves_gen()
            if mg:
                s.make_move(random.choice(mg))
            else:
                if s.board.turn == me:
                    score -= 1
                else:
                    score += 1
                break
            out = s.board.outcome()
            if out:
                if out.winner is None:
                    pass
                elif out.winner == me:
                    score += 1
                else:
                    score -= 1
                break
            if n > 20:
                break
    return score


def get_move_value(move, game):
    o = game.make_move(move)
    s = 0
    if o:
        if o.winner is None:
            s -= 1
        elif o.winner == me:
            s += infinity
        else:
            s -= infinity
    else:
        s += eval_board(game)
    game.undo_move()
    return s/100


def eval_board(game):
    s = material_val(game, me) - material_val(game, me ^ True)
    s += (checks(game) + attacks(game, me) - attacks(game, me ^ True) - attackers(game, me) + attackers(game, me ^ True))
    return s


def checks(game):
    if game.board.is_check and game.board.turn == me:
        return -999
    if game.board.is_check and game.board.turn == me ^ True:
        return 999


def material_val(game, player):
    chess = game.board
    val = 0
    for pos in range(63):
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
    for pos in range(63):
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
    for pos in range(63):
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
