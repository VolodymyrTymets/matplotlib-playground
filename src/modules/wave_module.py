import numpy as np
import struct
import matplotlib.animation as animation;

from src.modules.config_module import CHANNELS, nFFT, WAVE_RANGE, RATE, FPS

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
  stream_x_f = 1.0 * np.arange(1, WAVE_RANGE) / nFFT * RATE
 

  ax.set_yscale('linear');
  ax.set_xlim(stream_x_f[0], stream_x_f[-1]);
  ax.set_ylim(-32767, 32767);  
  
  line, = ax.plot(stream_x_f, np.zeros(WAVE_RANGE - 1))

  # Change x tick labels for left channel
  # def change_xlabel(evt):
  #   labels = [label.get_text().replace(u'\u2212', '')
  #             for label in ax.get_xticklabels()]
  #   ax.set_xticklabels(labels)
  #   fig.canvas.mpl_disconnect(drawid)
  # drawid = fig.canvas.mpl_connect('draw_event', change_xlabel)
  

  MAX_y = 2.0 ** (sample_size * 8 - 1);

  frames = None
  wf = None
  ani_stream = animation.FuncAnimation(
    fig, animate, frames,
    init_func=lambda: clear(line), fargs=(line, stream, wf, MAX_y),
    cache_frame_data=False,
    interval=1000.0 / FPS, blit=True
  )
  return ani_stream;