import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from mpl_toolkits.mplot3d import Axes3D

rho = 28.0
sigma = 10.0
beta = 8.0 / 3.0

def f(t,state):
  x, y, z = state  # unpack the state vector
  dxdt = sigma * (y - x)
  dydt = x * (rho - z) - y
  dzdt = x * y - beta * z
  return [dxdt, dydt, dzdt]

state0 = [1.0, 1.0, 1.0]

sol = solve_ivp(f, [0,40], state0, max_step=0.01)
plt.plot(sol.t, sol.y[0,:])
plt.show()
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(sol.y[0], sol.y[1], sol.y[2])
plt.show()