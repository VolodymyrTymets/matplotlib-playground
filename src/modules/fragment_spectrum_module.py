import numpy as np
import matplotlib.animation as animation;
import pathlib
import matplotlib.ticker as ticker

from src.modules.config_module import nFFT, RATE, FPS, WIDTH, AREA_RANGE, COUNT_OF_FRAGMENTS


PATH = pathlib.Path().resolve()

RIGHT_CHART_POSITION = (((WIDTH / 2) - 40) / 2) - 30;

class Fragmenter_Spectrum:
    def __init__(self, theme, callbacks):
        self.theme = theme;
        self.callbacks = callbacks
        self.dafault_fragment = np.zeros(nFFT - 1);
        self.MAX_y = None;
        self.exlude_indexses = [];
        self.fragments_w = [];
        self.fragments_s = [];
        self.fragmet_s_max = [];
        self.mean_of_fragments_s = [];
        self.max_top = None;
        self.max_bottom = None;
        self.on_between_callback = None;
        self.on_upper_callback = None;
        
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
    

    def strem_amplitude_to_spectrum_Y(self, y):
        y_L = y[::2]
        y_R = y[1::2]
        Y_L = np.fft.fft(y_L, nFFT)
        Y_R = np.fft.fft(y_R, nFFT)
        # Sewing FFT of two channels together, DC part uses right channel's
        return abs(np.hstack((Y_L[int(-nFFT / 2):-1], Y_R[:int(nFFT / 2)]))) / self.MAX_y;
    
    def find_most_diff(self, y):
        if(len(y) % 3 == 0):
            mean =np.mean(y);
            diff = [abs(mean - x) for x in y];
            max_index = diff.index(max(diff))
            self.exlude_indexses.append(max_index);
    
    def without_exlude(self, y):
        res = []
        for i, item in enumerate(y):
          if i not in self.exlude_indexses:
              res.append(item);
        return res;
        

    def on_data(self, y):
        spectrum = self.strem_amplitude_to_spectrum_Y(y=y)
        wave = y
        
        if(len(self.fragments_s) < COUNT_OF_FRAGMENTS):
            self.fragments_s.append(spectrum);
            self.fragments_w.append(wave);
            self.fragmet_s_max.append(np.max(spectrum))
            self.find_most_diff(self.fragmet_s_max)
        
            simular_spectrums = self.without_exlude(self.fragments_s)
            self.mean_of_fragments_s = np.mean(np.array(simular_spectrums), axis=0)
            self.display_pattertn_fragment(self.mean_of_fragments_s)
            simular_wawes = self.without_exlude(self.fragments_w)
             # call listeneres on fragment
            for i in range(len(self.callbacks)):
                callback = self.callbacks[i]
                callback(np.mean(np.array(simular_wawes), axis=0))

        self.display_fragment(spectrum)
     

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
        self.max_top = max_top
        self.max_bottom = max_bottom

    def display_fragment(self, Y):
        max = np.max(Y)
        self.fragment_line.set_ydata(Y)
        self.fragment_line_X.set_ydata(np.full(nFFT - 1, np.max(Y)))

        self.fragment_line_X_annotaion.set_text(int(max))
        self.fragment_line_X_annotaion.set_position((0,max))
        self.fragment_line_X_annotaion.xy = (0, max)
        self.fragment_line_X.set_color(self.theme.get_line_color())
        self.fragment_line.set_color(self.theme.get_line_color())

        if(self.max_bottom and self.max_top and len(self.fragments_s) >= COUNT_OF_FRAGMENTS):
            if(max < self.max_top and max > self.max_bottom and self.on_between_callback):
              self.on_between_callback(max);
              self.fragment_line_X.set_color(self.theme.get_warning_color())
              self.fragment_line.set_color(self.theme.get_warning_color())
            if(max > self.max_top and self.on_upper_callback):
              self.on_upper_callback(max)
              self.fragment_line_X.set_color(self.theme.get_dange_color())
              self.fragment_line.set_color(self.theme.get_dange_color())

    def get_dafault_fragment(self):
        return self.dafault_fragment;  

    def clear(self):
        return self.getAnimateObject()

    def animate(self, i, line, stream, wf, MAX_y):
         return self.getAnimateObject()
    
    def on_beetwen(self, callback):
        self.on_between_callback = callback;
    def on_upper(self, callback):
        self.on_upper_callback = callback;

    def init(self, fig, ax, sample_size):
        # Frequency range
        x_f = 1.0 * np.arange(-nFFT / 2 + 1, nFFT / 2) / nFFT * RATE

        ax.set_yscale('symlog');
        ax.set_xlim(x_f[0], x_f[-1]);
        ax.set_ylim(0, 2 * np.pi * nFFT ** 2 / RATE);
        ax.xaxis.set_major_locator(ticker.NullLocator())
        ax.yaxis.set_major_locator(ticker.NullLocator())
        ax.set_facecolor(self.theme.get_face_color())
        ax.spines['top'].set_color(self.theme.get_border_color())
        ax.spines['bottom'].set_color(self.theme.get_border_color())
        ax.spines['left'].set_color(self.theme.get_border_color())
        ax.spines['right'].set_color(self.theme.get_border_color())

        fragment_line, = ax.plot(x_f, self.dafault_fragment, linewidth=1)
        pattertn_line, = ax.plot(x_f, self.dafault_fragment, linestyle='dashed', linewidth=1, color=self.theme.get_teal_color())
        fragment_line_X, = ax.plot(x_f, self.dafault_fragment, linewidth=1, color=self.theme.get_line_color())
        pattertn_line_X_bottom, = ax.plot(x_f, self.dafault_fragment, linestyle='dashed', linewidth=1, color=self.theme.get_warning_color())
        pattertn_line_X_top, = ax.plot(x_f, self.dafault_fragment, linestyle='dashed', linewidth=1, color=self.theme.get_dange_color())
        pattertn_line_X_annotaion_BR = ax.annotate('', xy=(0, 0), xycoords='data', xytext=(0, 0), textcoords='offset pixels', color=self.theme.get_text_color())
        pattertn_line_X_annotaion_TR = ax.annotate('', xy=(0, 0), xycoords='data', xytext=(0, 0), textcoords='offset pixels', color=self.theme.get_text_color())
        fragment_line_X_annotaion = ax.annotate('', xy=(0, 0), xycoords='data', xytext=(0, 0), textcoords='offset pixels', color=self.theme.get_text_color())
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
        
        



