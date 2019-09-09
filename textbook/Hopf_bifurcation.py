# Code 8.2 in Textbook
# by Sayama
# draw phase space of systems whose eigenvalue of Jacobian Matrix at equilibrium point is pure imaginary
# System:
# dx/dt = y
# dy/dt = -r * (x^2-1) * y -x
# where r is the parameter of the system
# Simulation via Euler's method:
# x_next = x + dx/dt * h
# y_next = y + dy/dt * h
from pylab import *

Dt = 0.01

# set initial condition, save the first state variables into lists
def initialize():
    global x, xresult, y, yresult
    x = y = 0.1
    xresult = [x]
    yresult = [y]

# save current state variables into lists
def observe():
    global x, xresult, y, yresult
    xresult.append(x)
    yresult.append(y)

# calculate state variables at next step via Euler's method
def update():
    global x, xresult, y, yresult
    nextx = x + y * Dt
    nexty = y + (-r * (x**2 -1) * y - x ) * Dt
    x = nextx
    y = nexty

# do simulation and plot to current axis
def plot_phase_space():
    initialize()
    for t in range(10000):
        update()
        observe()

    plot(xresult, yresult)
    axis('image')
    axis([-3,3,-3,3])
    title('r='+str(r))

# main code, give different parameters, set target subplots, and run
rs = [-1, -0.1, 0, 0.1, 1]
for i in range(len(rs)):
    subplot(1, len(rs), i+1)
    r = rs[i]
    plot_phase_space()
show()