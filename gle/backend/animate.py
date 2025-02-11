import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import math


fig, ax = plt.subplots(figsize=(8, 5), dpi=120)
line, = ax.plot([], [])


def init():

    line.set_data([], [])

    return line,


def animate(i, u, step, accelerometers: dict):

    """Animator."""

    L = 0.1

    ax.clear()

    ax.set_xlim(0-L, L*5)
    ax.set_ylim(-20, 20)

    ax.set_ylabel('Displacement [m]')

    step_no = i*step
    y = [u[i][step_no] for i in u.columns[1:] if accelerometers[i]]
    # y = [0, u['u_1'][step_no], u['u_2'][step_no], u['u_3'][step_no], u['u_4'][step_no]]

    # If we assume that the columns on each storey remain a constant length then z = sqrt((j*L)^2-x^2)
    # z = [0]
    # z.extend([math.sqrt((L*j)**2-(u[f'u_{j}'][i])**2) for j in range(1, num_accels)])

    # However, if columns remain a constant length, then they have infinite stiffness which is impossible in reality
    z = [i*0.1 for i, label in enumerate(u.columns[1:]) if accelerometers[label]]
    print(z)

    ax.plot(z, y, marker='o', color='k')

    # Add timer text in the corner
    ax.text(0.70, 0.90, 'Time: {:.2f} s'.format(u['t'][step_no]), transform=ax.transAxes, fontsize=18)

    return line,


def animate_beam(data: pd.DataFrame, options: dict):

    """Animate beam using displacement data."""

    # Plot at every nth interval
    n = 1

    frames = round(len(data['t'])/n)
    fps = round(frames/max(data['t']))
    speed = 1
    true_fps = speed*fps

    print('Target animation duration: ', frames/true_fps, 's')

    ani = animation.FuncAnimation(fig, animate, fargs=(data, n, options['accelerometers']), frames=frames, init_func=init)
    ani.save('./images/beam.gif', writer='pillow', fps=true_fps)

    # plt.show()


if __name__ == '__main__':
    import reader as r
    options = {
        'excitationType': 'FREE',
        'samplingFreq': '400',
        'shakerPosition': '5',
        'accelerometers': {
            '0': True,
            'l/4': True,
            'l/2': False,
            '3l/4': False,
            'l': True
        }
    }
    data = pd.read_csv('./data/disp.csv')
    animate_beam(data, options)