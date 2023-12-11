import pyaudio
## MIC settings 
FPS = 25.0
nFFT = 512
BUF_SIZE = 4 * nFFT
FORMAT = pyaudio.paInt16
CHANNELS = 1

# sample rate - count of samples per seconds 
RATE = 44100
# max int value 
MAX_AMPLITUDE = 32767

## Spectrum settings

# on how much (in percent) spectrum of searched fragment is upper of pattern fragment
AREA_RANGE = [0.2, 0.5]
# on how much (in percent) amplitude shoulb be upper silence to determinate start of fragment
THRESHOLD_OF_SILENCE = 0.8

# rate = 1 seconds
MAX_FRAGMENT_LENGTH = RATE
MIN_FRAGMENT_LENGTH = RATE / 8

# min count of fragment is need to make some assumption
COUNT_OF_FRAGMENTS = 9

# ui
WIDTH = 800
HEIGHT = 480




