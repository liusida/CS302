# Question 3
# Implementation of Euler's forward method
# for simulating continuous one-species model
# Let's do a logistic growth model.
# dN/dt = r * N * (K-N) /K

# Euler forward method is:
# N( t + delta_t ) = N(t) + r * N(t) * (K-N) /K * delta_t
# One step is delta_t time unit: delta_t is the step size.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# tunable parameter h: in second, time per step
# growth_ratio:     how quick number grows 
# capacity:         maximum number of animals
# N_init:           initial number of animals
# total_time = 100  in second, total time observed
def Experiment(h=1.0, growth_ratio=0.2, capacity=10, N_init=1, total_time=100):
    delta_t = h         # sec, time of one step
    df = pd.DataFrame(columns=['Time', 'Number'])
    for t in range(int(total_time/delta_t)):
        if t==0:
            N = N_init
        else:
            N = N + growth_ratio * N * (capacity-N) /capacity * delta_t
        df = df.append( {"Time":t*delta_t, "Number":N}, ignore_index=True)
    return df

# Draw 4 simulations
h=np.array([[0.1,0.5],[1.0,2.0]])
fig, axes = plt.subplots(nrows=2, ncols=2)
for i1 in range(2):
    for i2 in range(2):
        df = Experiment(h=h[i1,i2])
        axes[i1,i2].set_title('h=%.1f'%h[i1,i2])
        axes[i1,i2].plot(df['Time'], df['Number'])

plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.2, hspace=0.4)
plt.show()
