import numpy as np
import struct
import matplotlib.animation as animation;

from src.modules.config_module import CHANNELS, nFFT, WAVE_RANGE, RATE, FPS, MAX_AMPLITUDE

class Wave:
  def __init__(self):
      self.y_L = [];  
      self.y_R = [];
  
  def on_data(self, y_L, y_R, y):
    self.y_L = y_L;
    self.y_R = y_R
       
  def animate(self, i, line, stream, wf, MAX_y):
    Y = np.hstack((self.y_L[::2], self.y_R[::2]));
    y_data = line.get_ydata();
    new_y_data = y_data[len(Y):len(y_data)];
    line.set_ydata(np.concatenate((new_y_data, Y)))
    
    return line,

  def clear(self, line):
    return line,

  def init(self, fig, ax): 
    # Frequency range
    x_f = 1.0 * np.arange(1, WAVE_RANGE) / nFFT * RATE
    ax.set_yscale('linear');
    ax.set_xlim(x_f[0], x_f[-1]);
    ax.set_ylim(-1 *  MAX_AMPLITUDE, MAX_AMPLITUDE);  
    
    line, = ax.plot(x_f, np.zeros(WAVE_RANGE - 1))

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