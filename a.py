import matplotlib.pyplot as plt

fig, axes = plt.subplots(nrows=3, ncols=3, squeeze=True)
axes[0,0].plot([1,2,3],[1,2,3],color='#110099')


plt.show()