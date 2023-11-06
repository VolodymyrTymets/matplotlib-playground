from __future__ import print_function
import pathlib
import csv

import struct
import wave
import difflib

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

TITLE = ''
WIDTH = 1280
HEIGHT = 720
FPS = 25

nFFT = 512
BUF_SIZE = 4 * nFFT
SAMPLE_SIZE = 2
CHANNELS = 2
RATE = 44100
FILE_NAME = './points/1.wav';
PATH = pathlib.Path(__file__).parent.resolve();

def get_mean_by_fragments(step, MAX_y, file_name):
  file_path = str(PATH) + file_name
  wf = wave.open(file_path, 'rb')
  assert wf.getnchannels() == CHANNELS
  assert wf.getsampwidth() == SAMPLE_SIZE
  assert wf.getframerate() == RATE
  frames = wf.getnframes()

  steps = np.arange(step,  wf.getnframes(), step);
  meamY = [];
  for step in steps:
    data = wf.readframes(int(step))

    # Unpack data, LRLRLR...
    y = np.array(struct.unpack("%dh" % (len(data) / SAMPLE_SIZE), data)) / MAX_y
    y_L = y[::2]
    y_R = y[1::2]

    Y_L = np.fft.fft(y_L, nFFT)
    Y_R = np.fft.fft(y_R, nFFT)

    # Sewing FFT of two channels together, DC part uses right channel's
    Y = abs(np.hstack((Y_L[int(-nFFT / 2):-1], Y_R[:int(nFFT / 2)])))
    meamY.append(Y);
  
  wf.close()
  return np.mean(np.array(meamY), axis=0)

def main():

  dpi = plt.rcParams['figure.dpi']
  plt.rcParams['savefig.dpi'] = dpi
  plt.rcParams["figure.figsize"] = (1.0 * WIDTH / dpi, 1.0 * HEIGHT / dpi)

  fig = plt.figure()

  # Frequency range
  x_f = 1.0 * np.arange(-nFFT / 2 + 1, nFFT / 2) / nFFT * RATE
  ax = fig.add_subplot(111, title=TITLE, xlim=(x_f[0], x_f[-1]),
                       ylim=(0, 2 * np.pi * nFFT ** 2 / RATE))
  ax.set_yscale('symlog')

  MAX_y = 2.0 ** (SAMPLE_SIZE * 8 - 1)


  Y1 = get_mean_by_fragments(step=RATE, MAX_y=MAX_y, file_name='/in/n-1.wav')
  ax.plot(x_f, Y1)

 
  Y2 = get_mean_by_fragments(step=RATE, MAX_y=MAX_y, file_name='/in/6mm-1.wav')
  ax.plot(x_f, Y2)



  # Y3 = get_mean_by_fragments(step=RATE / FPS, MAX_y=MAX_y, file_name='./points/3.wav')
  # ax.plot(x_f, Y3)

  # Y4 = get_mean_by_fragments(step=RATE / FPS, MAX_y=MAX_y, file_name='./points/4.wav')
  # ax.plot(x_f, Y4)

  # Y5 = get_mean_by_fragments(step=RATE / FPS, MAX_y=MAX_y, file_name='./points/5.wav')
  # ax.plot(x_f, Y5)

  sm=difflib.SequenceMatcher(None,Y1,Y2)


  persentage = [];
  for i in range(len(Y1)):
    a = Y1[i];
    b = Y2[i]
    persentage.append(min(a, b) / max(a, b) * 100);
    
 

  print('---MAX_y-->', MAX_y)
  print('---max-->', np.max(Y1))
  print('---max-->', np.max(Y2))
  print('---mean-->', np.mean(persentage))


  # to_write = np.mean(np.array((Y1, Y2)), axis=0)
  # file_path = str(PATH) + '/out/nerve.csv'
  # with open(file_path, 'w', newline='') as file:
  #   writer = csv.writer(file)
  #   writer.writerow(to_write)

  plt.show()




if __name__ == '__main__':
  main()
