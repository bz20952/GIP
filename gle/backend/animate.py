import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import math
from utils import accel_to_disp, format_accel_plot_name


plt.rcParams.update({
    'font.size': 18,
    'figure.figsize': (8, 5),
    'figure.dpi': 300
})


fig, ax = plt.subplots()
fig.tight_layout(pad=3)
line, = ax.plot([], [])


def init():

    line.set_data([], [])

    return line,


def animate(i: int, u: pd.DataFrame, step: int, shaker_position: int):

    """Animator."""

    L = 0.65/4  # Length of entire beam divided into 4 sections

    ax.clear()

    ax.set_xlim(0-L, L*5)
    ax.set_ylim(-0.1, 0.1)

    ax.set_title('Animation')
    ax.set_xlabel('Position [m]')
    ax.set_ylabel('Displacement [m]')

    step_no = i*step
    y = [u[j][step_no] for j in u.columns[1:]]
    # y = [0, u['u_1'][step_no], u['u_2'][step_no], u['u_3'][step_no], u['u_4'][step_no]]

    # If we assume that the columns on each storey remain a constant length then z = sqrt((j*L)^2-x^2)
    # z = [0]
    # z.extend([math.sqrt((L*j)**2-(u[f'u_{j}'][i])**2) for j in range(1, num_accels)])

    # However, if columns remain a constant length, then they have infinite stiffness which is impossible in reality
    z = [i*L for i in range(5)]

    ax.plot(z, y, marker='o', color='k')

    # Plot shaker position in red
    shaker_y = u[f'A{shaker_position}'][step_no]
    shaker_z = L*shaker_position
    ax.plot(shaker_z, shaker_y, marker='o', color='r')

    # Add timer text in the corner
    ax.text(0.70, 0.90, 'Time: {:.2f} s'.format(u['t'][step_no]), transform=ax.transAxes, fontsize=18)

    return line,


async def animate_beam(data: pd.DataFrame, options: dict):

    """Animate beam using displacement data."""

    data = accel_to_disp(data, options)

    # Plot at every nth interval
    n = len(data)//15

    frames = round(len(data['t'])/n)
    fps = round(frames/max(data['t']))
    speed = 1
    true_fps = speed*fps

    # print('Target animation duration: ', frames/true_fps, 's')

    ani = animation.FuncAnimation(fig, animate, fargs=(data, n, options['shakerPosition']), frames=frames, init_func=init)
        
    plot_path = f'./images/{format_accel_plot_name(options, 'anim')}'.replace('.png', '.gif')
    
    ani.save(plot_path, writer='pillow', fps=true_fps)

    return plot_path


if __name__ == '__main__':
    import json
    import asyncio
    import reader as r
    with open('./templates/requestFormat.json') as f:
        options = json.load(f)
    data = r.read_csv(options)
    plot_path = asyncio.run(animate_beam(data, options))
    # data = accel_to_disp(data, options)
    # print(data)