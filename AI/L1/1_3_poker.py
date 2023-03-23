import random


def kareta(hand):
    hand.sort()
    counter = 1
    for i in range(1, 5):
        if hand[i][0] == hand[i - 1][0]:
            counter += 1
        elif counter < 4:
            counter = 1
        else:
            return True
    if counter == 4:
        return True
    else:
        return False


def strit(hand):
    hand.sort()
    for i in range(1, 5):
        if int(hand[i][0]) != int(hand[i - 1][0]) + 1:
            return False
    return True


def kolor(hand):
    for i in range(1, 5):
        if hand[i][1] != hand[i - 1][1]:
            return False
    return True


def trzy(hand):
    hand.sort()
    counter = 1
    for i in range(1, 5):
        if hand[i][0] == hand[i - 1][0]:
            counter += 1
        elif counter < 3:
            counter = 1
        else:
            return True
    if counter >= 3:
        return True
    else:
        return False


def full(hand):
    hand.sort()
    counter = 1
    for i in range(1, 5):
        if hand[i][0] == hand[i - 1][0]:
            counter += 1
        elif counter < 2:
            return False
        else:
            counter = 1
    if counter < 2:
        return False
    else:
        return True


def dwiepary(hand):
    hand.sort()
    counter = 1
    sing = 0
    for i in range(1, 5):
        if hand[i][0] == hand[i - 1][0]:
            counter += 1
        elif counter < 2:
            counter = 1
            sing += 1
        else:
            counter = 1
    if sing <= 1:
        return True
    else:
        return False


def poker(hand):
    if strit(hand) and kolor(hand):
        return True
    else:
        return False


def blot_win(blot, fig):
    if kareta(fig):
        if poker(blot):
            return True
        else:
            return False
    elif full(fig):
        if poker(blot) or kareta(blot):
            return True
        else:
            return False
    elif trzy(fig):
        if strit(blot) or kolor(blot) or full(blot) or kareta(blot):
            return True
        else:
            return False
    elif dwiepary(fig):
        if trzy(blot) or strit(blot) or kolor(blot):
            return True
        else:
            return False
    else:
        if dwiepary(blot) or trzy(blot) or strit(blot) or kolor(blot):
            return True
        else:
            return False


def gra(blotki, figury):
    n = 100000
    b = 0
    for i in range(n):
        #random.shuffle(blotki)
        #blotkarz = blotki[:5]
        #random.shuffle(figury)
        #figurant = figury[:5]
        blotkarz = random.sample(blotki, 5)
        figurant = random.sample(figury, 5)
        if blot_win(blotkarz, figurant):
            b += 1
    pstwo = b / n
    print(pstwo)


talia_figuranta = [('A', 'kier'), ('A', 'karo'), ('A', 'trefl'), ('A', 'pik'),
          ('K', 'kier'), ('K', 'karo'), ('K', 'trefl'), ('K', 'pik'),
          ('Q', 'kier'), ('Q', 'karo'), ('Q', 'trefl'), ('Q', 'pik'),
          ('J', 'kier'), ('J', 'karo'), ('J', 'trefl'), ('J', 'pik')]
talia_blotkarza = [('2', 'kier'), ('2', 'karo'), ('2', 'trefl'), ('2', 'pik'),
          ('3', 'kier'), ('3', 'karo'), ('3', 'trefl'), ('3', 'pik'),
          ('4', 'kier'), ('4', 'karo'), ('4', 'trefl'), ('4', 'pik'),
          ('5', 'kier'), ('5', 'karo'), ('5', 'trefl'), ('5', 'pik'),
          ('6', 'kier'), ('6', 'karo'), ('6', 'trefl'), ('6', 'pik'),
          ('7', 'kier'), ('7', 'karo'), ('7', 'trefl'), ('7', 'pik'),
          ('8', 'kier'), ('8', 'karo'), ('8', 'trefl'), ('8', 'pik'),
          ('9', 'kier'), ('9', 'karo'), ('9', 'trefl'), ('9', 'pik'),
          ('10', 'kier'), ('10', 'karo'), ('10', 'trefl'), ('10', 'pik')]
P0 = 0.082367  # około 8% zawsze wychodzi
gra(talia_blotkarza, talia_figuranta)
B1 = [('7', 'kier'), ('7', 'karo'), ('7', 'trefl'), ('7', 'pik'),
      ('8', 'kier'), ('8', 'karo'), ('8', 'trefl'), ('8', 'pik'),
      ('9', 'kier'), ('9', 'karo'), ('9', 'trefl'), ('9', 'pik')]
B2 = [('2', 'kier'),
      ('3', 'kier'),
      ('4', 'kier'),
      ('5', 'kier'),
      ('6', 'kier'),
      ('7', 'kier'),
      ('8', 'kier'),
      ('9', 'kier'),
      ('10', 'kier'),
      ('2', 'karo')]
gra(B1, talia_figuranta)
gra(B2, talia_figuranta)


