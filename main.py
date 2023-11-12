import matplotlib.pyplot as plt
import pyaudio
import numpy as np
import struct
import platform

import src.modules.spectrum_module as spectrum_module

from src.modules.fragment_module import Fragmenter
from src.modules.wave_module import Wave
from src.modules.mic_module import Mic
from src.modules.fragment_spectrum_module import Fragmenter_Spectrum
from src.modules.config_module import CHANNELS, WIDTH, HEIGHT, RATE, FORMAT, BUF_SIZE, nFFT;


def main():
  plt.rcParams['toolbar'] = 'None'
  dpi = plt.rcParams['figure.dpi']
  plt.rcParams['savefig.dpi'] = dpi
  plt.rcParams["figure.figsize"] = (1.0 * WIDTH / dpi, 1.0 * HEIGHT / dpi)

  fig, axs = plt.subplots(2, 2, layout='constrained')
  fragmenter_spectrum = Fragmenter_Spectrum();
  wave = Wave();
  fragmenter = Fragmenter(fragmenter_spectrum);
  mic = Mic([wave.on_data, fragmenter.on_data]);

  # Start listening to the microphone
  p = pyaudio.PyAudio();
  rate =  p.get_device_info_by_index(0)['defaultSampleRate']
  stream = p.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=int(RATE),
                  input=True,
                  frames_per_buffer=BUF_SIZE,
                  stream_callback=mic.callback)
  stream.start_stream();
  gs = axs[0, 0].get_gridspec()
  axs[0][0].remove()
  axs[0][1].remove()
  ax_row = fig.add_subplot(gs[0, 0:])
  

  ani_wave = wave.init(fig=fig, ax=ax_row)
  ani_spectrum = fragmenter_spectrum.init(fig=fig, ax=axs[1][0], sample_size=p.get_sample_size(FORMAT))
  ani_fragment = fragmenter.init(fig=fig, ax=axs[1][1])


  if platform.system() == 'Linux':
    mng = plt.get_current_fig_manager()
    mng.window.overrideredirect(1)
  plt.show();

  stream.stop_stream()
  stream.close()
  p.terminate()


if __name__ == '__main__':
  main()
