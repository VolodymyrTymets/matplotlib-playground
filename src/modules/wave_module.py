import numpy as np
import struct
import matplotlib.animation as animation;

from src.modules.config_module import CHANNELS, nFFT, WAVE_RANGE, RATE, FPS, MAX_AMPLITUDE

# Wave
def animate(i, line, stream, wf, MAX_y):

  # Read n*nFFT frames from stream, n > 0
  N = int(max(stream.get_read_available() / nFFT, 1) * nFFT)
  data = stream.read(N)

  # Unpack data, LRLRLR...
  y = np.array(struct.unpack("%dh" % (N * CHANNELS), data))

  y_L = y[::2]
  y_R = y[1::2]
  Y = np.hstack((y_L[::2], y_R[::2]));
  
  y_data = line.get_ydata();
  new_y_data = y_data[len(Y):len(y_data)];

  line.set_ydata(np.hstack((new_y_data, Y)))

  return line,

def clear(line):
  return line,

def init(fig, ax, stream, sample_size): 
  # Frequency range
  x_f = 1.0 * np.arange(1, WAVE_RANGE) / nFFT * RATE
 

  ax.set_yscale('linear');
  ax.set_xlim(x_f[0], x_f[-1]);
  ax.set_ylim(-1 *  MAX_AMPLITUDE, MAX_AMPLITUDE);  
  
  line, = ax.plot(x_f, np.zeros(WAVE_RANGE - 1))

  MAX_y = 2.0 ** (sample_size * 8 - 1);

  frames = None
  wf = None
  ani = animation.FuncAnimation(
    fig, animate, frames,
    init_func=lambda: clear(line), fargs=(line, stream, wf, MAX_y),
    cache_frame_data=False,
    interval=1000.0 / FPS, blit=True
  )
  return ani;