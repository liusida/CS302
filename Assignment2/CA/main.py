# CA Simulation
#
#        Author: Sida Liu, Connor Klopfer, Wyatt Wu
#        Date: 2019-09-25
#
#
import matplotlib. pyplot as plt
from matplotlib import animation, colors
import numpy as np

# Text description and color mapping for each state
def constants():
    # Possible Cellular States
    states = ["Male", "Female"]
    state_index = np.arange(len(states)+1)
    # http://colorbrewer2.org
    colorbrew2 = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072']#, '#80b1d3', '#fdb462', '#b3de69']
    cmap = colors.ListedColormap(colorbrew2)
    color_bounds=state_index-0.5
    color_norm = colors.BoundaryNorm(color_bounds, cmap.N)
    return colorbrew2, states, state_index, cmap, color_bounds, color_norm

colorbrew2, states, state_index, cmap, color_bounds, color_norm = constants()

# Main Layout, 1 main windows for CA on the right, 3 plots for statistical information on the left, color bar on the bottom left.
def layout():
    fig = plt.figure(figsize=(16, 14))
    grid = plt.GridSpec(4, 4, hspace=0.2, wspace=0.2)
    main_ax = fig.add_subplot(grid[:, 1:])
    main_ax.get_xaxis().set_ticks([])
    main_ax.get_yaxis().set_ticks([])
    info_ax = []
    for i in range(4):
        info_ax.append(fig.add_subplot(grid[i, 0]))
    info_ax[3].axis('off')

    img = info_ax[3].imshow([[0]], cmap=cmap, norm=color_norm)
    plt.colorbar(img, ax=info_ax[3], orientation='horizontal', cmap=cmap, norm=color_norm, boundaries=color_bounds, ticks=state_index)
    return fig, main_ax, info_ax

fig, main_ax, info_ax = layout()

# Setup CA world, size and default populations
def CA_world_setup():
    CA_world_size = (128,128)
    main_data = np.zeros(CA_world_size)
    main_image = main_ax.imshow(main_data, cmap=cmap, norm=color_norm)
    return CA_world_size, main_data, main_image

CA_world_size, main_data, main_image = CA_world_setup()

# Generate data for next step based on CA Rules
class DataGenerator:
    def __init__(self):
        pass
    def __call__(self):
        # update main_data using Rules
        global main_data
        main_data = np.random.randint(low=0, high=len(states), size=CA_world_size)
generator = DataGenerator()
def frames():
    while True:
        yield generator()

# Provide new data to main_image
def animate(args):
    main_image.set_data(main_data)

# Animation Start
anim = animation.FuncAnimation(fig, animate, frames=frames)

plt.show()
