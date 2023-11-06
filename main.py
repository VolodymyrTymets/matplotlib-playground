import matplotlib.pyplot as plt
import pyaudio

import src.modules.wave_module as wave_module
import src.modules.spectrum_module as spectrum_module

from src.modules.fragment_module import Fragmenter
from src.modules.fragment_spectrum_module import Fragmenter_Spectrum
from src.modules.config_module import CHANNELS, WIDTH, HEIGHT, RATE, FORMAT, BUF_SIZE;


def main():
  dpi = plt.rcParams['figure.dpi']
  plt.rcParams['savefig.dpi'] = dpi
  plt.rcParams["figure.figsize"] = (1.0 * WIDTH / dpi, 1.0 * HEIGHT / dpi)

  fig, axs = plt.subplots(2, 2, layout='constrained')
  fragmenter_spectrum = Fragmenter_Spectrum();
  fragmenter = Fragmenter(fragmenter_spectrum);


  # Start listening to the microphone
  p = pyaudio.PyAudio();
  rate =  p.get_device_info_by_index(0)['defaultSampleRate']
  stream = p.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=int(rate),
                  input=True,
                  frames_per_buffer=BUF_SIZE)
  stream.start_stream();
  gs = axs[0, 0].get_gridspec()
  axs[0][0].remove()
  axs[0][1].remove()
  ax_row = fig.add_subplot(gs[0, 0:])
  

  ani_wave = wave_module.init(fig=fig, ax=ax_row, stream=stream, sample_size=p.get_sample_size(FORMAT))
  #ani_spectrum = spectrum_module.init(fig=fig, ax=axs[1][0], stream=stream, sample_size=p.get_sample_size(FORMAT))
 
  ani_spectrum = fragmenter_spectrum.init(fig=fig, ax=axs[1][0], stream=stream, sample_size=p.get_sample_size(FORMAT))
  ani_fragment = fragmenter.init(fig=fig, ax=axs[1][1], stream=stream, sample_size=p.get_sample_size(FORMAT))


  plt.show();

  stream.stop_stream()
  stream.close()
  p.terminate()


if __name__ == '__main__':
  main()
