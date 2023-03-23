dict = open("words_for_ai1.txt", 'r', encoding="utf-8")
words = dict.readlines()
words.sort()#alfabetycznie

def istnieje(word):
    a = 0
    b = len(words)
    word = word + "\n"
    while b > a + 1:
        s = (a + b) // 2
        # print(words[s])

        if words[s] > word:
            b = s
        elif words[s] < word:
            a = s
        else:
            return True
    if words[a] == word:
        return True
    else:
        return False


def find_opt(possibles, line):
    dp = []
    word = []
    for i in range(len(line)+1):
        dp.append(0)
        word.append("")

    for a in range(len(line)-1, -1, -1):
        for w in possibles[a]:
            if (a+len(w) == len(line) or (a+len(w) < len(line) and dp[a+len(w)] > 0)) and dp[a] < len(w)*len(w) + dp[a+len(w)]:
                dp[a] = len(w)*len(w) + dp[a+len(w)]
                word[a] = w

    a = 0
    result = ""
    while a < len(line)-1:
        result += word[a] + " "
        a += len(word[a])
        #print(result)

    return result



def find(possibles, line, result):
    return "result"


def split(line):
    len_max = min(31, len(line))
    possibles = []
    for i in range(len(line)):
        possibles.append([])
    starters = {0}
    for a in range(len(line)):
        if a not in starters:
            continue
        for b in range(a + 1, len(line)+1):
            if b - a > len_max:
                break
            elif istnieje(line[a:b]):
                possibles[a].append(line[a:b])
                starters.add(b)
    #print(possibles)
    return find_opt(possibles, line)


# fin = open("pan_tadeusz_bez_spacji.txt", 'r', encoding="utf-8")
# fout = open("pan_tadeusz_ze_spacjami.txt", 'w', encoding="utf-8")
fin = open("zad2_input.txt", 'r', encoding="utf-8")
fout = open("zad2_output.txt", 'w', encoding="utf-8")

line = " "
#ile = 0
while line:
#for num in range(993):
    line = fin.readline()[:-1]
    line_out = split(line)[:-1] + '\n'
    fout.write(line_out)
    #ile+=1
    #print(ile)

fin.close()
fout.close()
dict.close()




