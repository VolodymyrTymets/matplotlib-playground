import numpy as np
import struct
import matplotlib.animation as animation;

from src.modules.config_module import nFFT, WAVE_RANGE, RATE, MAX_AMPLITUDE, CHANNELS, FPS

class Fragmenter:
    def __init__(self, fragmenter_spectrum):
        self.mean_noise = 0;
        self.fragment = [];
        self.spectr_fragment = [];
        self.dafault_fragment = np.zeros(int(RATE / 16));
        self.x_lendth = int(RATE / 16);
        self.fragmenter_spectrum = fragmenter_spectrum;
        self.y_L = [];  
        self.y_R = [];
        self.y = [];
    
    def on_data(self, y_L, y_R, y):
        self.y_L = y_L;
        self.y_R = y_R
        self.y = y;

    def save_noise(self, mean_fragment): 
        if(self.mean_noise == 0):
            self.mean_noise = mean_fragment
            return
        if(mean_fragment < self.mean_noise):
            self.mean_noise = mean_fragment
            return
        
    def show_fragment(self, line, fragment, mean_fragment): 
        if(mean_fragment <= self.mean_noise):
            self.fragment = [];
            self.spectrum_fragment = [];
            line.set_ydata(self.dafault_fragment);
            #self.fragmenter_spectrum.set_ydata(self.fragmenter_spectrum.get_dafault_fragment());
        else:
            if(mean_fragment > self.mean_noise * 1.5):
                new_fragment = np.concatenate((self.fragment, fragment));
                new_spectrum_fragment = np.concatenate((self.spectr_fragment, self.y));
                self.fragment = new_fragment;
                self.spectr_fragment = new_spectrum_fragment;
                if(len(new_fragment) >= RATE / 2):
                    to_Dispaly = new_fragment[::16];
                    diff = int(self.x_lendth) - len(to_Dispaly);
                    if(diff > 0):
                        zerows = np.zeros(int(diff / 2) + 100);
                        y = np.concatenate((zerows, to_Dispaly, zerows), axis=0)
                        line.set_ydata(y[0:self.x_lendth])
                    else:
                        line.set_ydata(to_Dispaly[0: self.x_lendth])

                    Y_spectrum = self.strem_amplitude_to_spectr_Y(self.spectr_fragment)
                    self.fragmenter_spectrum.set_ydata(Y_spectrum);
                    self.fragment = [];
                    self.spectr_fragment = [];
    

    def strem_amplitude_to_wave_Y(self):
        return np.hstack((self.y_L, self.y_R));

    def strem_amplitude_to_spectr_Y(self, y):
        y_L = y[::2]
        y_R = y[1::2]
        Y_L = np.fft.fft(y_L, nFFT)
        Y_R = np.fft.fft(y_R, nFFT)
        # Sewing FFT of two channels together, DC part uses right channel's
        Y = abs(np.hstack((Y_L[int(-nFFT / 2):-1], Y_R[:int(nFFT / 2)])))
        return Y;

    def animate(self, i, line, stream, wf, MAX_y):
        Y_wave = self.strem_amplitude_to_wave_Y();
        
        mean_fragment = np.abs(np.mean(Y_wave));
        self.save_noise(mean_fragment=mean_fragment); 
        self.show_fragment(line=line, fragment=Y_wave, mean_fragment=mean_fragment)

        return line,

    def clear(self, line):
        return line,
    
    def init(self, fig, ax):
        # Frequency range
        x_f = 1.0 * np.arange(0, self.x_lendth) / nFFT * self.x_lendth
        ax.set_yscale('linear');
        ax.set_xlim(x_f[0], x_f[-1]);
        ax.set_ylim(-1 * MAX_AMPLITUDE, MAX_AMPLITUDE);  

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



