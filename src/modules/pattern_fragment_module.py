import numpy as np
import matplotlib.animation as animation;
import matplotlib.ticker as ticker

from src.modules.config_module import nFFT, MAX_AMPLITUDE, MAX_FRAGMENT_LENGTH, FPS, COUNT_OF_FRAGMENTS


class PatternFragmenter:
    def __init__(self):
        self.fragment = [];
        self.spectr_fragment = [];
        self.dafault_fragment = np.zeros(int(MAX_FRAGMENT_LENGTH / 16));
        self.x_lendth = int(MAX_FRAGMENT_LENGTH / 16);
        self.y = [];
        self.count_of_fragment = 0
        
        self.label = None;
    
    def on_data(self, y):
        self.count_of_fragment = self.count_of_fragment + 1
        self.y = y;
    
    def cat_mid(self, y, length):
        length_half = int(length / 2)
        all = len(y)
        mid = int(all / 2);
        start = mid - length_half if mid - length_half > 0 else 0
        end = mid + length_half if mid + length_half < all else all
        res = y[start:end];
        return res;
    
    def display_fragment(self, line):
        # dispaly amplitude
        fragment_cut = self.cat_mid(self.y, MAX_FRAGMENT_LENGTH)
        to_Dispaly = fragment_cut[::16];
        diff = int(self.x_lendth) - len(to_Dispaly);
        if(diff > 0):
            zerows = np.zeros(int(diff / 2) + 100);
            y = np.concatenate((zerows, to_Dispaly, zerows), axis=0)
            line.set_ydata(y[0:self.x_lendth])
        else:
            line.set_ydata(to_Dispaly[0: self.x_lendth])
        
        # dispaly spectrum
        fragment_cut = self.cat_mid(self.spectr_fragment, MAX_FRAGMENT_LENGTH)
    
    def clear_fragment(self):
        self.fragment = [];
        self.spectr_fragment = [];
        

    def animate(self, i, line, stream, wf, MAX_y):
        self.display_fragment(line=line)
        if(self.label.set_text):
            self.label.set_text(u"Adjusting:{}/{}".format(COUNT_OF_FRAGMENTS, self.count_of_fragment))

        return line, self.label

    def clear(self, line):
        return line,
    
    def init(self, fig, ax):
        # Frequency range
        x_f = 1.0 * np.arange(0, self.x_lendth) / nFFT * self.x_lendth
        ax.set_yscale('linear');
        ax.set_xlim(x_f[0], x_f[-1]);
        ax.set_ylim(-1 * MAX_AMPLITUDE, MAX_AMPLITUDE);  
        ax.yaxis.set_major_locator(ticker.NullLocator()) 
        ax.xaxis.set_major_locator(ticker.NullLocator())
        ax.set_facecolor('#c0c0c0')

        line, = ax.plot(x_f, self.dafault_fragment, linewidth=1, color="#3232c8")
        self.label = ax.text(0.2,0.9, "", bbox={'facecolor':'w', 'alpha':0, 'pad':5},
            transform=ax.transAxes, ha="center")

        frames = None
        wf = None
        stream = None
        MAX_y = None
        ani = animation.FuncAnimation(
            fig, self.animate, frames,
            init_func=lambda: self.clear(line), fargs=(line, stream, wf, MAX_y),
            cache_frame_data=False,
            interval=1000.0 / 2, blit=True
        )
        return ani;



