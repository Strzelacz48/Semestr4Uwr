import queue

########################################################################################################################
# ZAD 2 Z PRAC 3
########################################################################################################################


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
    print("wygraliśmy :)")
    fout.close()
    exit()


def no_solution():
    print("przegraliśmy :(")
    fout = open("zad_output.txt", 'w')
    fout.write("przegraliśmy :(")
    fout.close()
    exit()


def printtab(tab):
    for t in tab:
        for i in t:
            if i == "?":
                print(" ", end="")
            elif i:
                print(znak[1], end="")
            else:
                print(znak[0], end="")
        print()
    print()


def printrow(r):
    for x in r:
        if x:
            print(znak[1], end="")
        else:
            print(znak[0], end="")
    print()


def my_deepcopy(x):
    if type(x) == list:
        newx = []
        for elem in x:
            newx.append(my_deepcopy(elem))
        return newx
    else:
        return x


########################################################################################################################
# AC3
########################################################################################################################


def next_fit(t, length, fir, d):
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


def all_fits(d, length):
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
        koniec, t, fir = next_fit(my_deepcopy(t), length, my_deepcopy(fir), d)
        if koniec:
            break
        possibles.append(t)
        possible_starts.append(fir)

    return possibles


def revise_one(possibles, length, fix1):
    if len(possibles) == 0:
        return fix1, False
    elif len(possibles) == 1:
        fix1 = [True for _ in range(length)]
    else:
        for i in range(length):
            if not fix1[i]:
                fix1[i] = True
                for p in possibles:
                    if p[i] != possibles[0][i]:
                        fix1[i] = False
                        break
    return fix1, True


def revise_two(a, b, wzor, dom, fix, length):
    revised, ok = False, True
    k = []
    for p in dom[b]:
        if p[a] == wzor:
            k.append(p)
        else:
            revised = True
    dom[b] = k
    if revised:
        fix[b], ok = revise_one(dom[b], length, fix[b])
    return revised, ok


def queue_init():
    que = queue.Queue()
    for r in range(height):
        for c in range(width):
            que.put((r, c, True))
            que.put((r, c, False))
    return que


def possibles_init(d, siz1, siz2):
    pss = []
    for i in range(siz1):
        pss.append(all_fits(d[i], siz2))
    return pss


def fixed_init(pss, siz1, siz2):
    fix = []
    ok = True
    for i in range(siz1):
        f, ok = revise_one(pss[i], siz2, [False for _ in range(siz2)])
        fix.append(f)
    return fix, ok


def ac3_init():
    que = queue_init()  # (row, col, r/c)
    possibles_rows = possibles_init(dr, height, width)
    possibles_cols = possibles_init(dc, width, height)
    fixed_r, ok = fixed_init(possibles_rows, height, width)
    fixed_c, ok = fixed_init(possibles_cols, width, height)
    assignment = [["?" for _ in range(width)] for _ in range(height)]
    return ac3(que, possibles_rows, possibles_cols, fixed_r, fixed_c, assignment)


def ac3(que, possibles_rows, possibles_cols, fixed_r, fixed_c, assignment):
    while not que.empty():
        x = que.get()   # (row, col, r/c)

        if x[2] and fixed_r[x[0]][x[1]]:  # and not fixed_c[x[1]][x[0]]:
            if assignment[x[0]][x[1]] not in (possibles_rows[x[0]][0][x[1]], "?"):
                print("oo nie...")
                exit()
            if assignment[x[0]][x[1]] == "?":
                assignment[x[0]][x[1]] = possibles_rows[x[0]][0][x[1]]
            rev, ok = revise_two(x[0], x[1], assignment[x[0]][x[1]], possibles_cols, fixed_c, height)
            if not ok:
                return possibles_rows, possibles_cols, assignment, False
            if rev:
                for i in range(height):
                    que.put((i, x[1], False))

        if (not x[2]) and fixed_c[x[1]][x[0]]:  # and not fixed_r[x[0]][x[1]]:
            if assignment[x[0]][x[1]] not in (possibles_cols[x[1]][0][x[0]], "?"):
                print("oo nie...")
                exit()
            if assignment[x[0]][x[1]] == "?":
                assignment[x[0]][x[1]] = possibles_cols[x[1]][0][x[0]]
            rev, ok = revise_two(x[1], x[0], assignment[x[0]][x[1]], possibles_rows, fixed_r, width)
            if not ok:
                return possibles_rows, possibles_cols, assignment, False
            if rev:
                for i in range(width):
                    que.put((x[0], i, True))

    finish_check(possibles_rows)
    return possibles_rows, possibles_cols, assignment, True


def finish_check(possibles_rows):
    koniec = True
    for r in possibles_rows:
        if len(r) != 1:
            koniec = False
            break
    if koniec:
        t = []
        for r in possibles_rows:
            t.append(r[0])
        write_output(t)


########################################################################################################################
# BACKTRACKING
########################################################################################################################


def ac3_init_bctr(assignment, p_rows, p_cols, row, col, ins):
    que = queue.Queue()  # (row, col, r/c)
    for r in range(height):
        for c in range(width):
            if assignment[r][c] == "?":
                que.put((r, c, True))
                que.put((r, c, False))

    to_rm = []
    for p in p_rows[row]:
        if p[col] != ins:
            to_rm.append(p)
    for p in to_rm:
        p_rows[row].remove(p)
    to_rm = []
    for p in p_cols[col]:
        if p[row] != ins:
            to_rm.append(p)
    for p in to_rm:
        p_cols[col].remove(p)

    if not p_rows[row] or not p_cols[col]:
        return p_rows, p_cols, [], False

    fixed_r, ok = fixed_init(p_rows, height, width)
    fixed_c, ok = fixed_init(p_cols, width, height)
    for r in range(height):
        for c in range(width):
            if assignment[r][c] != "?":
                fixed_r[r][c] = True
                fixed_c[c][r] = True

    return ac3(que, p_rows, p_cols, fixed_r, fixed_c, assignment)


def backtracking(assignment, p_rows, p_cols, row, col):
    if row == height or col == width:
        return assignment

    cc, rr = col, row
    if col < width - 1:
        cc += 1
    else:
        rr += 1
        cc = 0

    if assignment[row][col] != "?":
        return backtracking(assignment, p_rows, p_cols, rr, cc)

    for color in (True, False):
        a2 = my_deepcopy(assignment)
        pr2 = my_deepcopy(p_rows)
        pc2 = my_deepcopy(p_cols)
        pr2, pc2, a2, ok = ac3_init_bctr(a2, pr2, pc2, row, col, color)
        if ok:
            result = backtracking(a2, pr2, pc2, rr, cc)
            if result:
                return result

    return []


########################################################################################################################

########################################################################################################################


global width, height, dr, dc
znak = (".", "#")

read_input()

possibl_rows, possibl_cols, res, b = ac3_init()
if not b:
    no_solution()

res = backtracking(res, possibl_rows, possibl_cols, 0, 0)
if res:
    write_output(res)
no_solution()