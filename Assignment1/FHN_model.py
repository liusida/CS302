from q7_rumor_simulation import *

class FHN_Model(DynamicalModel):
    def __init__(self, state_variables, z):
        super().__init__(step_size=0.02,boundary=[-100,100],state_variables=state_variables)
        self.z = z
    
    def continuous_formula(self, x):
        dots = np.zeros_like(x)
        a=0.7
        b=0.8
        c=3.0
        dots[0] = c*(x[0]-x[0]**3/3+x[1]+self.z)
        dots[1] = -(x[0]-a+b*x[1])/c
        return dots

plt.figure(figsize=(14,8))
conf = [-2,-1.8,-1.5,-1,-0.5,-0.25,0]
for i in range(len(conf)):
    plt.subplot(1,len(conf),i+1)
    m = FHN_Model(state_variables=[0.1,0.1], z=conf[i])
    m.run_simulation(max_step=5000)
    df = m.get_data()
    plt.plot(df[1],df[2])
    plt.axis("image")
    plt.axis([-3,3,-3,3])
    plt.title("z="+str(conf[i]))
plt.show()
