import time
import random
import matplotlib.pyplot as plt

maxVal = 1000
nVal = 10000
listeNombres = [i for i in range(10000, 0, -1)]
#random.choices(range(maxVal),k=nVal)

xdata = [i for i in range(nVal)]

ydata = listeNombres
plt.ion()
fig = plt.figure()
axes = fig.add_subplot(111)
l, = axes.plot(xdata, ydata)

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
        Li = []
        for i in range(len(L)):
            for j in range(len(L[i])):
                Li.append(L[i][j])
        ydata = Li
        l.set_ydata(ydata)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(1)
    time.sleep(5)
    return L

def triInsertion2(L: list):
    for i in range(1, len(L)):
        tmpval = L[i]
        j = i - 1
        while j >= 0 and tmpval < L[j]:
            L[j+1] = L[j]
            j -= 1
        ydata = L
        l.set_ydata(ydata)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.01)
        L[j+1] = tmpval
    time.sleep(5)
    return L

print(trifusion(listeNombres))

"""            Lis = []
            for i in range(len(temp)):
                for j in range(len(temp[i])):
                    Lis.append(temp[i][j])
            toto = []
            for i in range(len(L)):
                for j in range(len(L[i])):
                    toto.append(L[i][j])
            for i in range(len(Lis)):
                toto[i] = Lis[i]
            print(toto)
            ydata = Lis
            l.set_ydata(ydata)
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(1)
"""