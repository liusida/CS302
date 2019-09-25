import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
import random
import time

import matplotlib
print(matplotlib.__version__)

from matplotlib import pyplot as plt
from matplotlib import animation


class RegrMagic(object):
    """Mock for function Regr_magic()
    """
    def __init__(self):
        self.x = 0
    def __call__(self):
        time.sleep(random.random())
        self.x += 1
        return self.x, random.random()

regr_magic = RegrMagic()

def frames():
    while True:
        yield regr_magic()

fig = plt.figure(figsize=(16, 14))
grid = plt.GridSpec(4, 4, hspace=0.2, wspace=0.2)
main_ax = fig.add_subplot(grid[:, 1:])
info_ax = []
for i in range(4):
    info_ax.append(fig.add_subplot(grid[i, 0]))

x = []
y = []
def animate(args):
    x.append(args[0])
    y.append(args[1])
    return info_ax[0].plot(x, y, color='g')


anim = animation.FuncAnimation(fig, animate, frames=frames, interval=1000)
plt.show()
