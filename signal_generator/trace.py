import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

def plot_wave_gif(wave, sample_rate=44100, filename='wave.gif', save=False):
    fig, ax = plt.subplots()
    xdata, ydata = [], []
    ln, = plt.plot([], [], 'b')

    def init():
        ax.set_xlim(0, len(wave) / sample_rate)
        ax.set_ylim(np.min(wave), np.max(wave))
        return ln,

    def update(frame):
        xdata.append(frame / sample_rate)
        ydata.append(wave[frame])
        ln.set_data(xdata, ydata)
        return ln,

    frames = len(wave)
    fps = round(frames/(len(wave)/sample_rate))
    print(fps)
    speed = 1
    true_fps = speed*fps

    print('Target animation duration: ', frames/true_fps, 's')
    ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, interval=1000/sample_rate)
    
    if save:
        writer = PillowWriter(fps=true_fps)
        ani.save(filename, writer=writer)
    
    # plt.show()
    return ani

if __name__ == "__main__":
    # Example usage
    duration = 2  # seconds
    sample_rate = 100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    frequency = 5  # Hz
    amplitude = 1
    phase = 0
    wave = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    
    plot_wave_gif(wave, sample_rate, 'sine_wave.gif')