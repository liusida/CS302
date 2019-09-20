# DynamicalModel
#   Basic operations generalized into this base class.
# Usage:
#   1. Define your own class, inheriting DynamicalModel;
#   2. Override and extend the __init__(), set your own parameters;
#   3. Override continuous_formula(), implement your own ODE;
#   4. Call run_simulation(), run your model;
#   5. Call run_simulation() again, if you want continue the simulation;
#   6. Call get_data() get the data after simulation is done.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd

# I generalized every model as a DynamicalModel class
class DynamicalModel:
    # __init__: initialize the model
    # step_size: aka h, is a control for simulation
    # state_varibles: initital condition for every state variable. e.g. [0,0,0] means there're three state varibles, and their values are all zero.
    def __init__(self, step_size=0.01, state_variables=[0,0,0], simulation_method="euler"):
        self.step_size = float(step_size)
        self.initial_condition = np.array(state_variables, dtype=float)
        self.current_step = 0
        self.reset()
        self.simulation_method = simulation_method.lower()

    # continuous_formula: Calculate the dA/dt, dB/dt, ... for each state varible
    # it will be a simple write down of continuous equation
    def continuous_formula(self, state_variables):
        # Must be overwrite
        assert(False)
        state_dots = np.zeros_like(state_variables)
        return state_dots

    # reset: erase all data stored, reset the system to initial condition.
    def reset(self):
        self.data = pd.DataFrame()
        self.state_variables = self.initial_condition.copy()
        self.state_increment = np.zeros_like(self.initial_condition)
        self.observe()

    # update: simultaneously update all state variables to next step
    def update(self):
        for i, _ in enumerate(self.state_variables):
            self.state_variables[i] = self.state_variables[i] + self.state_increment[i]

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


# ========================================
# some constants like plot style and color
class constant:
    line_styles = ['--', ':', '-.']
    colors = ['#53A567FF', '#56A8CBFF', '#DA291CFF']

