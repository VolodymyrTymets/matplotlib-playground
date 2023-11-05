import numpy as np
import struct
import matplotlib.animation as animation;

from src.modules.config_module import nFFT, WAVE_RANGE, RATE, MAX_AMPLITUDE, CHANNELS, FPS

class Fragmenter:
    def __init__(self):
        self.noise = [];
        self.mean_noise = 0;
        self.fragment = []
        self.dafaultFragment = np.zeros(RATE);
        self.x_lendth = RATE;

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
            line.set_ydata(self.dafaultFragment);
        else:
            if(mean_fragment > self.mean_noise * 0.5):
                new_fragment = np.concatenate((self.fragment, fragment));
                self.fragment = new_fragment;
                if(len(new_fragment) >= RATE):
                    to_Dispaly = new_fragment[::2]
                    diff =  int(RATE) - len(to_Dispaly);
                    zerows =  np.zeros(int(diff - 1));
                    zerows_half = int(len(zerows) / 2)
                    left = zerows[0: zerows_half+ 1];
                    right = zerows[0: zerows_half+ 1]
                    Y = np.concatenate((left, to_Dispaly, right), axis=0)
                    line.set_ydata(Y)
                    self.fragment = [];
    


    def animate(self, i, line, stream, wf, MAX_y):

        # Read n*nFFT frames from stream, n > 0
        N = int(max(stream.get_read_available() / nFFT, 1) * nFFT)
        data = stream.read(N)

        # Unpack data, LRLRLR...
        y = np.array(struct.unpack("%dh" % (N * CHANNELS), data))

        y_L = y[::2]
        y_R = y[1::2]
        Y = np.hstack((y_L, y_R));
        mean_fragment = np.abs(np.mean(Y));
        self.save_noise(mean_fragment=mean_fragment); 
        self.show_fragment(line=line, fragment=Y, mean_fragment=mean_fragment)

        return line,

    def clear(self, line):
        return line,
    
    def init(self, fig, ax, stream, sample_size):
        # Frequency range
        x_f = 1.0 * np.arange(0, self.x_lendth) / nFFT * self.x_lendth
        ax.set_yscale('linear');
        ax.set_xlim(x_f[0], x_f[-1]);
        ax.set_ylim(-1 * MAX_AMPLITUDE, MAX_AMPLITUDE);  

        line, = ax.plot(x_f, self.dafaultFragment)

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



