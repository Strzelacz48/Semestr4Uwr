S = ["ala","kot","siedem","czerwony"]
def sortS(S):
    for j in range(len(S)-1):
        for i in range(len(S) - j-1):
            if(len(S[i]) < len(S[i+1])):
                pom = S[i+1]
                S[i+1] = S[i]
                S[i] = pom
    return S
print(sortS(S))
a = tuple([2,3])
print(a[1])
#no_space_text = input()
#for i in S:
#   for j in range(S[i].length()):
