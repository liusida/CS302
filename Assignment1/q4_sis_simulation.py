# Question 4
# Simulate SIS model via Euler's and Heun's methods with different parameters
# Let's modify q3, and reuse q3's functions
import q3_euler_simulation as q3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Similar to LogisticGrowthModel, we define a SISModel which contain N_dot function
#  and implement SIS continuous function in it.
class SISModel:
    def __init__(self, boundary=[0,100], total_population=100, infect_rate=0.03, recover_rate=0.25, N_init=1):
        self.boundary = boundary
        self.total_population = total_population
        self.infect_rate = infect_rate
        self.recover_rate = recover_rate
        self.N_init = N_init

    def N_dot(self, N):
        susceptible = N
        infectious = self.total_population - susceptible
        return self.recover_rate * infectious - self.infect_rate * susceptible * infectious

if __name__ == "__main__":
    total_time = 10
    h = np.array([0.01,0.5,2.0])
    #h = np.array([0.1])
    infect_rates = np.array([0.03, 0.06, 0.1])
    fig, axes = plt.subplots(nrows=3, ncols=3)
    for i1 in range(len(h)):
        for i2 in range(len(infect_rates)):
            sis_model = SISModel(total_population=100, N_init=90, infect_rate=infect_rates[i2])
            df1 = q3.Euler_Method(model=sis_model, h=h[i1], total_time=total_time)
            df2 = q3.Heun_Method(model=sis_model, h=h[i1], total_time=total_time)
            q3.draw_subplot(axes[i1,i2], [df1,df2], 'h=%.2f b=%.2f'%(h[i1],infect_rates[i2]), y_max=100 )

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.4, hspace=0.4)

    plt.show()
