import numpy as np
import struct
import matplotlib.animation as animation;
import pyaudio

from src.modules.config_module import nFFT, BUF_SIZE

class Mic:
  def __init__(self, callbacks):
      self.callbacks = callbacks
  
  # callback function to stream audio, another thread.
  def callback(self, in_data, frame_count, time_info, status):
      # Unpack data, LRLRLR...
      y = np.array(struct.unpack("%dh" % (BUF_SIZE), in_data))
      y_L = y[::2]
      y_R = y[1::2]
      for i in range(len(self.callbacks)):
         callback = self.callbacks[i]
         callback(y_L, y_R, y)

      # If len(data) is less than requested frame_count, PyAudio automatically
      # assumes the stream is finished, and the stream stops.
      return (in_data, pyaudio.paContinue)