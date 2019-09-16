import matplotlib.pyplot as plt
import numpy as np


def initialize(mN1, mN2):
    global N1,N2
    global N1s, N2s
    N1 = mN1
    N2 = mN2
    N1s = [N1]
    N2s = [N2]
    pass
def observe():
    global N1s, N2s
    N1s.append(N1)
    N2s.append(N2)
    pass
def update():
    global N1,N2
    N1_dot = r1 * N1 * (K1-N1-a21*N2) /K1
    N2_dot = r2 * N2 * (K2-N2-a12*N1) /K2
    N1 += N1_dot
    N2 += N2_dot
    pass
def reduce():
    global N1,N2
    #N1 = N1 * (1-p)
    N2 = N2 * (1-p)
    
K1 = 100
K2 = 200
a12 = 1.0
a21 = 0.5
r1 = 0.03
r2 = 0.05

h = 1
#ps = [0.01, 0.12, 0.5]
#p = 0.12
#p = ps[1]
N1_set = [20,100,200]
N2_set = [10,50,300,500]
ps = [0, 0.005, 0.008,0.009, 0.01, 0.011, 0.012, 0.013, 0.015, 0.04]

iN1 = 50
plt.figure(figsize=[16,16])
l1 = []
l2 = []
for i, ip in enumerate(ps):
    p = ip
    for j, iN2 in enumerate(N2_set):
        plt.subplot(len(ps),len(N2_set), len(N2_set)*i+j+1)
        initialize(iN1, iN2)
        observe()
        h0 = h
        for k in range(1000):
            h0 -= 1
            if h0==0:
                reduce()
                h0 = h
            update()
            observe()
        plt.scatter(N1s[0],N2s[0], color='black')
        plt.scatter(N1s, N2s, s=0.1)
        plt.scatter(N1s[-1],N2s[-1], color='red')
        #plt.plot([0, K2/a12], [K2,0], linewidth=0.2, color='#aaaa00' ) #dot N2=0, yellow
        plt.plot([K1,0], [0,K1/a21], linewidth=0.2, color='#aa00aa') #dot N1=0, pink
        #x1 = 0, y1 = (1-p/r2)*K2/a12
        #x2 = (1-p/r2)*K2, y2 = 0
        plt.plot([0,(1-p/r2)*K2], [(1-p/r2)*K2/a12,0], linewidth=0.2, color="#aa0000") #red 
        #final point: N1s[-1],N2s[-1]
        #a12
        b = N2s[-1] + a12*N1s[-1]
        plt.title("p=%.3f, N2=%d, y-axis=%.f"%(p,iN2,b))
        l1.append(p)
        l2.append(b)
        #plt.plot([0,a1],[a2,0], linewidth=0.5, color='#aaaa00')
        plt.ylim(0,350)
        plt.xlim(0,250)
        

plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.4, hspace=0.5)

plt.show()