import time
import random
import matplotlib.pyplot as plt

maxVal = 10
nVal = 10
listeNombres = random.choices(range(maxVal),k=nVal)

def triSelection(L: list)-> list:
    for i in range(len(L)-1):
 #       print(L)
        indiceMini = i
        for j in range(i, len(L)):
            if L[j] < L[indiceMini]:
                indiceMini = j
#        L[i], L[indiceMini] = L[indiceMini], L[i]
        temp = L[i]
        L[i] = L[indiceMini]
        L[indiceMini] = temp
    return L

#Tri bulle je crois
def triBulle(L: list)-> list:
    for i in range(len(L)):
        pivot = i
        for j in range(len(L)):
            print(L)
            if L[j] > L[pivot]:
                L[j], L[pivot] = L[pivot], L[j]
    return L

def triInsertion(L: list):
    for i in range(1, len(L)):
        tmpval = L[i]
        j = i - 1
        while j >= 0 and tmpval < L[j]:
            L[j+1] = L[j]
            j -= 1
        L[j+1] = tmpval
    return L

def trifusion(L: list):
    if L == []:
        return []
    initlist = L
    temp = []
    if len(L)%2 != 0:
        L.append(0)
    for i in range(len(L)):
        temp.append([L[i]])
    L = temp
#    print(initlist)
    while len(L[0]) != len(initlist):
        temp = []
        if len(L)%2 != 0:
            L.append([])
        for i in range(0, len(L), 2):
#            print("-----------------------------------------------------------")
#            print("temp: ", temp)
#            print("L: ", L)
#            print("i", i)
            subdiv = []
            while L[i] != [] and L[i+1] != []:
                if L[i][0] < L[i+1][0]:
                    subdiv.append(L[i].pop(0))
                else:
                    subdiv.append(L[i+1].pop(0))
            if L[i] != []:
                for j in range(len(L[i])):
                    subdiv.append(L[i][j])
            elif L[i+1] != []:
                for j in range(len(L[i+1])):
                    subdiv.append(L[i+1][j])
            temp.append(subdiv)
        L = temp
    return L

def comparaisontemps():
    tpssel = []
    tpsins = []
    tpsins2 = []
    nelements = []
    for i in range(0, 10000, 100):
        nelements.append(i)
        print(i)
        liste1 = random.choices(range(100000),k=i)
        liste2 = random.choices(range(100000),k=i)
        liste3 = random.choices(range(100000),k=i)
#        liste1 = [j for j in range(i, 0, -1)]
#        liste2 = [j for j in range(i, 0, -1)]
#        liste3 = [j for j in range(i, 0, -1)]
        tps  = time.time()
        triSelection(liste1)
        tpssel.append(time.time()-tps)
        tps = time.time()
        trifusion(liste2)
        tpsins.append(time.time()-tps)
        tps = time.time()
        triInsertion(liste3)
        tpsins2.append(time.time()-tps)
    plt.plot(tpssel, label="Selection")
    plt.plot(tpsins, label="Fusion")
    plt.plot(tpsins2, label="Insertion")
    plt.legend()
    plt.show()

#listeNombresTriee = trifusion(listeNombres) # trie la liste
comparaisontemps()
#print(listeNombresTriee) # affiche la liste
