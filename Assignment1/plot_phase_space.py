#from pylab import *
import numpy as np
import matplotlib.pyplot as plt

xvalues, yvalues = np.meshgrid(np.arange(0,3,0.1), np.arange(0,3,0.1))
xdot = xvalues - xvalues * yvalues
ydot = -yvalues + xvalues * yvalues
plt.streamplot(xvalues, yvalues, xdot, ydot)
plt.show()