import pyaudio

WIDTH = 1280
HEIGHT = 720
FPS = 25.0

nFFT = 512
WAVE_RANGE = nFFT * 32;
BUF_SIZE = 4 * nFFT
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100