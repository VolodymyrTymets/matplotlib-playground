import numpy as np
import matplotlib.animation as animation;
import matplotlib.ticker as ticker

from src.modules.config_module import nFFT, THRESHOLD_OF_SILENCE, MAX_FRAGMENT_LENGTH, MIN_FRAGMENT_LENGTH, MAX_AMPLITUDE, FPS


class Fragmenter:
    def __init__(self, theme, callbacks):
        self.theme = theme;
        self.callbacks = callbacks
        self.fragment = [];
        self.spectr_fragment = [];
        self.dafault_fragment = np.zeros(int(MAX_FRAGMENT_LENGTH / 16));
        self.x_lendth = int(MAX_FRAGMENT_LENGTH / 16);
        self.y_L = [];  
        self.y_R = [];
        self.y = [];
        
        self.line = None
    
    def on_data(self, y_L, y_R, y):
        self.y_L = y_L;
        self.y_R = y_R
        self.y = y;
    
    def get_percentage_of_max(self, mean_fragment):
        return 0 if mean_fragment == 0 else mean_fragment / (MAX_AMPLITUDE) * 100
    
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
        fragment_cut = self.cat_mid(self.fragment, MAX_FRAGMENT_LENGTH)
        to_Dispaly = fragment_cut[::16];
        diff = int(self.x_lendth) - len(to_Dispaly);
        if(diff > 0):
            zerows = np.zeros(int(diff / 2) + 100);
            y = np.concatenate((zerows, to_Dispaly, zerows), axis=0)
            line.set_ydata(y[0:self.x_lendth])
        else:
            line.set_ydata(to_Dispaly[0: self.x_lendth])

        self.line.set_color(self.theme.get_line_color())
        
        # dispaly spectrum
        fragment_cut = self.cat_mid(self.spectr_fragment, MAX_FRAGMENT_LENGTH)
        # call listeneres on fragment
        for i in range(len(self.callbacks)):
            callback = self.callbacks[i]
            callback(fragment_cut)

        
    
    def clear_fragment(self):
        #print('--clear---->')  
        self.fragment = [];
        self.spectr_fragment = [];
    
    ## need change color if stectrum between AREA_RANGE
    def on_between(self, max):
        self.line.set_color(self.theme.get_warning_color())
    ## need change color if stectrum upper AREA_RANGE
    def on_upper(self, max):
        self.line.set_color(self.theme.get_dange_color())
        

    def strem_amplitude_to_wave_Y(self):
        return np.hstack((self.y_L, self.y_R));

    def animate(self, i, line, stream, wf, MAX_y):
        Y_wave = self.strem_amplitude_to_wave_Y();
        percentage = self.get_percentage_of_max(mean_fragment=np.mean(np.abs(Y_wave)));
        len_fragment = len(self.fragment)
        is_start = (len_fragment < MIN_FRAGMENT_LENGTH)
        is_tail = (len_fragment > MIN_FRAGMENT_LENGTH and len_fragment < MAX_FRAGMENT_LENGTH)
        is_end = (len_fragment >= MAX_FRAGMENT_LENGTH)
        if(percentage > THRESHOLD_OF_SILENCE and is_start):
           self.save_fragment(fragment=Y_wave)
        elif(is_tail):
            self.save_fragment(fragment=Y_wave)
        elif(is_end):
            self.display_fragment(line=line)
            self.clear_fragment();
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
        ax.set_facecolor(self.theme.get_face_color())
        ax.spines['top'].set_color(self.theme.get_border_color())
        ax.spines['bottom'].set_color(self.theme.get_border_color())
        ax.spines['left'].set_color(self.theme.get_border_color())
        ax.spines['right'].set_color(self.theme.get_border_color())

        line, = ax.plot(x_f, self.dafault_fragment, linewidth=1, color=self.theme.get_line_color())
        self.line = line

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



