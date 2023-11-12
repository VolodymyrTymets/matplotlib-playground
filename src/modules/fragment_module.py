import numpy as np
import matplotlib.animation as animation;
import matplotlib.ticker as ticker

from src.modules.config_module import nFFT, WAVE_RANGE, RATE, MAX_AMPLITUDE, CHANNELS, FPS

class Fragmenter:
    def __init__(self, callbacks):
        self.callbacks = callbacks
        self.fragment = [];
        self.spectr_fragment = [];
        self.dafault_fragment = np.zeros(int(RATE / 16));
        self.x_lendth = int(RATE / 16);
        self.y_L = [];  
        self.y_R = [];
        self.y = [];
    
    def on_data(self, y_L, y_R, y):
        self.y_L = y_L;
        self.y_R = y_R
        self.y = y;
    
    def get_percentage_of_max(self, mean_fragment):
        return 0 if mean_fragment == 0 else int(mean_fragment / (MAX_AMPLITUDE) * 100)
    
    def cat_mid(self, y, length):
        length_half = int(length / 2)
        all = len(y)
        mid = int(all / 2);
        start = mid - length_half if mid - length_half > 0 else 0
        end = mid + length_half if mid + length_half < all else all
        res = y[start:end];
        return res;

    def save_fragment(self, fragment):
        new_fragment = np.concatenate((self.fragment, fragment));
        self.fragment = new_fragment;

        new_spectrum_fragment = np.concatenate((self.spectr_fragment, self.y));
        self.spectr_fragment = new_spectrum_fragment;
    
    def display_fragment(self, line):
        # dispaly amplitude
        fragment_cut = self.cat_mid(self.fragment, WAVE_RANGE)
        to_Dispaly = fragment_cut[::16];
        diff = int(self.x_lendth) - len(to_Dispaly);
        if(diff > 0):
            zerows = np.zeros(int(diff / 2) + 100);
            y = np.concatenate((zerows, to_Dispaly, zerows), axis=0)
            line.set_ydata(y[0:self.x_lendth])
        else:
            line.set_ydata(to_Dispaly[0: self.x_lendth])
        
        # dispaly spectrum
        fragment_cut = self.cat_mid(self.spectr_fragment, RATE)
        # call listeneres on fragment
        for i in range(len(self.callbacks)):
            callback = self.callbacks[i]
            callback(fragment_cut)
    
    def clear_fragment(self):
        #print('--clear---->')  
        self.fragment = [];
        self.spectr_fragment = [];
        

    def strem_amplitude_to_wave_Y(self):
        return np.hstack((self.y_L, self.y_R));

    def animate(self, i, line, stream, wf, MAX_y):
        Y_wave = self.strem_amplitude_to_wave_Y();
        if(self.get_percentage_of_max(mean_fragment=np.max(Y_wave)) > 1 and len(self.fragment) < RATE):
           self.save_fragment(fragment=Y_wave)
        elif(len(self.fragment) >= RATE / 2):
            self.display_fragment(line=line)
            self.clear_fragment()
        else:
            self.clear_fragment()    

        return line,

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

        line, = ax.plot(x_f, self.dafault_fragment)

        frames = None
        wf = None
        stream = None
        MAX_y = None
        ani = animation.FuncAnimation(
            fig, self.animate, frames,
            init_func=lambda: self.clear(line), fargs=(line, stream, wf, MAX_y),
            cache_frame_data=False,
            interval=1000.0 / FPS, blit=True
        )
        return ani;



