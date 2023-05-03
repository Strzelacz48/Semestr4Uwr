import random
from typing import Set, Any


def next_perm(perm, n, arr, dl, inn, out, pref, to_xor):
    k = n-1
    if perm[k] + dl[k] == len(arr):
        k -= 1
        while k >= 0 and perm[k] + dl[k] + 1 == perm[k + 1]:
            k -= 1
        if k < 0:
            return to_xor
        else:
            perm[k] += 1
            x = perm[k] + dl[k] + 1
            for i in range(k+1, n):
                perm[i] = x
                x += dl[i] + 1
            # pref update
            if k == 0:
                if arr[perm[k]-1] == 1:
                    pref += 1
            else:
                if arr[perm[k]-1] == 1:
                    out[k-1] += 1
            x = perm[k]
            for kk in range(k, n):
                inn[kk] = 0
                out[kk] = 0
                for i in range(dl[kk]):
                    if arr[x] == 0:
                        inn[kk] += 1
                    x += 1
                if x < len(arr) and arr[x] == 1:
                    out[kk] += 1
                x += 1
            for i in range(x, len(arr)):
                if arr[i] == 1:
                    out[n - 1] += 1
    else:
        perm[k] += 1
        if arr[perm[k] - 1] == 1:
            if k != 0:
                out[k - 1] += 1
            else:
                pref += 1
        else:
            inn[k] -= 1
        if arr[perm[k] + dl[k] - 1] == 1:
            out[k] -= 1
        else:
            inn[k] += 1
    to_xor = min(to_xor, sum(inn) + sum(out) + pref)
    #print(to_xor)
    #print(perm)
    #print()
    return next_perm(perm, n, arr, dl, inn, out, pref, to_xor)


def opt_dist(arr, dl):
    out = [] # do xororwania za k-tym blokiem
    inn = [] # do xorowania wewn k-tego bloku
    pref = 0 # do xorowania przed pierwszym
    n = len(dl)
    x = 0
    start = []
    for k in range(n):
        start.append(x)
        inn.append(0)
        out.append(0)
        for i in range(dl[k]):
            if arr[x] == 0:
                inn[k] += 1
            x += 1
        if x < len(arr) and arr[x] == 1:
            out[k] += 1
        x += 1
    for i in range(x, len(arr)):
        if arr[i] == 1:
            out[n-1] += 1
    to_xor = sum(inn) + sum(out)
    return next_perm(start, n, arr, dl, inn, out, pref, to_xor)

###############################################################
###############################################################


def read_input():
    global width, height, dr, dc
    fin = open("zad_input.txt", 'r')
    line = fin.readline()[:-1]
    xy = line.split(" ")
    height = int(xy[0])
    width = int(xy[1])
    sdr = []
    for i in range(height):
        line = fin.readline()[:-1]
        ts = line.split(" ")
        ti = []
        for c in ts:
            ti.append(int(c))
        sdr.append(tuple(ti))
    dr = tuple(sdr)
    sdc = []
    for i in range(width):
        line = fin.readline()[:-1]
        ts = line.split(" ")
        ti = []
        for c in ts:
            ti.append(int(c))
        sdc.append(tuple(ti))
    dc = tuple(sdc)
    fin.close()
    return width, height, dr, dc


def write_output(tab):
    fout = open("zad_output.txt", 'w')
    for t in tab:
        for i in t:
            if i:
                fout.write(znak[0])
            else:
                fout.write(znak[1])
        fout.write("\n")
    print("eureka!!!")
    fout.close()
    exit()


def maketab(x, y):
    rows = []
    for i in range(y):
        t = []
        for j in range(x):
            t.append(random.choice((True, False)))
        rows.append(t)
    cols = []
    for j in range(x):
        t = [False for i in range(y)]
        cols.append(t)
    for j in range(x):
        for i in range(y):
            cols[j][i] = rows[i][j]
    return rows, cols


def printtab(tab):
    for t in tab:
        for i in t:
            if i:
                print(znak[0], end="")
            else:
                print(znak[1], end="")
        print()
    print()


def check_rows_cols(rows, cols):
    for i in range(height):
        for j in range(width):
            if rows[i][j] != cols[j][i]:
                print("!")


def b_init():
    bad_rows, bad_cols = [], []
    for i in range(height):
        bad_rows.append(i)
    for i in range(width):
        bad_cols.append(i)
    brt = [True for i in range(height)]
    bct = [True for i in range(width)]
    return bad_rows, bad_cols, brt, bct


def opt_init(row, col):
    row_opt = []
    for i in range(height):
        row_opt.append(opt_dist(row[i], dr[i]))
    col_opt = []
    for i in range(width):
        col_opt.append(opt_dist(col[i], dc[i]))
    return row_opt, col_opt


def rozw():
    row, col = maketab(width, height)
    row_opt, col_opt = opt_init(row, col)
    bad_rows, bad_cols, br_t, bc_t = b_init()
    for round in range(100000):
        which = random.choice((True, False))
        if which:
            if fcja(row, col, bad_rows, bad_cols, br_t, bc_t, height, width, dr, dc, row_opt, col_opt):
                write_output(row)
        else:
            if fcja(col, row, bad_cols, bad_rows, bc_t, br_t, width, height, dc, dr, col_opt, row_opt):
                write_output(row)


def fcja(tab_x, tab_y, bad_x, bad_y, ifb_x, ifb_y, siz_x, siz_y, dx, dy, opt_x, opt_y):
    if len(bad_x) == 0:
        return False
    x = random.choice(bad_x)
    best = -100
    y_xor = 0
    oo_x = 0
    oo_y = 0
    yy = random.sample(range(siz_y), max(siz_y//2, 1))
    for y in yy:
        tab_x[x][y] ^= 1
        tab_y[y][x] ^= 1
        o_x = opt_dist(tab_x[x], dx[x])
        o_y = opt_dist(tab_y[y], dy[y])
        dif = opt_x[x] + opt_y[y] - o_x - o_y
        if dif > best:
            best = dif
            y_xor = y
            oo_x = o_x
            oo_y = o_y
        tab_x[x][y] ^= 1
        tab_y[y][x] ^= 1

    tab_x[x][y_xor] ^= 1
    tab_y[y_xor][x] ^= 1
    opt_x[x] = oo_x
    opt_y[y_xor] = oo_y
    if not ifb_y[y_xor] and oo_y > 0:
        bad_y.append(y_xor)
        ifb_y[y_xor] = True
    elif oo_y == 0 and ifb_y[y_xor]:
        bad_y.remove(y_xor)
        ifb_y[y_xor] = False
    if oo_x == 0:
        bad_x.remove(x)
        ifb_x[x] = False

    if len(bad_y) == len(bad_x) == 0:
        return True
    return False

    # losuj czy wiersz czy kolumna
    # losuj po 3 elementy i sprawdź poprawę
    # wybierz opcję z najlepszą poprawą i zmień na stałe


global width, height, dr, dc
znak = ("#", ".")
read_input()
for rrr in range(10):
    rozw()
write_output([["przegraliśmy :'("]])

# s = [2, 3, 4, 2]
# arr = [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1]
# print(opt_dist(arr, s))

# osobne listy: bad_rows i bad_columns
# obrócona tablica, żeby nie przepisywać
# startuj z samych dobrych wierszy
# przesunięcia bloków zamiast xorowania pikseli
# zrób szybszy opt_dist

"""
10 10
4
6
3 4
4 5
4 5
5 4
5 2
6
6
2 2
3
5
9
10
2 4
5 3
6 3
9
5
3
"""