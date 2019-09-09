# Question 7
# Simulate a simple rumor model via Euler's and Heun's methods with different parameters

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd

# Based on the code of q3, I generalized every model as a DynamicalModel class
class DynamicalModel:
    # __init__: initialize the model
    # step_size: aka h, is a control for simulation
    # boundary: [lower_boundary, higher_boundary], is a restraint to all state_variables
    # state_varibles: initital condition for every state variable. e.g. [0,0,0] means there're three state varibles, and their values are all zero.
    def __init__(self, step_size=0.01, boundary=[0,0], state_variables=[0,0,0], simulation_method="euler"):
        self.step_size = float(step_size)
        self.boundary = np.array(boundary, dtype=float)
        self.initial_condition = np.array(state_variables, dtype=float)
        self.current_step = 0
        self.reset()
        self.simulation_method = simulation_method.lower()

    # reset: erase all data stored, reset the system to initial condition.
    def reset(self):
        self.data = pd.DataFrame()
        self.state_variables = self.initial_condition.copy()
        self.state_increment = np.zeros_like(self.initial_condition)
        self.observe()

    # continuous_formula: Calculate the dA/dt, dB/dt, ... for each state varible
    # it will be a simple write down of continuous equation
    def continuous_formula(self, state_variables):
        # Must be overwrite
        assert(False)
        state_dots = np.zeros_like(state_variables)
        return state_dots

    # update: simultaneously update all state variables to next step
    def update(self):
        for i, _ in enumerate(self.state_variables):
            self.state_variables[i] = self.state_variables[i] + self.state_increment[i]
        self.boundary_check()

    # observe:store current state variables into data
    # data is stored in the form of pandas.DataFrame:
    # 0     1                   2                   3                   ...
    # Time  state_variable[0]   state_variable[1]   state_variable[2]   ...
    #
    def observe(self):
        _line = [self.current_step * self.step_size]
        _line.extend(self.state_variables)
        _line = [_line]
        self.data = self.data.append(_line, ignore_index=True)

    # increment: Calculate the increment for each state variable according to the continuous equations for each state variable.
    # do consider step size.
    def increment(self):
        if (self.simulation_method=="euler"):
            self.increment_euler()
        elif (self.simulation_method=="heun"):
            self.increment_heun()
        else:
            assert(False)

    # increment: rewrite using Euler's method
    def increment_euler(self):
        state_dots = self.continuous_formula(self.state_variables)
        self.state_increment = self.step_size * state_dots

    # increment: rewrite using Heun's method
    def increment_heun(self):
        state_dots = self.continuous_formula(self.state_variables)
        state_variables_approx = self.state_variables + self.step_size * state_dots
        self.state_increment = self.step_size/2 * (state_dots + self.continuous_formula(state_variables_approx))

    # boundary_check: confine state variables in boundary.
    def boundary_check(self):
        if (self.boundary[0]==self.boundary[1]):
            # boundary isn't set, just skip this check
            return
        for i, state in enumerate(self.state_variables):
            if state < self.boundary[0]:
                self.state_variables[i] = self.boundary[0]
            if state > self.boundary[1]:
                self.state_variables[i] = self.boundary[1]

    # run_simulation: run it
    # if we call this function multiple times, the system will keep go forward, unless we reset() the system.
    def run_simulation(self, max_step=10000, max_time=10000):
        total_step = max_time / self.step_size
        if total_step>max_step:
            total_step = max_step
        for i in range(int(total_step)):
            self.current_step += 1
            self.increment()
            self.update()
            self.observe()

    # get_data: get the result data we want
    # return data is in the form of pandas.DataFrame:
    # 0     1                   2                   3                   ...
    # Time  state_variable[0]   state_variable[1]   state_variable[2]   ...
    #
    def get_data(self):
        return self.data

# Implement our SimpleRumorModel based on the genral DynaicalModel
class SimpleRumorModel(DynamicalModel):
    # additional parameters:
    # total_population: N which is the fixed total population A + B + C
    # infectious_rate: beta
    # antirumor_rate: alpha
    def __init__(self, step_size=1.0, boundary=[0,100], total_population=100, infectious_rate=0.02, antirumor_rate=0.01, initial_population=[1,98,1]):
        # make sure N = A + B + C
        assert(sum(initial_population)==total_population)
        super().__init__(step_size=step_size, boundary=boundary, state_variables=initial_population)
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

    def boundary_check(self):
        DynamicalModel.boundary_check(self)
        self.state_variables = self.state_variables *  (self.total_population/sum(self.state_variables))


# constants like plot style and color
class constant:
    line_styles = ['--', ':', '-.']
    colors = ['#53A567FF', '#56A8CBFF', '#DA291CFF']

if __name__ == "__main__":
    fig, axes = plt.subplots(ncols=3, nrows=3, figsize=(14,8))
    alpha = [0.01, 0.1, 0.5]
    beta = [0.01, 0.05, 0.1]
    labels = ['knew', 'susceptible', 'rumor']
    initial_population = [20, 79, 1]
    for i,_ in enumerate(alpha):
        for j,_ in enumerate(beta):
            model = SimpleRumorModel(step_size=0.2, infectious_rate=alpha[i], antirumor_rate=beta[j], initial_population=initial_population)
            model.run_simulation(max_step=100)
            df = model.get_data()
            axes[i,j].set_title("alpha=%.2f, beta=%.2f"%(alpha[i],beta[j]))
            axes[i,j].set_ylim([-10,110])
            for k in range(3):
                axes[i,j].plot(df.iloc[:,0], df.iloc[:,k+1], constant.line_styles[k], label=labels[k], color=constant.colors[k])

    # Make a custom legend for all subplots
    custom_lines = [ Line2D([0], [0], linestyle=constant.line_styles[i], color=constant.colors[i], lw=2) for i in range(len(labels)) ]

    plt.figlegend(custom_lines, labels, loc='lower center', ncol=4)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.4, hspace=0.5)
    plt.show()
    