import numpy as np
import struct
import matplotlib.animation as animation;

from src.modules.config_module import nFFT, WAVE_RANGE, RATE, MAX_AMPLITUDE, CHANNELS, FPS

class Fragmenter:
    def __init__(self, fragmenter_spectrum):
        self.noise = [];
        self.mean_noise = 0;
        self.fragment = [];
        self.spectr_fragment = [];
        self.dafault_fragment = np.zeros(RATE);
        self.x_lendth = RATE;
        self.fragmenter_spectrum = fragmenter_spectrum;

    def save_noise(self, mean_fragment): 
        if(self.mean_noise == 0):
            self.mean_noise = mean_fragment
            return
        if(mean_fragment < self.mean_noise):
            self.mean_noise = mean_fragment
            return
        
    def show_fragment(self, line, fragment, mean_fragment, spectrum_fragment): 
        if(mean_fragment <= self.mean_noise):
            self.fragment = [];
            self.spectrum_fragment = [];
            line.set_ydata(self.dafault_fragment);
            #self.fragmenter_spectrum.set_ydata(self.fragmenter_spectrum.get_dafault_fragment());
        else:
            if(mean_fragment > self.mean_noise * 1.5):
                new_fragment = np.concatenate((self.fragment, fragment));
                new_spectrum_fragment = np.concatenate((self.spectr_fragment, spectrum_fragment));
                self.fragment = new_fragment;
                self.spectr_fragment = new_spectrum_fragment;
                if(len(new_fragment) >= RATE / 2):
                    to_Dispaly = new_fragment[::2];
                    diff =  int(RATE) - len(to_Dispaly);
                    zerows =  np.zeros(int(diff - 1));
                    zerows_half = int(len(zerows) / 2)
                    left = zerows[0: zerows_half+ 1];
                    right = zerows[0: zerows_half+ 1]
                    Y = np.concatenate((left, to_Dispaly, right), axis=0)
                    Y_spectrum = self.strem_amplitude_to_spectr_Y(self.spectr_fragment)
                    line.set_ydata(Y)
                    self.fragmenter_spectrum.set_ydata(Y_spectrum);
                    self.fragment = [];
                    self.spectr_fragment = [];
    

    def strem_amplitude_to_wave_Y(self, y_L, y_R):
        Y = np.hstack((y_L, y_R));
        return Y;
    def strem_amplitude_to_spectr_Y(self, y):
        y_L = y[::2]
        y_R = y[1::2]
        Y_L = np.fft.fft(y_L, nFFT)
        Y_R = np.fft.fft(y_R, nFFT)
        # Sewing FFT of two channels together, DC part uses right channel's
        Y = abs(np.hstack((Y_L[int(-nFFT / 2):-1], Y_R[:int(nFFT / 2)])))
        return Y;

    def animate(self, i, line, stream, wf, MAX_y):

        # Read n*nFFT frames from stream, n > 0
        N = int(max(stream.get_read_available() / nFFT, 1) * nFFT)
        data = stream.read(N, exception_on_overflow = False)

        # Unpack data, LRLRLR...
        y = np.array(struct.unpack("%dh" % (N * CHANNELS), data))
        y_L = y[::2]
        y_R = y[1::2]
        Y_wave = self.strem_amplitude_to_wave_Y(y_L, y_R);
        
        mean_fragment = np.abs(np.mean(Y_wave));
        self.save_noise(mean_fragment=mean_fragment); 
        self.show_fragment(line=line, fragment=Y_wave, mean_fragment=mean_fragment, spectrum_fragment=y)

        return line,

    def clear(self, line):
        return line,
    
    def init(self, fig, ax, stream, sample_size):
        # Frequency range
        x_f = 1.0 * np.arange(0, self.x_lendth) / nFFT * self.x_lendth
        ax.set_yscale('linear');
        ax.set_xlim(x_f[0], x_f[-1]);
        ax.set_ylim(-1 * MAX_AMPLITUDE, MAX_AMPLITUDE);  

        line, = ax.plot(x_f, self.dafault_fragment)

        MAX_y = 2.0 ** (sample_size * 8 - 1);

        frames = None
        wf = None
        ani = animation.FuncAnimation(
            fig, self.animate, frames,
            init_func=lambda: self.clear(line), fargs=(line, stream, wf, MAX_y),
            cache_frame_data=False,
            interval=1000.0 / FPS, blit=True
        )
        return ani;



