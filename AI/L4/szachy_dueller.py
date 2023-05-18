# COŚ CO KOMUNIKUJE SIĘ ZE SPRAWDZACZKĄ SKOSOWĄ
#agent_1 = "szachy_ab.py"
import copy
import sys
from game import Chess
import chess
#from agent_1 import pick_move  # TU WRZUĆ TO CO MA WYBIERAĆ RUCHY
from szachy_ab import pick_move  # TU WRZUĆ TO CO MA WYBIERAĆ RUCHY


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
    sys.stderr.write('************************************************\n')
    sys.stderr.write(what)
    sys.stderr.write('\n************************************************\n')


def reset():
    global game, my_player
    game = Chess()
    my_player = 1
    write('RDY')


def loop():
    global game, my_player
    while True:
        cmd, args = read()
        if cmd == 'HEDID':
            unused_move_timeout, unused_game_timeout = args[:2]
            move = args[2]
            game.make_move(move)
        elif cmd == 'ONEMORE':
            reset()
            continue
        elif cmd == 'BYE':
            break
        else:
            assert cmd == 'UGO'
            # assert not self.game.move_list
            my_player = 0

        move = pick_move(game)
        # printerr(move)
        game.make_move(move)
        write('IDO ' + move)


if __name__ == '__main__':
    game = Chess()
    my_player = 1
    write('RDY')
    loop()
