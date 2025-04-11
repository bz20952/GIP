from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


plt.rcParams.update({
    'font.size': 18,
    'figure.figsize': (8, 5),
    'figure.dpi': 300
})


def linear_to_db(gains):
    return 20*np.log10(gains)


def plot_bode(frequencies, frfs, excitation_location):

    """Generic FRF plotting."""

    fig, axes = plt.subplots(nrows=2, ncols=1, sharex='col', figsize=(10, 8))

    # max_gain = linear_to_db(0)

    for i in range(0, 5*2, 2):
        gains = [linear_to_db(np.abs(frf))[excitation_location*2,i] for k, frf in enumerate(frfs)]
        # if max(gains) > max_gain:
        #     max_gain = max(gains)
        axes[0].plot(frequencies / (2*np.pi), gains, label=f'A{(i/2):.0f}')
        axes[1].plot(frequencies / (2*np.pi), [np.angle(frf)[excitation_location*2,i] for frf in frfs], label=f'A{(i/2):.0f}')

    # print(max_gain)

    axes[0].set_title('Bode plot')
    axes[0].set_ylabel('Gain [dB]')
    axes[0].grid(True)

    axes[1].set_ylabel('Phase [rad]')
    axes[1].set_xlabel('Frequency [Hz]')
    axes[1].grid(True)

    plt.legend()
    fig.savefig('bode.png', bbox_inches='tight')

    # for i in range(0, 5*2, 2):
    #     plt.subplot(2, 1, 1)
    #     plt.plot(frequencies / (2*np.pi), [linear_to_db(np.abs(frf))[excitation_location*2,i] for frf in frfs], label=f'A{(i/2):.0f}')

    # plt.xlabel('Frequency [Hz]')
    # plt.ylabel('Gain [dB]')
    # plt.grid(True)
    # plt.savefig('bode.png', bbox_inches='tight')
    # plt.show()


def plot_mode_shapes(mode_shapes, n_free_dofs):

    """Plot modeshapes."""

    # fixed_node = np.array([0]*n_free_dofs)
    # mode_shapes = np.vstack((mode_shapes, fixed_node))

    fig, axs = plt.subplots(nrows=n_free_dofs, ncols=1, sharex='col')

    for i in range(n_free_dofs):
        axs[i].plot(np.linspace(0, 0.65, 5), mode_shapes[:,i][::-1],)
        axs[i].set_title(f'Mode {i+1}')

    plt.legend()
    plt.show()


def plot_nyquist(frequencies, frfs, excitation_location):

    """Plot Receptance Nyquist plot."""

    for i in range(0, 5*2, 2):
        node_frfs = np.array([frf[excitation_location*2,i] for frf in frfs])
        plt.plot(node_frfs.real, node_frfs.imag, label=f'A{(i/2):.0f}', c='k')
        theta_n_index = np.argmax([np.abs((frf[excitation_location*2,i]).imag) for frf in frfs])
        txt = plt.text((node_frfs.real)[theta_n_index], (node_frfs.imag)[theta_n_index]*0.65, f"{frequencies[theta_n_index]/(2*np.pi):.2f} Hz", color='k', size=30) # text for coordinates and frequency of data point
        break

    from adjustText import adjust_text
    adjust_text([txt], target_x=(node_frfs.real)[[theta_n_index]], target_y=(node_frfs.imag)[[theta_n_index]], arrowprops=dict(arrowstyle="->", color='black', lw=3))

    plt.scatter(0, 0, s=40, c='purple')
    plt.gca().set_aspect('equal', adjustable='box')
    # plt.xlabel('Re')
    # plt.ylabel('Im')
    plt.gca().set_xticklabels([])
    plt.gca().set_yticklabels([])
    plt.grid(True)
    # plt.legend()
    plt.savefig('nyquist.png', bbox_inches='tight')
    plt.show()


def plot_im(frequencies, frfs, excitation_location):

    """Plot Im component of FRF plot."""

    mobility_frf = []
    for freq, frf in zip(frequencies, frfs):
        mobility_frf.append(frf/(1j*freq))

    for i in range(0, 5*2, 2):
        gains = np.abs([mobility_frf[k][excitation_location, i] for k in range(len(frequencies))])
        wn_index = np.argmax(gains)
        plt.plot(i, mobility_frf[excitation_location, i][wn_index], label=f'A{(i/2):.0f}')

    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel('Re')
    plt.ylabel('Im')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_motion(y, v, a, t, n_free_dofs, nodal: bool = True):

    """Generic plotting function for dynamic motion data."""

    for i in range(n_free_dofs):
        if nodal:
            label = f'A{i}'
        else:
            label = f'Mode {i+1}'
        plt.plot(t, y[:,i], label=label)
    plt.title('Displacement')
    plt.xlabel('t [s]', fontsize=18)
    if nodal:
        plt.ylabel('u [m]', fontsize=18)
    else:
        plt.ylabel('q [m]', fontsize=18)
    plt.yticks(fontsize=18)
    plt.xticks(fontsize=18)
    plt.legend()
    plt.show()

    for i in range(n_free_dofs):
        if nodal:
            label = f'A{i}'
        else:
            label = f'Mode {i+1}'
        plt.plot(t, v[:,i], label=label)
    plt.title('Velocity')
    plt.xlabel('t [s]')
    if nodal:
        plt.ylabel('du/dt [m/s]')
    else:
        plt.ylabel('dq/dt [m/s]')
    plt.legend()
    plt.show()

    for i in range(n_free_dofs):
        if nodal:
            label = f'A{i}'
        else:
            label = f'Mode {i+1}'
        plt.plot(a['t'], a[f'A{i}'], label=label)
    plt.title('Acceleration')
    plt.xlabel('t [s]')
    if nodal:
        plt.ylabel('d$^2$u/dt$^2$ [g]')
    else:
        plt.ylabel('d$^2$q/dt$^2$ [g]')
    plt.legend()
    plt.show()