import numpy as np
import matplotlib.animation as animation;
import csv
import pathlib

from src.modules.config_module import nFFT, WAVE_RANGE, RATE, MAX_AMPLITUDE, CHANNELS, FPS

PATH = pathlib.Path().resolve()

class Fragmenter_Spectrum:
    def __init__(self):
        self.dafault_fragment = np.zeros(nFFT - 1);
        self.line = None;
        self.MAX_y = None;
        self.title = None;
        self.pattern = np.zeros(nFFT - 1)

    def conpare(self, Y1, Y2):
        persentage = [];
        for i in range(len(Y1)):
            a = Y1[i];
            b = Y2[i]
            persentage.append(min(a, b) / max(a, b) * 100);    
        return np.mean(persentage);

    def set_ydata(self, Y):
        new_Y = Y / self.MAX_y;
        self.line.set_ydata(new_Y)
        simularity = self.conpare(new_Y, self.pattern);
        self.title.set_text(u"{}%".format(int(simularity)))

    def get_dafault_fragment(self):
        return self.dafault_fragment;  

    def clear(self, line):
        return line, 

    def animate(self, i, line, stream, wf, MAX_y):
        return line, self.title

    def show_pattern_line(self, ax, x_f): 
          with open(str(PATH) + '/assets/nerve.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
              Y_srt = np.array(row)
              Y = Y_srt.astype(float)
              self.pattern = Y;
              ax.plot(x_f, Y)

    def init(self, fig, ax, sample_size):
        # Frequency range
        x_f = 1.0 * np.arange(-nFFT / 2 + 1, nFFT / 2) / nFFT * RATE

        ax.set_yscale('symlog');
        ax.set_xlim(x_f[0], x_f[-1]);
        ax.set_ylim(0, 2 * np.pi * nFFT ** 2 / RATE);


        self.title = ax.text(0.95,0.5, "", bbox={'facecolor':'w', 'alpha':0, 'pad':5},
                transform=ax.transAxes, ha="center")


        line, = ax.plot(x_f, np.zeros(nFFT - 1))
        self.show_pattern_line(ax=ax, x_f=x_f);
        # Because of saving wave, paInt16 will be easier.
        MAX_y = 2.0 ** (sample_size * 8 - 1) * 2
        self.MAX_y = MAX_y

        self.line = line;
        frames = None
        wf = None
        stream = None
        ani = animation.FuncAnimation(
            fig, self.animate, frames,
            init_func=lambda: self.clear(line), fargs=(line, stream, wf, MAX_y),
            cache_frame_data=False,
            interval=1000.0 / FPS, blit=True
        )
        return ani;
        
        



