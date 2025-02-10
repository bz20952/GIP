import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import math


fig, ax = plt.subplots(figsize=(8, 5), dpi=120)
line, = ax.plot([], [])


def init():

    line.set_data([], [])

    return line,


def animate(i, u, step):

    """Animator."""

    L = 0.1
    num_accels = 5

    ax.clear()

    ax.set_xlim(0-L, L*num_accels)
    ax.set_ylim(-0.02, 0.02)

    ax.set_ylabel('Displacement [m]')

    step_no = i*step
    y = [0, u['u_1'][step_no], u['u_2'][step_no], u['u_3'][step_no], u['u_4'][step_no]]

    # If we assume that the columns on each storey remain a constant length then z = sqrt((j*L)^2-x^2)
    z = [0]
    z.extend([math.sqrt((L*j)**2-(u[f'u_{j}'][i])**2) for j in range(1, num_accels)])

    # However, if columns remain a constant length, then they have infinite stiffness which is impossible in reality
    # z = [L*j for j in range(num_accels)]

    ax.plot(z, y, marker='o', color='k')

    # Add timer text in the corner
    ax.text(0.70, 0.90, 'Time: {:.2f} s'.format(u['t'][step_no]), transform=ax.transAxes, fontsize=18)

    return line,


def animate_beam(u):

    """Animate beam usinh displacement data."""

    # Plot at every nth interval
    n = 50

    frames = round(len(u['t'])/n)
    fps = round(frames/max(u['t']))
    speed = 1
    true_fps = speed*fps

    print('Target animation duration: ', frames/true_fps, 's')

    ani = animation.FuncAnimation(fig, animate, fargs=(u, n), frames=frames, init_func=init)
    ani.save('./images/beam.gif', writer='pillow', fps=true_fps)

    # plt.show()


if __name__ == '__main__':
    u = pd.read_excel('./data/test.xlsx')
    animate_beam(u)