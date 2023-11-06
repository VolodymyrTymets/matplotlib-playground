import numpy as np
import struct
import matplotlib.animation as animation;

from src.modules.config_module import CHANNELS, nFFT, RATE, FPS

def animate(i, line, stream, wf, MAX_y):
  # Read n*nFFT frames from stream, n > 0
  N = int(max(stream.get_read_available() / nFFT, 1) * nFFT)
  data = stream.read(N, exception_on_overflow = False)

  # Unpack data, LRLRLR...
  y = np.array(struct.unpack("%dh" % (N * CHANNELS), data)) / MAX_y
  y_L = y[::2]
  y_R = y[1::2]
 

  Y_L = np.fft.fft(y_L, nFFT)
  Y_R = np.fft.fft(y_R, nFFT)
  

  # Sewing FFT of two channels together, DC part uses right channel's
  Y = abs(np.hstack((Y_L[int(-nFFT / 2):-1], Y_R[:int(nFFT / 2)])))
  line.set_ydata(Y)
  return line,


def clear(line):
  # This data is a clear frame for animation
  line.set_ydata(np.zeros(nFFT - 1))
  return line,

def init(fig, ax, stream, sample_size): 
  # Frequency range
  x_f = 1.0 * np.arange(-nFFT / 2 + 1, nFFT / 2) / nFFT * RATE

  ax.set_yscale('symlog');
  ax.set_xlim(x_f[0], x_f[-1]);
  ax.set_ylim(0, 2 * np.pi * nFFT ** 2 / RATE);
  

  line, = ax.plot(x_f, np.zeros(nFFT - 1))
  # Because of saving wave, paInt16 will be easier.
  MAX_y = 2.0 ** (sample_size * 8 - 1) * 2

  frames = None
  wf = None

  ani = animation.FuncAnimation(
    fig, animate, frames,
    init_func=lambda: clear(line), fargs=(line, stream, wf, MAX_y),
    cache_frame_data=False,
    interval=1000.0 / FPS, blit=True
  )
  return ani;