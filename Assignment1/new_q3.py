# Improve the implementation of Question 3, reusing the basic class DynamicalModel defined in q7
import q7_rumor_simulation as q7

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

class LogisticGrowthModel(q7.DynamicalModel):
    # basic settings and initial conditions
    def __init__(self, step_size=1, simulation_method="euler", growth_ratio=0.2, capacity=10, X_init=1):
        super().__init__(step_size=step_size, state_variables=[X_init], simulation_method=simulation_method )
        self.growth_ratio = growth_ratio
        self.capacity = capacity
        self.X_init = 1
    # continuous formula:
    # state_dots[0] = dx/dt = ...
    # state_dots[1] = dy/dt = ...
    def continuous_formula(self, state_variables):
        state_dots = state_variables.copy()
        state_dots[0] = self.growth_ratio * state_variables[0] * (self.capacity-state_variables[0]) /self.capacity
        return state_dots

if __name__ == "__main__":
    h = [0.1,1,5,10]
    methods = ["Euler", "Heun"]
    plt.figure(figsize=(14,6))

    for j in range(len(methods)):
        for i in range(len(h)):
            plt.subplot(len(methods), len(h), j*len(h)+i+1)
            model = LogisticGrowthModel(step_size=h[i], simulation_method=methods[j])
            model.run_simulation(max_time=50)
            df = model.get_data()
            plt.plot(df.iloc[:,0], df.iloc[:,1], q7.constant.line_styles[j],color=q7.constant.colors[j], label=methods[j])
            plt.xlabel("Time")
            plt.ylabel("Population")
    
    # Make a custom legend for all subplots
    custom_lines = [ Line2D([0], [0], linestyle=q7.constant.line_styles[i], color=q7.constant.colors[i], lw=2) for i in range(len(methods)) ]
    plt.figlegend(custom_lines, methods, loc='lower center', ncol=4)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.15, wspace=0.4, hspace=0.3)
    plt.show()