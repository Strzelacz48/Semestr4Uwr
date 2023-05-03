import copy
import queue
import random

# ZADANIE 4 WERSJA DZIAŁAJĄCA

########################################################################################################################
# FUNKCJE 1
########################################################################################################################
import reportlab.graphics.renderSVG


class Stan:
    def __init__(self, t, m):
        self.tab = t
        self.move = m


def read_input():
    fin = open("zad_input.txt", 'r')
    ww = [] #sciany
    gg = [] #cele
    kk = [] #komandosi
    while line := fin.readline()[:-1]:
        w = [False for i in range(len(line))]
        g = [False for i in range(len(line))]
        k = [False for i in range(len(line))]
        for x in range(len(line)):
            if line[x] == "#":
                w[x] = True
            elif line[x] == "G":
                g[x] = True
            elif line[x] == "B":
                g[x] = True
                k[x] = True
            elif line[x] == "S":
                k[x] = True
        ww.append(w)
        gg.append(g)
        kk.append(k)
    fin.close()
    h = len(ww)
    w = len(ww[0])
    return Stan(kk, ""), ww, gg, h, w
    # shallow copy - co to?


def write_output(stan):
    fout = open("zad_output.txt", 'w')
    fout.write(stan.move + '\n')
    fout.close()
    exit()


def printtab(tab):
    # print("\n".join([str(row) for row in tab]))
    for i in tab:
        for j in i:
            if j:
                print("&", end="")
            else:
                print(".", end="")
        print()
    print()

########################################################################################################################


def move_up(stan):
    ludz = stan.tab
    moved = False
    for col in range(1, width - 1):
        for row in range(1, height - 1):
            if ludz[row + 1][col] and not wall[row][col]:
                ludz[row][col] = True
                ludz[row + 1][col] = False
                moved = True
    if moved:
        stan.move += "U"
    return moved


def move_down(stan):
    ludz = stan.tab
    moved = False
    for col in range(1, width - 1):
        for row in range(height - 2, 0, -1):
            if ludz[row - 1][col] and not wall[row][col]:
                ludz[row][col] = True
                ludz[row - 1][col] = False
                moved = True
    if moved:
        stan.move += "D"
    return moved


def move_left(stan):
    ludz = stan.tab
    moved = False
    for row in range(1, height - 1):
        for col in range(1, width - 1):
            if ludz[row][col + 1] and not wall[row][col]:
                ludz[row][col] = True
                ludz[row][col + 1] = False
                moved = True
    if moved:
        stan.move += "L"
    return moved


def move_right(stan):
    ludz = stan.tab
    moved = False
    for row in range(1, height - 1):
        for col in range(width - 2, 0, -1):
            if ludz[row][col - 1] and not wall[row][col]:
                ludz[row][col] = True
                ludz[row][col - 1] = False
                moved = True
    if moved:
        stan.move += "R"
    return moved

########################################################################################################################


def losowe_ruchy(stan, n): # losowo ruszamy w ta sama strone
    while len(stan.move) < n:
        m = random.choice(range(16)) + 1
        modulo = random.choice(range(4))
        for j in range(m):
            if modulo == 0:
                masens = move_up(stan)
            elif modulo == 1:
                masens = move_right(stan)
            elif modulo == 2:
                masens = move_down(stan)
            else:
                masens = move_left(stan)
            if zwyciestwo(stan):
                print("losowo")
                write_output(stan)
                break
            if not masens:
                break
    return stan


def count_s(tab):
    ile = 0
    for i in tab:
        for j in i:
            if j:
                ile += 1
    return ile


def losowe_best(stan, n):# wybiera najlepszy ruh zmniejszajacy niepewnosc
    best = count_s(stan.tab)
    best_len = 0
    bx = -1
    xs = []
    for i in range(n):
        x = losowe_ruchy(copy.deepcopy(stan), 100)
        xs.append(x)
        ile = count_s(x.tab)
        if ile < best:
            best = ile
            bx = i
            best_len = len(x.move)
        elif ile == best and best_len > len(x.move):
            best = ile
            bx = i
            best_len = len(x.move)
        if best == 1:
            break
    return xs[bx]


def zwyciestwo(stan):
    for i in range(height):
        for j in range(width):
            if stan.tab[i][j] and not goal[i][j]:
                return False
    print("wygraliśmy :^)")
    return True


########################################################################################################################
# FUNKCJE 2
########################################################################################################################


def change_representation(stan): # zapisujemy wszystkie pozycje komandosow
    s = []
    for i in range(height):
        for j in range(width):
            if stan.tab[i][j]:
                s.append(Pos(i, j))
    return s


