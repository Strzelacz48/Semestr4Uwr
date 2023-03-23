def opt_dist(arr, dl):
    pref = 0
    suf = 0
    inn = 0
    for i in range(dl):
        if arr[i] == '0':
            inn += 1
    for i in range(dl, len(arr)):
        if arr[i] == '1':
            suf += 1
    x = pref + inn + suf
    a = 1
    b = dl
    while b < len(arr):
        if arr[a - 1] == '1':
            pref += 1
        else:  # arr[a-1] == znak[0]
            inn -= 1
        if arr[b] == '1':
            suf -= 1
        else:  # arr[b] == znak[0]
            inn += 1
        x = min(x, pref + suf + inn)
        a += 1
        b += 1
    return x


fin = open("zad4_input.txt", 'r')
fout = open("zad4_output.txt", 'w')
k = " "
arr = ""
while k:
    k = fin.read(1)
    if k == ' ':
        dl = int(fin.read(1))
        fout.write(str(opt_dist(arr, dl)) + "\n")
    elif k == '\n':
        arr = ""
    elif k == '1' or k == '0':
        arr += k
fin.close()
fout.close()

#print(opt_dist("0010001000", 5)) #powinna zwrócić 3
#print(opt_dist("0010001000", 4))
#print(opt_dist("0010001000", 3))
#print(opt_dist("0010001000", 2))
#print(opt_dist("0010001000", 1))
#print(opt_dist("0010001000", 0))


