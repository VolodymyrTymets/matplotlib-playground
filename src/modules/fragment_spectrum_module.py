import numpy as np
import matplotlib.animation as animation;
import pathlib
import matplotlib.ticker as ticker

from src.modules.config_module import nFFT, WAVE_RANGE, RATE, MAX_AMPLITUDE, CHANNELS, FPS

PATH = pathlib.Path().resolve()
COUNT_OF_FRAGMENTS = 5

class Fragmenter_Spectrum:
    def __init__(self):
        self.dafault_fragment = np.zeros(nFFT - 1);
        self.fragment_line = None;
        self.pattertn_line = None;
        self.MAX_y = None;
        self.title = None;
        self.label = None;
        self.pattern = np.zeros(nFFT - 1)
        self.fragments = [];
        self.mean_of_fragments = [];

    def on_data(self, y):
        y_L = y[::2]
        y_R = y[1::2]
        Y_L = np.fft.fft(y_L, nFFT)
        Y_R = np.fft.fft(y_R, nFFT)
        # Sewing FFT of two channels together, DC part uses right channel's
        Y = abs(np.hstack((Y_L[int(-nFFT / 2):-1], Y_R[:int(nFFT / 2)]))) / self.MAX_y;
        if(len(self.fragments) < COUNT_OF_FRAGMENTS):
            self.fragments.append(Y);
            self.mean_of_fragments = np.mean(np.array(self.fragments), axis=0)
            self.display_pattertn_fragment(self.mean_of_fragments)
        
        self.display_fragment(Y)

    def conpare(self, Y1, Y2):
        persentage = [];
        for i in range(int(len(Y1) / 2)):
            a = np.abs(Y1[i]);
            b = np.abs(Y2[i])
            persentage.append(min(a, b) / max(a, b) * 100);    
        return np.mean(persentage);

    def display_pattertn_fragment(self, Y):
        self.pattertn_line.set_ydata(Y)

    def display_fragment(self, Y):
        self.fragment_line.set_ydata(Y)
        simularity = self.conpare(Y, self.mean_of_fragments);
        self.title.set_text(u"{}%".format(int(simularity)))
        self.label.set_text(u"S:{}/{}".format(int(np.max(Y)), int(np.max(self.pattern))))

    def get_dafault_fragment(self):
        return self.dafault_fragment;  

    def clear(self, fragment_line, pattertn_line):
        return fragment_line, pattertn_line

    def animate(self, i, line, stream, wf, MAX_y):
        return line[0], line[1], self.title, self.label

    def init(self, fig, ax, sample_size):
        # Frequency range
        x_f = 1.0 * np.arange(-nFFT / 2 + 1, nFFT / 2) / nFFT * RATE

        ax.set_yscale('symlog');
        ax.set_xlim(x_f[0], x_f[-1]);
        ax.set_ylim(0, 2 * np.pi * nFFT ** 2 / RATE);
        ax.xaxis.set_major_locator(ticker.NullLocator()) 


        self.title = ax.text(0.95,0.5, "", bbox={'facecolor':'w', 'alpha':0, 'pad':5},
                transform=ax.transAxes, ha="center")
        self.label = ax.text(0.1,0.9, "", bbox={'facecolor':'w', 'alpha':0, 'pad':5},
                transform=ax.transAxes, ha="center")


        fragment_line, = ax.plot(x_f, self.dafault_fragment)
        pattertn_line, = ax.plot(x_f, self.dafault_fragment)
        # Because of saving wave, paInt16 will be easier.
        MAX_y = 2.0 ** (sample_size * 8 - 1) * 2
        self.MAX_y = MAX_y

        self.fragment_line = fragment_line;
        self.pattertn_line = pattertn_line;
        frames = None
        wf = None
        stream = None
        ani = animation.FuncAnimation(
            fig, self.animate, frames,
            init_func=lambda: self.clear(fragment_line, pattertn_line), fargs=([fragment_line, pattertn_line], stream, wf, MAX_y),
            cache_frame_data=False,
            interval=1000.0 / FPS, blit=True
        )
        return ani;
        
        



