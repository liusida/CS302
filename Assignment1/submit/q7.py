# Question 7
# Simulate a simple rumor model via Euler's and Heun's methods with different parameters

# reusing the basic class DynamicalModel defined in dynamical_model.py
import dynamical_model

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd

# Implement our SimpleRumorModel based on the genral DynaicalModel
class SimpleRumorModel(dynamical_model.DynamicalModel):
    # additional parameters:
    # total_population: N which is the fixed total population A + B + C
    # infectious_rate: beta
    # antirumor_rate: alpha
    def __init__(self, step_size=1.0, total_population=100, infectious_rate=0.02, antirumor_rate=0.01, initial_population=[1,98,1]):
        # make sure N = A + B + C
        assert(sum(initial_population)==total_population)
        super().__init__(step_size=step_size, state_variables=initial_population)
        self.total_population = float(total_population)
        self.infectious_rate = float(infectious_rate)
        self.antirumor_rate = float(antirumor_rate)

    # continuous_formula: write down the continuous dA/dt, ... formula
    def continuous_formula(self, state_variables):
        a = self.antirumor_rate
        b = self.infectious_rate
        A = state_variables[0]
        B = state_variables[1]
        C = state_variables[2]
        state_dots = np.zeros_like(state_variables)
        state_dots[0] = a*A*C
        state_dots[1] = -b*B*C
        state_dots[2] = -a*A*C + b*B*C
        return state_dots


if __name__ == "__main__":
    fig, axes = plt.subplots(ncols=3, nrows=3, figsize=(14,8))
    alpha = [0.01, 0.1, 0.5]
    beta = [0.01, 0.05, 0.1]
    labels = ['knew', 'susceptible', 'rumor']
    initial_population = [20, 79, 1]
    for i,_ in enumerate(alpha):
        for j,_ in enumerate(beta):
            model = SimpleRumorModel(step_size=0.04, infectious_rate=alpha[i], antirumor_rate=beta[j], initial_population=initial_population)
            model.run_simulation(max_step=500)
            df = model.get_data()
            axes[i,j].set_title("alpha=%.2f, beta=%.2f"%(alpha[i],beta[j]))
            axes[i,j].set_ylim([-10,110])
            for k in range(3):
                axes[i,j].plot(df.iloc[:,0], df.iloc[:,k+1], dynamical_model.constant.line_styles[k], label=labels[k], color=dynamical_model.constant.colors[k])

    # Make a custom legend for all subplots
    custom_lines = [ Line2D([0], [0], linestyle=dynamical_model.constant.line_styles[i], color=dynamical_model.constant.colors[i], lw=2) for i in range(len(labels)) ]

    plt.figlegend(custom_lines, labels, loc='lower center', ncol=4)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.4, hspace=0.5)
    plt.show()
    