from q7_rumor_simulation import *

class DiscreteBifurcationModel(DynamicalModel):

    def __init__(self,r=0.1):
        super().__init__(step_size=1)
        self.r = r

    def increment(self):
        self.state_increment[0] = self.r-self.state_variables[0]**2

rs = []
for i in range(40):
    rs.append(i*0.05)

df_parabola = pd.DataFrame()
for i in range(200):
    x = -1 + i * 0.05
    y = 0 + x - x**2
    df_parabola = df_parabola.append([[x,y]], ignore_index=True)

for i in range(len(rs)):
    #plt.subplot(1,len(rs),i+1)
    m = DiscreteBifurcationModel(r=rs[i])
    m.run_simulation(max_step=50)
    df = m.get_data()
    plt.figure(figsize=(10,10))
    #draw cobweb plot
    s = df.iloc[:,1]
    s = np.repeat(s,2)
    s1 = s.shift(1)
    plt.plot(s1,s)
    #draw straight line
    plt.plot([-1,5],[-1,5], color="#999999", linewidth=0.2)
    p = df_parabola.copy()
    p["2"] = p.iloc[:,1]+rs[i]
    #draw parabola
    plt.plot(p.iloc[:,0], p.iloc[:,2], color="#999999", linewidth=0.2)
    plt.axis("image")
    plt.axis([-0.1,2,-0.1,2])
    plt.title("r=%.2f"%rs[i])
    plt.savefig('./discrete_bifurcation/discrete_bifurcation_%d.png'%i)
    plt.close()