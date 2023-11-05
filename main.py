import matplotlib.pyplot as plt
import pyaudio

import src.modules.wave_module as wave_module
import src.modules.spectrum_module as spectrum_module
from src.modules.config_module import CHANNELS, WIDTH, HEIGHT, RATE, FORMAT, BUF_SIZE;


def main():
  dpi = plt.rcParams['figure.dpi']
  plt.rcParams['savefig.dpi'] = dpi
  plt.rcParams["figure.figsize"] = (1.0 * WIDTH / dpi, 1.0 * HEIGHT / dpi)

  fig = plt.figure()
  fig, axs = plt.subplots(2, 1, layout='constrained')

  # Start listening to the microphone
  p = pyaudio.PyAudio();
  stream = p.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  frames_per_buffer=BUF_SIZE)
  
  ani_wave = wave_module.init(fig=fig, ax=axs[0], stream=stream, sample_size=p.get_sample_size(FORMAT))
  ani_spectrum = spectrum_module.init(fig=fig, ax=axs[1], stream=stream, sample_size=p.get_sample_size(FORMAT))

  plt.show();

  stream.stop_stream()
  stream.close()
  p.terminate()


if __name__ == '__main__':
  main()
