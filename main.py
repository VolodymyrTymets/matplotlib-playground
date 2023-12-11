import matplotlib.pyplot as plt
import pyaudio
import numpy as np
import struct
import platform

import src.modules.spectrum_module as spectrum_module

from src.modules.fragment_module import Fragmenter
from src.modules.pattern_fragment_module import PatternFragmenter
from src.modules.theme_module import Theme_Module
from src.modules.wave_module import Wave
from src.modules.mic_module import Mic
from src.modules.fragment_spectrum_module import Fragmenter_Spectrum
from src.modules.config_module import CHANNELS, WIDTH, HEIGHT, RATE, FORMAT, BUF_SIZE, nFFT;


def main():
  theme = Theme_Module();
  plt.rcParams['toolbar'] = 'None'
  dpi = plt.rcParams['figure.dpi']
  plt.rcParams['savefig.dpi'] = dpi
  plt.rcParams["figure.figsize"] = (1.0 * WIDTH / dpi, 1.0 * HEIGHT / dpi)
  plt.rcParams['figure.facecolor'] = theme.get_face_color();

  wave = Wave(theme);
  pattern_fragmenter = PatternFragmenter(theme);
  fragmenter_spectrum = Fragmenter_Spectrum(theme, [pattern_fragmenter.on_data]);
  fragmenter = Fragmenter(theme, [fragmenter_spectrum.on_data]);
  mic = Mic([wave.on_data, fragmenter.on_data]);

  fragmenter_spectrum.on_beetwen(fragmenter.on_between)
  fragmenter_spectrum.on_upper(fragmenter.on_upper)

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

  fig = plt.figure(layout="constrained", edgecolor=None)
  axd = fig.subplot_mosaic(
    """
    AAA
    BBC
    BBD
    """
  ) 
  axs = [];

  for k, ax in axd.items():
    axs.append(ax)

  ani_wave = wave.init(fig=fig, ax=axs[0])
  ani_spectrum = fragmenter_spectrum.init(fig=fig, ax=axs[1], sample_size=p.get_sample_size(FORMAT))
  ani_fragment = fragmenter.init(fig=fig, ax=axs[2])
  ani_pattern_fragmenter = pattern_fragmenter.init(fig=fig, ax=axs[3])

  if platform.system() == 'Linux':
    mng = plt.get_current_fig_manager()
    mng.window.overrideredirect(1)
  plt.show();

  stream.stop_stream()
  stream.close()
  p.terminate()


if __name__ == '__main__':
  main()
