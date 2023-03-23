# P1 ZAD 5 (OBRAZKI LOGICZNE)
import random

def opt_dist(arr, dl):
    pref = 0
    suf = 0
    inn = 0
    for i in range(dl):
        if arr[i] == 0:
            inn += 1
    for i in range(dl, len(arr)):
        if arr[i] == 1:
            suf += 1
    x = pref + inn + suf
    a = 1
    b = dl
    while b < len(arr):
        if arr[a-1] == 1:
            pref += 1
        else: # arr[a-1] == 0
            inn -= 1
        if arr[b] == 1:
            suf -= 1
        else: # arr[b] == 0
            inn += 1
        x = min(x, pref + suf + inn)
        a += 1
        b += 1
    return x


def printtab(tab):
    for i in range(y):
        for j in tab[i]:
            fout.write(znak[j])
        fout.write("\n")


def maketab(x, y):
    tab = []
    for i in range(y):
        t = []
        for j in range(x):
            t.append(random.choice(range(2)))
        tab.append(t)
    return tab


def makelist(n):
    s = []
    for i in range(n):
        s.append(i)
    return s


def opt_init(x, y, tab, dls):
    opt_lines = []
    opt_columns = []
    for i in range(y):
        opt_lines.append(opt_dist(tab[i], dls[0][i]))
    for j in range(x):
        arr = []
        for i in range(y):
            arr.append(tab[i][j])
        opt_columns.append(opt_dist(arr, dls[1][j]))
    return [opt_lines, opt_columns]


def szukaj_rozw (x, y, dls):# ^ xor | or
    tab = maketab(x, y)
    bad = makelist(x)
    opts = opt_init(x, y, tab, dls)
    koniec = False
    #print(opts)
    #printtab(tab)
    for round in range(N):
        column = random.choice(bad)
        #print(column)
        arr = []
        for i in range(y):
            arr.append(tab[i][column])
        maxi = -1000
        to_xor = -1
        for i in range(y):
            tab[i][column] ^= 1
            arr[i] ^= 1
            opt_lin = opt_dist(tab[i], dls[0][i])
            opt_col = opt_dist(arr, dls[1][column])
            dif = opts[0][i] + opts[1][column] - opt_lin - opt_col
            if dif > maxi:
                maxi = dif
                to_xor = i
            tab[i][column] ^= 1
            arr[i] ^= 1
        tab[to_xor][column] ^= 1
        arr[to_xor] ^= 1
        opts[1][column] = opt_dist(arr, dls[1][column])
        opts[0][to_xor] = opt_dist(tab[to_xor], dls[0][to_xor])
        if opts[1][column] == 0:
            bad.remove(column)
        if len(bad) == 0:
            for i in range(x):
                bad.append(i)
            koniec = True
            for line in range(y):
                if opts[0][line] != 0:
                    koniec = False
                    break
        if koniec:
            break

        #printtab(tab)
        #print(bad)
        #print()
    if koniec:
        printtab(tab)
        return True
    else:
        #printtab(tab)
        #fout.write('\n')
        return False


###############################################################
###############################################################

fin = open("zad5_input.txt", 'r')
fout = open("zad5_output.txt", 'w')
znak = [".", "#"]
line = fin.readline()[:-1]
xy = line.split(" ")
x = int(xy[0])
y = int(xy[1])
N = min(100000, x*y*1000)
#print(N)
dls = [[], []]
for i in range(y):
    line = fin.readline()[:-1]
    dls[0].append(int(line))
for i in range(x):
    line = fin.readline()[:-1]
    dls[1].append(int(line))

for rounda in range(100):
    if szukaj_rozw(x, y, dls):
        break
    print(rounda)

fin.close()
fout.close()

"""
7 7
1
3
5
7
5
3
1
7
5
5
3
3
1
1


12 12
0
0
8
8
8
8
8
8
8
8
0
0
0
0
8
8
8
8
8
8
8
8
0
0
"""
