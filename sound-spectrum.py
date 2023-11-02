import struct
import wave

import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pyaudio

SAVE = 0.0
TITLE = ''
WIDTH = 1280
HEIGHT = 720
FPS = 25.0
WAVE_FPS = 25.0

nFFT = 512
WAVE_RANGE = nFFT * 32;
BUF_SIZE = 4 * nFFT
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


# Wave
def animate_wave(i, line, stream, wf, MAX_y):

  # Read n*nFFT frames from stream, n > 0
  N = int(max(stream.get_read_available() / nFFT, 1) * nFFT)
  data = stream.read(N)

  # Unpack data, LRLRLR...
  y = np.array(struct.unpack("%dh" % (N * CHANNELS), data))

  y_L = y[::2]
  y_R = y[1::2]
  Y = np.hstack((y_L[::4], y_R[::4]));
  
  y_data = line.get_ydata();
  new_y_data = y_data[len(Y):len(y_data)];

  line.set_ydata(np.hstack((new_y_data, Y)))

  return line,

def init_wave(line):

  # This data is a clear frame for animation
  # line.set_ydata(np.zeros(nFFT * 2 - 1))
  return line,

def init_wave_chart(fig, axs, stream, sample_size): 
  # Frequency range
  stream_x_f = 1.0 * np.arange(1, WAVE_RANGE) / nFFT * RATE
 
  stream_x= axs[0];

  stream_x.set_yscale('linear');
  stream_x.set_xlim(stream_x_f[0], stream_x_f[-1]);
  stream_x.set_ylim(-32767 * 2, 32767 * 2);  
  
  stream_line, = stream_x.plot(stream_x_f, np.zeros(WAVE_RANGE - 1))

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
    fig, animate_wave, frames,
    init_func=lambda: init_wave(stream_line), fargs=(stream_line, stream, wf, MAX_y),
    cache_frame_data=False,
    interval=1000.0 / WAVE_FPS, blit=True
  )
  return ani_stream;


# Spectrum
def animate(i, line, stream, wf, MAX_y):

  # Read n*nFFT frames from stream, n > 0
  N = int(max(stream.get_read_available() / nFFT, 1) * nFFT)
  data = stream.read(N)

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


def init(line):

  # This data is a clear frame for animation
  line.set_ydata(np.zeros(nFFT - 1))
  return line,


def main():
  dpi = plt.rcParams['figure.dpi']
  plt.rcParams['savefig.dpi'] = dpi
  plt.rcParams["figure.figsize"] = (1.0 * WIDTH / dpi, 1.0 * HEIGHT / dpi)

  fig = plt.figure()
  fig, axs = plt.subplots(2, 1, layout='constrained')

  # Frequency range
  x_f = 1.0 * np.arange(-nFFT / 2 + 1, nFFT / 2) / nFFT * RATE
  # stream_x_f = 1.0 * np.arange(-nFFT + 1, nFFT) / nFFT * RATE
 
  stream_x= axs[0];
  ax= axs[1];

  # stream_x.set_yscale('symlog');
  # stream_x.set_xlim(stream_x_f[0], stream_x_f[-1]);
  # stream_x.set_ylim(0, 2 * np.pi * nFFT ** 2 / RATE);

  ax.set_yscale('symlog');
  ax.set_xlim(x_f[0], x_f[-1]);
  ax.set_ylim(0, 2 * np.pi * nFFT ** 2 / RATE);
  

  line, = ax.plot(x_f, np.zeros(nFFT - 1))
  # stream_line, = stream_x.plot(stream_x_f, np.zeros(nFFT * 2 - 1))

  # # Change x tick labels for left channel
  # def change_xlabel(evt):
  #   labels = [label.get_text().replace(u'\u2212', '')
  #             for label in ax.get_xticklabels()]
  #   ax.set_xticklabels(labels)
  #   fig.canvas.mpl_disconnect(drawid)
  # drawid = fig.canvas.mpl_connect('draw_event', change_xlabel)

  p = pyaudio.PyAudio()
  # Used for normalizing signal. If use paFloat32, then it's already -1..1.
  # Because of saving wave, paInt16 will be easier.
  MAX_y = 2.0 ** (p.get_sample_size(FORMAT) * 8 - 1) * 2

  frames = None
  wf = None

  stream = p.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  frames_per_buffer=BUF_SIZE)

  ani = animation.FuncAnimation(
    fig, animate, frames,
    init_func=lambda: init(line), fargs=(line, stream, wf, MAX_y),
    cache_frame_data=False,
    interval=1000.0 / FPS, blit=True
  )
  
  ani_wave = init_wave_chart(fig=fig, axs=axs, stream=stream, sample_size=p.get_sample_size(FORMAT))

  plt.show();

  stream.stop_stream()
  stream.close()
  p.terminate()


if __name__ == '__main__':
  main()
