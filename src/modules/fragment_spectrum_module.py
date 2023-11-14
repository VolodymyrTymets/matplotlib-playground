import numpy as np
import matplotlib.animation as animation;
import pathlib
import matplotlib.ticker as ticker

from src.modules.config_module import nFFT, RATE, FPS, WIDTH, AREA_RANGE


PATH = pathlib.Path().resolve()
COUNT_OF_FRAGMENTS = 5
RIGHT_CHART_POSITION = (((WIDTH / 2) - 40) / 2) - 30;

class Fragmenter_Spectrum:
    def __init__(self):
        self.dafault_fragment = np.zeros(nFFT - 1);
        self.MAX_y = None;
        self.fragments = [];
        self.mean_of_fragments = [];
        
        # lines
        self.fragment_line = None;
        self.pattertn_line = None;
        self.pattertn_line_X_top = None;
        self.pattertn_line_X_bottom = None;
        self.fragment_line_X = None;

        # annotation 
        self.pattertn_line_X_annotaion_BR = None;
        self.pattertn_line_X_annotaion_TR = None;
        self.fragment_line_X_annotaion  = None;
    
    def getAnimateObject(self): 
       return self.fragment_line, self.pattertn_line, self.fragment_line_X, self.pattertn_line_X_bottom, self.pattertn_line_X_top, self.pattertn_line_X_annotaion_BR, self.pattertn_line_X_annotaion_TR, self.fragment_line_X_annotaion,
    
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
        max = np.max(Y)
        max_top = max + max * AREA_RANGE[1];
        max_bottom = max + max * AREA_RANGE[0]
        self.pattertn_line.set_ydata(Y)

        self.pattertn_line_X_bottom.set_ydata(np.full(nFFT - 1, max_bottom))
        self.pattertn_line_X_top.set_ydata(np.full(nFFT - 1,  max_top))

        self.pattertn_line_X_annotaion_BR.set_text(round(max_bottom, 2));
        self.pattertn_line_X_annotaion_BR.set_position((RIGHT_CHART_POSITION, max_bottom))
        self.pattertn_line_X_annotaion_BR.xy = (RIGHT_CHART_POSITION, max_bottom)

        self.pattertn_line_X_annotaion_TR.set_text(round(max_top, 2));
        self.pattertn_line_X_annotaion_TR.set_position((RIGHT_CHART_POSITION, max_top))
        self.pattertn_line_X_annotaion_TR.xy = (RIGHT_CHART_POSITION, max_top)

    def display_fragment(self, Y):
        max = np.max(Y)
        self.fragment_line.set_ydata(Y)
        self.fragment_line_X.set_ydata(np.full(nFFT - 1, np.max(Y)))

        self.fragment_line_X_annotaion.set_text(int(max))
        self.fragment_line_X_annotaion.set_position((0,max))
        self.fragment_line_X_annotaion.xy = (0, max)

    def get_dafault_fragment(self):
        return self.dafault_fragment;  

    def clear(self):
        return self.getAnimateObject()

    def animate(self, i, line, stream, wf, MAX_y):
         return self.getAnimateObject()

    def init(self, fig, ax, sample_size):
        # Frequency range
        x_f = 1.0 * np.arange(-nFFT / 2 + 1, nFFT / 2) / nFFT * RATE

        ax.set_yscale('symlog');
        ax.set_xlim(x_f[0], x_f[-1]);
        ax.set_ylim(0, 2 * np.pi * nFFT ** 2 / RATE);
        ax.xaxis.set_major_locator(ticker.NullLocator())
        ax.yaxis.set_major_locator(ticker.NullLocator())

        fragment_line, = ax.plot(x_f, self.dafault_fragment, linewidth=1)
        pattertn_line, = ax.plot(x_f, self.dafault_fragment, linestyle='dashed', linewidth=1, color="teal")
        fragment_line_X, = ax.plot(x_f, self.dafault_fragment, linewidth=1, color="blue")
        pattertn_line_X_bottom, = ax.plot(x_f, self.dafault_fragment, linestyle='dashed', linewidth=1, color="teal")
        pattertn_line_X_top, = ax.plot(x_f, self.dafault_fragment, linestyle='dashed', linewidth=1, color="teal")
        pattertn_line_X_annotaion_BR = ax.annotate('', xy=(0, 0), xycoords='data', xytext=(0, 0), textcoords='offset pixels')
        pattertn_line_X_annotaion_TR = ax.annotate('', xy=(0, 0), xycoords='data', xytext=(0, 0), textcoords='offset pixels')
        fragment_line_X_annotaion = ax.annotate('', xy=(0, 0), xycoords='data', xytext=(0, 0), textcoords='offset pixels')
        # Because of saving wave, paInt16 will be easier.
        MAX_y = 2.0 ** (sample_size * 8 - 1) * 2
        self.MAX_y = MAX_y

        self.fragment_line = fragment_line;
        self.pattertn_line = pattertn_line;
        self.fragment_line_X = fragment_line_X;
        self.pattertn_line_X_top = pattertn_line_X_top;
        self.pattertn_line_X_bottom = pattertn_line_X_bottom;
        self.pattertn_line_X_annotaion_BR = pattertn_line_X_annotaion_BR;
        self.pattertn_line_X_annotaion_TR = pattertn_line_X_annotaion_TR;
        self.fragment_line_X_annotaion = fragment_line_X_annotaion;

        frames = None
        wf = None
        stream = None
        line = None
        ani = animation.FuncAnimation(
            fig, self.animate, frames,
            init_func=lambda: self.clear(), 
                fargs=(line, stream, wf, MAX_y),
            cache_frame_data=False,
            interval=1000.0 / FPS, blit=True
        )
        return ani;
        
        



