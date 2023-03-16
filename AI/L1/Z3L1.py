import random 
#K - kier, k - karo, T - trefl, P - pik
#11 - walet, #12 - dama, #13 - król #14 - as
talia_blotkarza = ["K02", "k02", "T02", "P02", "K03", "k03", "T03", "P03","K04", "k04", "T04", "P04", "K05", "k05", "T05", "P05",
                    "K06", "k06", "T06", "P06", "K07", "k07", "T07", "P07", "K08", "k08", "T08", "P08", "K09", "k09", "T09", "P09",
                      "K10", "k10", "T10", "P10"]
talia_figuranta = ["K11", "k11", "T11", "P11", "K12", "k12", "T12", "P12", "K13", "k13", "T13", "P13", "K14", "k14", "T14", "P14"]

def reka(talia):
    for i in range(0,5):
        los = random.randrange(i,len(talia))
        pom = talia[i]
        talia[i] = talia[los]
        talia[los] = pom
    return talia[0:5]
#Wysoka karta = wygrywa figurant zawsze
def para(reka):
    counted = [0,0,0,0,0]
    liczba_par = 0
    for i in range(0, len(reka) - 1):
        for j in range(i + 1, len(reka)):
            if(counted[i] == counted[j] == 0 and reka[j][1] == reka[i][1] and reka[j][2] == reka[i][2]):#same numery trzeba dodać kolory
                liczba_par += 1
                counted[i] = counted[j] = 1
                i += 1
    return liczba_par
#dwie pary
def trojka(reka):
    for i in range(0, len(reka) - 2):
        for j in range(i + 1, len(reka) - 1):
            for k in range(j+1, len(reka)):
                if(reka[j][1] == reka[i][1] and reka[j][2] == reka[i][2] and reka[k][1] == reka[i][1] and reka[k][2] == reka[i][2]):#same numery trzeba dodać kolory
                    return 1
    return 0
#strit pięć kart po sobie w kolejności od najmniejszej do największej
def strit(reka):
    for i in range(len(reka)):
        has_neighbors = False
        for j in range(len(reka)):
            if(j != i):
                neighbor = int(reka[j - 1][1] + reka[j - 1][2])
                if(neighbor == int(reka[i][1] + reka[i][2]) + 1 or neighbor == int(reka[i][1] + reka[i][2]) - 1):
                    has_neighbors = True
                    break
        if(not has_neighbors):
            return False
    return True

def kolor(reka):
    for i in range(len(reka) - 1):
        if(reka[i][0] != reka[i + 1][0]):
                return False
    return True

#Full - trójka i para
def full(reka):
    if(trojka(reka) and para(reka)):
        return True
    return False
#def kareta(reka): 4 te same karty 
def kareta(reka):
    if(para(reka) == 2):
        return True
    return False
"""
    for i in range(len(reka) ):
        is_four = 0
        for j in range(len(reka)):
            if(j != i):
                if(reka[i][1] + reka[i][2] == reka[j][1] + reka[j][2]):
                    is_four += 1
        if(is_four == 3):
            return True
    return False
"""

def poker(reka):
    if(strit and kolor):
        return True
    return False

'''
cards = {2,3,4,5,6,7,8,9,10,11,12,13,14}#11 - walet, #12 - dama, #13 - król #14 - as
print(cards)
print(talia_blotkarza)
pierwsza_reka = reka(talia_blotkarza)
print(pierwsza_reka)
for i in range(0,5):
    print(pierwsza_reka[i][0]," ",pierwsza_reka[i][1],pierwsza_reka[i][2])

test_reka = ["K01", "k03", "P01", "T01", "K01"]

print("liczba par : ",para(pierwsza_reka))
print("liczba par : ",para(test_reka))
print("liczba trojek : ",trojka(pierwsza_reka))
print("liczba trojek : ",trojka(test_reka))
print("czy strit : ",strit(pierwsza_reka))
print("czy strit : ",strit(test_reka))
print("czy kolor : ",kolor(pierwsza_reka))
print("czy kolor : ",kolor(test_reka))
print("czy kareta : ",kareta(pierwsza_reka))
print("czy kareta : ",kareta(test_reka))
'''
#milion gier albo miliard wygrane blotkarza/ ilosc wszystkich gier
#bierzemy talie blotkarza i puszczamy mu np 1000 talii figuranta liczymy z tego % wygranych i tak dla powiedmy miliona talii blotkarza
#potem bierzemy najwyższy procent blotkarza i jego talii co później zwracamy. 
BLOTNR = 10000
FIGNR = 10000 # dla 1000 000 trwa 16 h sprawdzanie ok
wynik = 0
for i in range(BLOTNR):
    blotkarz = reka(talia_blotkarza)
    blotkarz_wygrane = 0
    print("i : ",i)
    for j in range(FIGNR):
        figurant = reka(talia_figuranta)
        print("i : ",i,"j : ",j)
        if(poker(blotkarz) and not(poker(figurant))):
            blotkarz_wygrane += 1
            continue
        elif(poker(figurant)):
            continue

        if(kareta(blotkarz) and not(kareta(figurant))):
            blotkarz_wygrane += 1
            continue
        elif(kareta(figurant)):
            continue

        if(full(blotkarz) and not(full(figurant))):
            blotkarz_wygrane += 1
            continue
        elif(full(figurant)):
            continue
        
        if(kolor(blotkarz) and not(kolor(figurant))):
            blotkarz_wygrane += 1
            continue
        elif(kolor(figurant)):
            continue

        if(strit(blotkarz) and not(strit(figurant))):
            blotkarz_wygrane += 1
            continue
        elif(strit(figurant)):
            continue
        
        if(trojka(blotkarz) and not(trojka(figurant))):
            blotkarz_wygrane += 1
            continue
        elif(trojka(figurant)):
            continue

        if(para(blotkarz) > para(figurant)):
            blotkarz_wygrane += 1
            continue
        elif(para(blotkarz) <= para(figurant)):
            continue
    wynik += blotkarz_wygrane/FIGNR
wynik /= BLOTNR/100 # wynik /1 000 / 1 000 000 000 * 100% = procent wygranych blotkarza minus trzy zera 000 potem sie doda je z powrtoem
print("Wynik: ",wynik,"%")
#print("Blotkarz: ",blotkarz)
#print("Figurant: ",figurant)