# ZADANIE 5 Z PRACOWNI 2

import copy
import queue
import random
import time


def my_deepcopy(lab):
    pri = copy.copy(lab.pri)
    his = copy.copy(lab.history)
    ss = []
    for s in lab.ss:
        ss.append([copy.copy(s[0]), copy.copy(s[1])])
    return Labirynt(ss, his, pri)


class Labirynt:
    def __init__(self, ss, h, pri):
        self.pri = pri
        self.ss = ss
        self.history = h

    def __lt__(self, other):#less
        return self.pri < other.pri

    def __le__(self, other):#less or equal
        return self.pri <= other.pri

    def __gt__(self, other):#greater
        return self.pri > other.pri

    def __ge__(self, other):#greater or equal
        return self.pri >= other.pri

    def __eq__(self, other):#equal
        return self.pri == other.pri


def read_input():
    fin = open("zad_input.txt", 'r')
    ww = []
    gg = []
    row = 0
    ss = []
    gs = []
    while line := fin.readline()[:-1]:
        w = [False for i in range(len(line))]
        g = [False for i in range(len(line))]
        for x in range(len(line)):
            if line[x] == "#":
                w[x] = True
            elif line[x] == "G":
                g[x] = True
                gs.append((row, x))
            elif line[x] == "S":
                ss.append([row, x])
            elif line[x] == "B":
                g[x] = True
                gs.append((row, x))
                ss.append([row, x])
        ww.append(w)
        gg.append(g)
        row += 1
    fin.close()
    h = len(ww)
    w = len(ww[0])
    odl = odl_init(gs, h, w, ww)
    return Labirynt(ss, "", 0), ww, gg, gs, h, w, odl


def odl_init(gs, h, w, wal):
    odl = []
    inf = 10000
    for i in range(h):
        o = []
        for j in range(w):
            o.append(inf)
        odl.append(o)

    for g in gs:
        maly_bfs(g, odl, wal)
        # print("ooo")

    return odl


def maly_bfs(g0, odl, wal): # do liczenia odległości od G dla każdego dobrego punktu
    que = queue.Queue()
    que.put((g0[0], g0[1], 0))
    done = set()
    done.add((g0[0], g0[1], 0))
    while not que.empty():
        p = que.get()
        odl[p[0]][p[1]] = min(odl[p[0]][p[1]], p[2])
        x = (p[0]-1, p[1], odl[p[0]][p[1]]+1)
        if x not in done and not wal[p[0]-1][p[1]]:
            que.put(x)
            done.add(x)
        x = (p[0]+1, p[1], odl[p[0]][p[1]]+1)
        if x not in done and not wal[p[0]+1][p[1]]:
            que.put(x)
            done.add(x)
        x = (p[0], p[1]-1, odl[p[0]][p[1]]+1)
        if x not in done and not wal[p[0]][p[1]-1]:
            que.put(x)
            done.add(x)
        x = (p[0], p[1] + 1, odl[p[0]][p[1]] + 1)
        if x not in done and not wal[p[0]][p[1] + 1]:
            que.put(x)
            done.add(x)


def write_out(lab):
    fout = open("zad_output.txt", 'w')
    fout.write(lab.history + '\n')
    # printss(lab)
    fout.close()
    print("time: ", time.process_time())
    exit()


def updatess(lab):
    if len(lab.ss) <= 1:
        return
    elif len(lab.ss) < 5:
        lab.ss.sort()
        i = 1
        while i < len(lab.ss):
            while i < len(lab.ss) and lab.ss[i - 1] == lab.ss[i]:
                lab.ss.remove(lab.ss[i])
            i += 1
    else:
        tt = []
        for _ in range(height):
            tt.append([False for _ in range(width)])
        for s in lab.ss:
            tt[s[0]][s[1]] = True

        lab.ss = []
        for t in range(height):
            for i in range(width):
                if tt[t][i]:
                    lab.ss.append([t, i])


def up(lab):
    moved = False
    for s in lab.ss:
        if not wall[s[0] - 1][s[1]]:
            s[0] -= 1
            moved = True
    if moved:
        lab.history += "U"
        updatess(lab)
    return moved


def down(lab):
    moved = False
    for s in lab.ss:
        if not wall[s[0] + 1][s[1]]:
            s[0] += 1
            moved = True
    if moved:
        lab.history += "D"
        updatess(lab)
    return moved


def left(lab):
    moved = False
    for s in lab.ss:
        if not wall[s[0]][s[1] - 1]:
            s[1] -= 1
            moved = True
    if moved:
        lab.history += "L"
        updatess(lab)
    return moved


def right(lab):
    moved = False
    for s in lab.ss:
        if not wall[s[0]][s[1] + 1]:
            s[1] += 1
            moved = True
    if moved:
        lab.history += "R"
        updatess(lab)
    return moved


def printss(lab):
    for s in lab.ss:
        print(s[0], s[1])
    print()


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


def ss2str(lab):
    w = ""
    for s in lab.ss:
        w += str(s[0]) + ' ' + str(s[1]) + ' '
    return w


def win(lab):
    for s in lab.ss:
        if not goal[s[0]][s[1]]:
            return False
    return True


def priority(lab):  # arrival cost + estimated future cost
    efc = 0

    for s in lab.ss:
        su = odl[s[0]][s[1]]
        efc = max(efc, su)

    return efc + len(lab.history)


def put_kids(lab, que, fun):
    r = my_deepcopy(lab)
    if fun(r):
        r.pri = priority(r)
        que.put(r)


def bfs(lab):
    que = queue.PriorityQueue()
    que.put(lab)
    done = set()
    while not que.empty():
        ll = que.get()
        if ss2str(ll) in done:
            continue
        done.add(ss2str(ll))
        if win(ll):
            print(len(ll.history), "kroków")
            write_out(ll)
            return True
        put_kids(ll, que, right)
        put_kids(ll, que, left)
        put_kids(ll, que, up)
        put_kids(ll, que, down)
    print(":'(")
    write_out(lab)
    return False


########################################################################################################################


l0, wall, goal, goal_list, height, width, odl = read_input()
# for x in odl:
#    print(x)
# for i in range(height):
#    for j in range(width):
#        if odl[i][j]<10000:
#            print(odl[i][j], end=" ")
#        else:
#            print("#", end=" ")
#    print()

bfs(l0)
