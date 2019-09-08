# Question 4
# Simulate SIS model via Euler's and Heun's methods with different parameters
# Let's modify q3, and reuse q3's functions
import q3_euler_simulation as q3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd

# Similar to LogisticGrowthModel in q3, we define a SISModel which also contain an X_dot function
#  and implement SIS continuous function in it.
class SISModel:
    # Parameters of SIS Model
    # total_population: N
    # infect_rate: beta
    # recover_rate: gamma
    # X_init: initial susceptible number
    def __init__(self, boundary=[0,100], total_population=100, infect_rate=0.03, recover_rate=0.25, X_init=1):
        self.boundary = boundary
        self.total_population = total_population
        self.infect_rate = infect_rate
        self.recover_rate = recover_rate
        self.X_init = X_init

    # Continous SIS Model:
    # dS/dt = - beta S I + gamma I             <- ! Here, I think maybe it's better to use "dS/dt = - beta S I /N + gamma I", because in the formula introduced in class, beta will be effected by total population. I think beta should be a property associate with the disease itself.
    # dI/dt = beta S I - gamma I
    # S = N - I
    # choose I to be the variable in interest: X
    def X_dot(self, X):
        infectious = X
        susceptible = self.total_population - infectious
        return self.infect_rate * susceptible * infectious - self.recover_rate * infectious

if __name__ == "__main__":
    total_time = 100
    max_steps = 50
    h = np.array([0.01,0.5,2.0])
    infect_rates = np.array([0.03, 0.06, 0.1])
    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(14,8))
    for i1 in range(len(h)):
        for i2 in range(len(infect_rates)):
            sis_model = SISModel(total_population=100, X_init=10, recover_rate=0.25, infect_rate=infect_rates[i2])
            df1 = q3.Euler_Method(model=sis_model, h=h[i1], total_time=total_time, max_steps=max_steps)
            df2 = q3.Heun_Method(model=sis_model, h=h[i1], total_time=total_time, max_steps=max_steps)
            q3.draw_subplot(axes[i1,i2], [df1,df2], 'h=%.2f b=%.2f'%(h[i1],infect_rates[i2]), y_max=100)

    # Make a custom legend for all subplots
    custom_lines = [Line2D([0], [0], color=df1.data.line_color, lw=2),
                    Line2D([0], [0], color=df2.data.line_color, lw=2)]
    plt.figlegend(custom_lines, [df1.data.method_name, df2.data.method_name], loc='lower center', ncol=3)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.4, hspace=0.5)
    
    plt.show()
