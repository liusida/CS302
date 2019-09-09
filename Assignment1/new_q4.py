# Improve the implementation of Question 4, reusing the basic class DynamicalModel defined in q7
import q7_rumor_simulation as q7

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

class SISModel(q7.DynamicalModel):
    def __init__(self, step_size, total_population, X_init, recover_rate, infect_rate, simulation_method):
        super().__init__(step_size=step_size, boundary=[0,total_population], state_variables=[X_init], simulation_method=simulation_method)
        self.infect_rate = float(infect_rate)
        self.recover_rate = float(recover_rate)
        self.total_population = float(total_population)

    def continuous_formula(self, state_variables):
        state_dots = state_variables.copy()
        infectious = state_variables[0]             #<-- Don't use self.state_variables, because in Heun's method we also need to compute F(x_approx) instead of F(x)
        susceptible = self.total_population - infectious
        state_dots[0] = self.infect_rate * susceptible * infectious - self.recover_rate * infectious
        return state_dots

if __name__ == "__main__":
    h = [0.01,0.5,2.0]
    infect_rates = [0.03, 0.06, 0.1]
    methods = ["Euler", "Heun"]
    plt.figure(figsize=(14,8))

    for i1 in range(len(h)):
        for i2 in range(len(infect_rates)):
            plt.subplot(len(h), len(infect_rates), i1*len(infect_rates)+i2+1)
            for i3 in range(len(methods)):
                sis_model = SISModel(step_size=h[i1], total_population=100, X_init=10, recover_rate=0.25, infect_rate=infect_rates[i2], simulation_method=methods[i3])
                sis_model.run_simulation(max_step=50)
                df = sis_model.get_data()
                plt.plot(df.iloc[:,0], df.iloc[:,1], q7.constant.line_styles[i3], color=q7.constant.colors[i3], label=methods[i3])
            plt.title('h=%.2f b=%.2f'%(h[i1],infect_rates[i2]))
            plt.ylim((0,100))

    # Make a custom legend for all subplots
    custom_lines = [ Line2D([0], [0], linestyle=q7.constant.line_styles[i], color=q7.constant.colors[i], lw=2) for i in range(len(methods)) ]
    plt.figlegend(custom_lines, methods, loc='lower center', ncol=3)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.4, hspace=0.5)
    
    plt.show()
