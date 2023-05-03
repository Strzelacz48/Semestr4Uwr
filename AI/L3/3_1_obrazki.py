import copy
import queue

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
                fout.write(znak[1])
            else:
                fout.write(znak[0])
        fout.write("\n")
    print("euuuuuuuuuurekaaaaaaaaaaa!!!")
    fout.close()
    exit()


def no_solution():
    print("przegraliśmy :'(")
    exit()


def printtab(tab):
    for t in tab:
        for i in t:
            if i:
                print(znak[1], end="")
            else:
                print(znak[0], end="")
        print()
    print()


def printline(line):
    for i in line:
        if i:
            print(znak[1], end="")
        else:
            print(znak[0], end="")
    print()


########################################################################################################################
########################################################################################################################

def next_fit(t, length, fir, d):#
    n = len(d)-1
    if fir[n] + d[n] == length:
        n -= 1
        while n >= 0 and t[fir[n] + d[n] + 1]:
            n -= 1
        if n < 0:
            return True, t, fir
        t[fir[n]] = False
        t[fir[n] + d[n]] = True
        fir[n] += 1
        for i in range(n + 1, len(d)):
            fir[i] = fir[i-1] + d[i-1] + 1
            for j in range(fir[i], fir[i] + d[i]):
                t[j] = True
            t[fir[i] - 1] = False
            if fir[i] + d[i] < length:
                t[fir[i] + d[i]] = False
        for j in range(fir[len(d)-1] + d[len(d)-1], length):
            t[j] = False
    else:
        t[fir[n]] = False
        t[fir[n] + d[n]] = True
        fir[n] += 1
    return False, t, fir


def all_fits(d, length):# zwraca listę wszystkich możliwych ustawień dla danego wiersza/kolumny
    t = []
    fir = []
    for k in d:     # k = długość bloku
        fir.append(len(t))
        for i in range(k):
            t.append(True)
        t.append(False)
    t = t[:-1]
    if len(t) > length:
        return False
    for i in range(len(t), length):
        t.append(False)
    possibles = [t]
    possible_starts = [fir]
    while True:
        koniec, t, fir = next_fit(copy.deepcopy(t), length, copy.deepcopy(fir), d)
        if koniec:
            break
        possibles.append(t)
        possible_starts.append(fir)

    return possibles


def revise_one(possibles, length, fix1):
    if len(possibles) == 0:
        no_solution()
    elif len(possibles) == 1:
        fix1 = [True for _ in range(length)]
    else:
        for i in range(length):#Jeśli istnieje wiele możliwości, to dla każdej sprawdzamy, czy wszystkie możliwości mają ten sam piksel na danej pozycji
            if not fix1[i]:
                fix1[i] = True
                for p in possibles:
                    if p[i] != possibles[0][i]:
                        fix1[i] = False
                        break
    return fix1


def revise_two(a, b, wzor, dom, fix, length):# sprawdza, czy w dziedzinie b istnieje dopasowanie, które ma piksel a w odpowiednim ustawieniu
    revised = False
    k = []
    for p in dom[b]:
        if p[a] == wzor:
            k.append(p)
        else:
            revised = True
    dom[b] = k
    if revised:
        fix[b] = revise_one(dom[b], length, fix[b])
    if not fix[b][a]:
        print("dalej niedziałaaaaaaa!!!!!!!!!!")
        exit()
    return revised
    # wyrzuć z dziedziny wszystkie dopasowania, które nie mają danego piksela we właściwym ustawieniu
    # ustaw piksel jako fixed


def queue_init():
    que = queue.Queue()
    for r in range(height):
        for c in range(width):
            que.put((r, c, True))
            que.put((r, c, False))
    return que    # dodaj wszystkie piksele na kolejkę


def possibles_init(d, siz1, siz2):# dla każdego wiersza/kolumny znajdź wszystkie możliwe ustawienia
    pss = []
    for i in range(siz1):
        pss.append(all_fits(d[i], siz2))
    return pss


def fixed_init(pss, siz1, siz2):#
    fix = []
    for i in range(siz1):
        fix.append(revise_one(pss[i], siz2, [False for _ in range(siz2)]))
    return fix


def ac3():
    que = queue_init()    # (row, col, r/c)
    possibles_rows = possibles_init(dr, height, width)
    possibles_cols = possibles_init(dc, width, height)
    fixed_r = fixed_init(possibles_rows, height, width)
    fixed_c = fixed_init(possibles_cols, width, height)
    while not que.empty():
        x = que.get()   # (row, col, r/c)

        if x[2] and fixed_r[x[0]][x[1]]:  # and not fixed_c[x[1]][x[0]]:
            # print("row -> col", x)
            if revise_two(x[0], x[1], possibles_rows[x[0]][0][x[1]], possibles_cols, fixed_c, height):
                for i in range(height):
                    que.put((i, x[1], False))

        if (not x[2]) and fixed_c[x[1]][x[0]]:  # and not fixed_r[x[0]][x[1]]:
            # print("col -> row", x)
            if revise_two(x[1], x[0], possibles_cols[x[1]][0][x[0]], possibles_rows, fixed_r, width):
                for i in range(width):
                    que.put((x[0], i, True))

    for i in range(height):
        for j in range(width):
            if fixed_r[i][j] != fixed_c[j][i]:
                print("fixed się źle ustawiają", i, j)

    finish_check(possibles_rows)


def finish_check(possibles_rows):
    koniec = True
    for r in possibles_rows:
        if len(r) > 1:
            koniec = False
            break
    if koniec:
        t = []
        for r in possibles_rows:
            t.append(r[0])
        write_output(t)

########################################################################################################################


global width, height, dr, dc
znak = (".", "#")

read_input()
ac3()
print("przegraliśmy :'(")
