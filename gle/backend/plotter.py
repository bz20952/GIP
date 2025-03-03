from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import utils as u


plt.rcParams.update({
    'font.size': 18,
    'figure.figsize': (8, 5),
    'figure.dpi': 120
})


async def plot_acceleration(data: pd.DataFrame, options: dict):

    """Plot raw acceleration data."""

    accelerometers = options['accelerometers']
    file_suffix = ''

    for acc in accelerometers.keys():
        if accelerometers[acc]:
            file_suffix += f'_{acc}'
            plt.plot(data['t'], data[acc], label=acc)

    plot_path = f'./images/{u.format_filename(options)}_accel{file_suffix}.png'
    
    plt.xlabel('Time [s]')
    plt.ylabel(r'Acceleration [m/s$^2$]')
    plt.title('Raw Acceleration Data')
    plt.legend()
    plt.grid(True)
    plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)
    plt.close()

    return plot_path


async def plot_forcing(data: pd.DataFrame, options: dict):
    
    """Plot raw forcing data."""

    plot_path = f'./images/{u.format_filename(options)}_force.png'

    plt.plot(data['t'], data['F'])
    plt.xlabel('Time [s]')
    plt.ylabel('Force [N]')
    plt.title('Raw Forcing Data')
    plt.grid(True)
    plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)
    plt.close()

    return plot_path


# if __name__ == '__main__':
#     import reader as r
#     data = r.read_csv('FREE_400_5')
#     plot_forcing(data)
#     # plot_acceleration(data, {
#     #     '0': True,
#     #     'l/4': False,
#     #     'l/2': False,
#     #     '3l/4': False,
#     #     'l': True
#     # })