class Pos:
    def __init__(self, r, c):
        self.row = r
        self.col = c


class Labirynt:
    def __init__(self, tab, h):
        self.tab = tab
        self.history = h


def up(lab):
    moved = False
    for s in lab.tab:
        if not wall[s.row - 1][s.col]:
            s.row -= 1
            moved = True
    if moved:
        lab.history += "U"
    return moved


def down(lab):
    moved = False
    for s in lab.tab:
        if not wall[s.row + 1][s.col]:
            s.row += 1
            moved = True
    if moved:
        lab.history += "D"
    return moved


def left(lab):
    moved = False
    for s in lab.tab:
        if not wall[s.row][s.col-1]:
            s.col -= 1
            moved = True
    if moved:
        lab.history += "L"
    return moved


def right(lab):
    moved = False
    for s in lab.tab:
        if not wall[s.row][s.col+1]:
            s.col += 1
            moved = True
    if moved:
        lab.history += "R"
    return moved


def printss(lab):
    for s in lab.tab:
        print(s.row, s.col)
    print()

########################################################################################################################


def write_out(lab):
    fout = open("zad_output.txt", 'w')
    fout.write(lab.history + '\n')
    fout.close()
    exit()


def ss2str(lab):
    w = ""
    for s in lab.tab:
        w += str(s.row) + ' ' + str(s.col) + ' '
    return w


def win(lab):
    for s in lab.tab:
        if not goal[s.row][s.col]:
            return False
    return True


def put_kids(lab, que, done, fun):
    r = copy.deepcopy(lab)
    if fun(r):
        w = ss2str(r)
        if w not in done:
            done.add(w)
            que.put(r)


def bfs(lab):
    que = queue.Queue()
    que.put(lab)
    done = set()
    done.add(ss2str(lab))
    ile = len(lab.history)
    while not que.empty():
        ll = que.get()
        if win(ll):
            print(len(ll.history) - ile, "bfs")
            write_out(ll)
            return True
        if len(ll.history) > 150:
            write_out(ll)
            print("przekroczony limit ruchow")
            return False
        put_kids(ll, que, done, right)
        put_kids(ll, que, done, left)
        put_kids(ll, que, done, up)
        put_kids(ll, que, done, down)
    print(":'(")
    return False


########################################################################################################################
########################################################################################################################

########################################################################################################################
# FAZA 1
########################################################################################################################

stan0, wall, goal, height, width = read_input()
stan0 = losowe_best(stan0, 1000)
# printtab(wall)
# print(stan0.move)
# printtab(stan0.tab)
# print(len(stan0.move))

########################################################################################################################
# FAZA 2
########################################################################################################################

ss = change_representation(stan0)
lab0 = Labirynt(ss, stan0.move)

bfs(lab0)

"""
#####
#B#S#
#SSS#
#SSB#
#S#S#
#SSS#
#SSS#
#####


######################
#SSSSSSSS#SSSSSSSSSBS#
#SSSSSSSSSSSS##SSSSSS#
#SSSSSSSS#############
#SSSSSS###SSSSSSSSSSS#
#SSSSSS###SSSSSSSSSSS#
#SSSSSSSS#SSSSSSSSSSS#
##S#######SSSSSSSSSSS#
#SSSSSSSSSSSSSSSSSSSS#
#SSSSSSSSSSSSSSSSSSSS#
#SSSSSSSSSSSSSSSSSSSS#
#SSSSSSSSSSSSSSSSSSSS#
#SSSSSSSSSSSSSSSSSSSS#
#SSSSSSSSSSSSSSSSSSSS#
#SSSSSSSSSSSSSSSSSSSS#
######################


######################
#SSSSSSSSSSSSSSSSSSBS#
#SSBSSSSBSSSSSSSSSSSS#
#########S#######S####
#SSSSS#SSSSSSSSSSSSSB#
##SSS##SSSS###########
#SSSS#SSSSSSSSSSSSSSS#
#S##S###########SSSSS#
#SSSS#SSSSSSSSSSSSSSS#
#SSSSSSSSSS####SSSSSS#
######################


######################
#SSSSSSSS#SSS##SSSSSS#
#SSSSSSSSSSSS##SSSSSS#
#SSSSSS###SSSSSSSSS#B#
#SSSSSS###SSSSSSSSSSS#
#SSSSSSSSSSSSSSSSSSSS#
#####SSSSSSSSSSSSSSSS#
#SSSSSSSSSSSSSSSSSSSS#
######################
"""
