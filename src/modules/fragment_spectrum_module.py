import numpy as np
import struct
import matplotlib.animation as animation;

from src.modules.config_module import nFFT, WAVE_RANGE, RATE, MAX_AMPLITUDE, CHANNELS, FPS

class Fragmenter_Spectrum:
    def __init__(self):
        self.dafault_fragment = np.zeros(nFFT - 1);
        self.line = None;

    def set_ydata(self, Y):
        self.line.set_ydata(Y)

    def get_dafault_fragment(self):
        return self.dafault_fragment;  

    def clear(self, line):
        return line, 

    def animate(self, i, line, stream, wf, MAX_y):
        line.set_ydata(line.get_ydata())
        return line,

    def init(self, fig, ax, stream, sample_size):
        # Frequency range
        x_f = 1.0 * np.arange(-nFFT / 2 + 1, nFFT / 2) / nFFT * RATE

        ax.set_yscale('symlog');
        ax.set_xlim(x_f[0], x_f[-1]);
        ax.set_ylim(0, 2 * np.pi * nFFT ** 2);


        line, = ax.plot(x_f, np.zeros(nFFT - 1))
        # Because of saving wave, paInt16 will be easier.
        MAX_y = 2.0 ** (sample_size * 8 - 1) * 2

        self.line = line;
        frames = None
        wf = None
        ani = animation.FuncAnimation(
            fig, self.animate, frames,
            init_func=lambda: self.clear(line), fargs=(line, stream, wf, MAX_y),
            cache_frame_data=False,
            interval=1000.0 / FPS, blit=True
        )
        return ani;
        
        



