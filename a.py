import pandas as pd
df = pd.DataFrame()
import numpy as np
class A:
    def __init__(self, state_variables=[0,0,0]):
        self.a = np.array(state_variables)
        self.b = np.zeros(len(state_variables))

a = A()
a.a[0] = 1
print(a.a)
print(a.b)

a = A()
print(a.a)
