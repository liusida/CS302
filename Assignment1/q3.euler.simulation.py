# Question 3
# Implementation of Euler's forward method
# for simulating continuous one-species model
# Let's do a logistic growth model for example.
# If we want to switch to other models, just change the N_dot function to define new dN/dt

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Get dN/dt from N
# This is the definition of the original continuous function for both Euler's and Heun's methods.
# Here, we implement the logistic growth.
def N_dot(N, growth_ratio, capacity):
    return growth_ratio * N * (capacity-N) /capacity

# Euler forward method is:
# N( t + delta_t ) = N(t) + r * N(t) * (K-N) /K * delta_t
# One step is delta_t time unit: delta_t is the step size.
# parameters:
# h:                in second, time per step
# growth_ratio:     how quick number grows 
# capacity:         maximum number of animals
# N_init:           initial number of animals
# total_time = 100  in second, total time observed
def Euler_Method(h=1.0, growth_ratio=0.2, capacity=10, N_init=1, total_time=100):
    delta_t = h         # sec, time of one step
    df = pd.DataFrame(columns=['Time', 'Number'])
    for t in range(int(total_time/delta_t)):
        if t==0:
            N = N_init
        else:
            N = N + delta_t * N_dot(N, growth_ratio, capacity)
        df = df.append( {"Time": t*delta_t, "Number": N}, ignore_index=True)
    return df

# Heun Method, aka improved Euler's method is:
# step 1> N_dot(t) = r * N(t) * (K-N(t)) /K
# step 2> N_approx(t+h) = N(t) + h * N_dot(t)
# step 3> N_dot_approx(t+h) = r * N_approx(t+h) * (K-N_approx(t+h)) /K
# step 4> N(t+h) = N(t) + 1/2 * h * (N_dot(t) + N_dot_approx(t+h))
def Heun_Method(h=1.0, growth_ratio=0.2, capacity=10, N_init=1, total_time=100):
    delta_t = h     # sec, time of one step
    df = pd.DataFrame(columns=['Time', 'Number'])
    for t in range(int(total_time/delta_t)):
        if t==0:
            N = N_init
        else:
            N_approx_after = N + delta_t * N_dot(N, growth_ratio, capacity)
            N = N + 1/2 * delta_t * ( N_dot(N, growth_ratio, capacity) + N_dot(N_approx_after, growth_ratio, capacity) )
        df = df.append( {"Time": t*delta_t, "Number": N}, ignore_index=True)
    return df

# Finally,
# Draw 4 simulations
def draw_subplot(ax, df, title=''):
    ax.set_title(title)
    ax.plot(df['Time'], df['Number'])
    ax.set_ylim([0,12])

h=np.array([0.1,1.0,5.0,10.0])
fig, axes = plt.subplots(nrows=2, ncols=4)
for i1 in range(4):
    df = Euler_Method(h=h[i1])
    draw_subplot(axes[0,i1], df, 'Euler\'s h=%.1f'%h[i1] )
for i1 in range(4):
    df = Heun_Method(h=h[i1])
    draw_subplot(axes[1,i1], df, 'Heun\'s h=%.1f'%h[i1] )

plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.4, hspace=0.4)

plt.show()
