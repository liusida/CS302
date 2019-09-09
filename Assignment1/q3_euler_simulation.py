# Question 3
# Implementation of Euler's forward method
# for simulating continuous one-species model
# Let's do a logistic growth model for example.
# If we want to switch to other models, just change the X_dot function to define new dX/dt

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd

# This is the definition of the original continuous function for both Euler's and Heun's methods.
# Here, we implement the logistic growth.
class LogisticGrowthModel:
    def __init__(self, boundary=[0,100000], growth_ratio=0.2, capacity=10., X_init=1.):
        self.boundary = boundary
        self.growth_ratio = growth_ratio
        self.capacity = capacity
        self.X_init = 1
    
    # Continuous Logistic Growth: 
    # dN/dt = r N (K-N) /K
    # Choose N to be the variable in interest: X
    def X_dot(self, X):
        return self.growth_ratio * X * (self.capacity-X) /self.capacity

# Modify pandas DataFrame, adding additional property for Method name and Line color
# A fancy way to do this is using pandas extension
@pd.api.extensions.register_dataframe_accessor("data")
class CustomedDataFrame:
    def __init__(self, _obj):
        self._obj = _obj
        self.method_name = ""
        self.line_color = "#000000"

# Euler forward method is:
# X( t + delta_t ) = X(t) + r * X(t) * (K-X) /K * delta_t
# One step is delta_t time unit: delta_t is the step size.
# parameters:
# h:                in second, time per step
# growth_ratio:     how quick number grows 
# capacity:         maximum number of animals
# X_init:           initial number of animals
# total_time = 100  in second, total time observed
def Euler_Method(model, h=1.0, total_time=100, max_steps=10000):
    delta_t = h         # sec, time of one step
    df = pd.DataFrame(columns=['Time', 'Number'])
    for t in range(int(total_time/delta_t)):
        if t==0:
            X = model.X_init
        else:
            X = X + delta_t * model.X_dot(X)

        if X<model.boundary[0]:
            X = model.boundary[0]
        if X>model.boundary[1]:
            X = model.boundary[1]
        df = df.append( {"Time": t*delta_t, "Number": X}, ignore_index=True)
        max_steps-=1
        if max_steps<=0:
            break

    df.data.method_name = "Euler"   # set additional properties before return the dataframe
    df.data.line_color = "#339900"  # otherwise it will be rewrite when df=df.append()
    return df

# Heun Method, aka improved Euler's method is:
# step 1> X_dot(t) = r * X(t) * (K-X(t)) /K
# step 2> X_approx(t+h) = X(t) + h * X_dot(t)
# step 3> X_dot_approx(t+h) = r * X_approx(t+h) * (K-X_approx(t+h)) /K
# step 4> X(t+h) = X(t) + 1/2 * h * (X_dot(t) + X_dot_approx(t+h))
def Heun_Method(model, h=1.0, total_time=100, max_steps=10000):
    delta_t = h     # sec, time of one step
    df = pd.DataFrame(columns=['Time', 'Number'])
    for t in range(int(total_time/delta_t)):
        if t==0:
            X = model.X_init
        else:
            X_approx_after = X + delta_t * model.X_dot(X)
            X = X + 1/2 * delta_t * ( model.X_dot(X) + model.X_dot(X_approx_after) )

        if X<model.boundary[0]:
            X = model.boundary[0]
        if X>model.boundary[1]:
            X = model.boundary[1]
        df = df.append( {"Time": t*delta_t, "Number": X}, ignore_index=True)
        max_steps-=1
        if max_steps<=0:
            break

    df.data.method_name = "Heun"
    df.data.line_color = "#aa4422"
    return df

# Finally,
# Draw simulations
# ax: the subplot we want to draw in
# dfs: a list of dataframe with additional property
# title: title of the subplot
# y_max: give a max limit to y
def draw_subplot(ax, dfs, title='', y_max=12):
    ax.set_title(title)
    for df in dfs:
        ax.plot(df['Time'], df['Number'], label=df.data.method_name, color=df.data.line_color)
    ax.set_ylim([0,y_max])

if __name__ == "__main__":
    logistic_model = LogisticGrowthModel()
    h=np.array([0.1,1.0,5.0,10.0])
    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(14,8))
    for i1 in range(4):
        df1 = Euler_Method(model=logistic_model, h=h[i1])
        draw_subplot(axes[0,i1], [df1], 'Euler\'s h=%.1f'%h[i1] )
    for i1 in range(4):
        df2 = Heun_Method(model=logistic_model, h=h[i1])
        draw_subplot(axes[1,i1], [df2], 'Heun\'s h=%.1f'%h[i1] )

    # Make a custom legend for all subplots
    custom_lines = [Line2D([0], [0], color=df1.data.line_color, lw=2),
                    Line2D([0], [0], color=df2.data.line_color, lw=2)]
    plt.figlegend(custom_lines, [df1.data.method_name, df2.data.method_name], loc='lower center', ncol=4)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.4, hspace=0.5)

    plt.show()
