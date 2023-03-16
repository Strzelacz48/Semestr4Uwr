'''
starting_table = input()
D = int(input())
print("starting_table :",starting_table,"D :",D)
maxmoves = D
ones = 0
p = 0
q = len(starting_table) - 1
next1 = 1
prev1 = 1
while(starting_table[p] != '1'):
    p += 1

while(starting_table[q] != '1'):
    q -= 1
print("p :",p,"q :",q)
while(p < q and q - p > D):
    ones += 1
    next1 = 1
    print("1.ones :",ones,"p :",p,"q :",q,"next1 :",next1,"prev1 :",prev1)
    while(starting_table[p + next1] != '1'):
        next1 += 1
    prev1 = 1
    print("2.ones :",ones,"p :",p,"q :",q,"next1 :",next1,"prev1 :",prev1)
    while(starting_table[q - prev1] != '1'):
        prev1 += 1
    print("3. ones :",ones,"p :",p,"q :",q,"next1 :",next1,"prev1 :",prev1)
    if(next1 < prev1):
        next1 = 0
    else:
        prev1 = 0
    print("ones :",ones,"p :",p,"q :",q,"next1 :",next1,"prev1 :",prev1)
    q = q - prev1
    p = p + next1
#Problem z 
wynik = ones
for i in range(p,q):
    if(starting_table[i] == '0'):
        wynik += 1


print("ones :",ones,"pp :",p,"pq :",q,"next1 :",next1,"prev1 :",prev1)

started = False
    for i in range(len(table)):
        if(table[i] == '1' and not(started) and D > 0):
            started = True
            D -= 1
        elif(started):
            if(D > 0 and table[i] != '1'):
                return False
            elif(table[i] == '1'):
                D -= 1
    if(D == 0):
        return True
    return False
'''

#DFS zaczynamy w korzeniu z oryginalnym wejściem potem w lewo nie zmieniamy bitu nr na którym poziomie jesteśmy
#a w prawo zmieniamy ten bit. Jeżeli znajdziemy jakieś rozwiązanie z przesuniętym 2^n - 1 to sprawdzamy jak głęboko jesteśmy
#jak przejdziemy wszystko to znajdziemy najmiejszy.
def f(table, D):
    it = 0
    ones = 0
    while(D > 0 and it < len(table) and table[it]!= '1' ):
        it += 1

    while(D > ones and it < len(table) and table[it] == '1'):
        ones += 1
        it += 1
    
    while(it < len(table)):
        if(table[it] == '1'):
            return False
        it += 1
    if(D == ones):
        return True
    return False

def changebit(table, which):
    #print(" before table :",table,"which :",which)
    newtable = table.copy()
    if(table[which] == '0'):
        newtable[which] = '1'
    else:
        newtable[which] = '0'
    #print("after table :",table,"which :",which)
    return newtable

def DFS(table, D, which_bit, changed_bits, max_bit):
    #print("table :",table,"which_bit :",which_bit,"changed_bits :",changed_bits,"max_bit :",max_bit)
    if(f(table, D)):
        #print("table spelnia warunek :",table,"which_bit :",which_bit,"changed_bits :",changed_bits,"max_bit :",max_bit)
        return changed_bits
    if(which_bit == max_bit):
        return max_bit
    #print("DFS(l) :",table, D, which_bit + 1, changed_bits, max_bit,"DFS(p) :",changebit(table, which_bit), D, which_bit + 1, changed_bits + 1, max_bit)
    return min(DFS(table, D, which_bit + 1, changed_bits, max_bit), DFS(changebit(table, which_bit), D, which_bit + 1, changed_bits + 1, max_bit))

starting_table = list(input())
D = int(input())
#print("starting_table :",starting_table,"D :",D)
print(DFS(starting_table, D, -1, 0, len(starting_table)))

#0010001000