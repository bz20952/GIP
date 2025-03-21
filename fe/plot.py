from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


def linear_to_db(gains):
    return 20*np.log10(gains)


def plot_frf(frequencies, gains, excitation_location):

    """Generic FRF plotting."""

    # Compute magnitude and phase
    gains = linear_to_db(gains)

    for i in range(0, 5*2, 2):
        plt.plot(frequencies / (2*np.pi), [gain[excitation_location,i] for gain in gains], label=f'A{(i/2):.0f}')

    # ax[j].set_yscale('log')
    # ax[-1].set_xticks(fontsize=18)
    # ax[-1].set_xlabel(r'$f$ [MHz]', fontsize=18)
    # plt.ylabel('Amplitude [m/N]', fontsize=18)
    # plt.yscale('log')

    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain (dB)')
    plt.grid(True)
    plt.legend(fontsize=18)
    plt.show()


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
        plt.plot(t, a[f'A{i}'], label=label)
    plt.title('Acceleration')
    plt.xlabel('t [s]')
    if nodal:
        plt.ylabel('d$^2$u/dt$^2$ [g]')
    else:
        plt.ylabel('d$^2$q/dt$^2$ [g]')
    plt.legend()
    plt.show()