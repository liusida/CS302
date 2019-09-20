import matplotlib.pyplot as plt
import numpy as np

h = 0.1
N1 = 1.
N2 = 1.
N1_dot = 0.
N2_dot = 0.
K1 = 120.
K2 = 160.
a21 = 0.3
a12 = 0.8
r1 = 0.2
r2 = 0.4


def continuous_function(N1,N2):
    N1_dot = r1*N1*(K1-N1-a12*N2)/K1
    N2_dot = r2*N2*(K2-N2-a21*N1)/K2
    return np.array([N1_dot,N2_dot])

xlim = 300
ylim = 300
stepsize = 10
plt.figure(figsize=[9,9])
plt.xlim(-10,xlim)
plt.ylim(-10,ylim)
for N1 in range(0,xlim,stepsize):
    for N2 in range(0,ylim,stepsize):
        dots = continuous_function(N1,N2)
        length = dots.T.dot(dots)
        dots = dots / length
        # print(dots[0],dots[1])
        if length>0:
            plt.arrow(N1,N2, dots[0],dots[1], head_width=1, head_length=3, fc='k', ec='k')
        else:
            plt.scatter(N1,N2, s=1, color='black')

plt.plot([K2/a21,0],[0,K2],label='isocline N2')
plt.plot([0,K1],[K1/a12,0],label='isocline N1')
plt.legend()
plt.show()