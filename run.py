# A simple run.py for the demo

import time
import sys
from leds import ColumnedLEDStrip
from music import calculate_levels, read_musicfile_in_chunks, calculate_column_frequency
from shairplay import initialize_shairplay, shutdown_shairplay, RaopCallbacks
import alsaaudio as aa
import random
from hs_logo import draw_logo

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = 'sample.mp3'

columns = 12
gap_leds = 0
total_leds = 100
skip_leds = 4

SAMPLE_RATE = 44100
NUM_CHANNELS = 2
FORMAT = aa.PCM_FORMAT_S16_LE
PERIOD_SIZE = 2048

led = ColumnedLEDStrip(leds=total_leds, columns=columns, gap_leds=gap_leds, skip_leds=skip_leds)
led.all_off()
draw_logo()
time.sleep(1)

frequency_limits =  calculate_column_frequency(200, 10000, columns)


input = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NONBLOCK)
input.setchannels(NUM_CHANNELS)
input.setformat(aa.PCM_FORMAT_S16_BE)
input.setrate(SAMPLE_RATE)
input.setperiodsize(PERIOD_SIZE)

while True:
    size, chunk = input.read()
    if size > 0:
        # make sure chunk is even length
        L = (len(chunk)/2 * 2)
        chunk = chunk[:L]
        data = calculate_levels(chunk, SAMPLE_RATE, frequency_limits)
        print data
        led.display_data(data[::-1])

import sys
sys.exit(1)

# for chunk, sample_rate in read_musicfile_in_chunks(path, play_audio=True):
#     # data = calculate_levels(chunk, sample_rate, frequency_limits)
#     # data = [16 * random.random()] * columns
#     data = [1600] * columns
#     led.display_data(data)

# import sys
# sys.exit(1)

class SampleCallbacks(RaopCallbacks):
    def audio_init(self, bits, channels, samplerate):
        print "Initializing", bits, channels, samplerate
        self.bits = bits
        self.channels = channels
        self.samplerate = samplerate

        min_frequency = 500
        max_frequency = samplerate / 30 * 10  # Abusing integer division
        self.frequency_limits = calculate_column_frequency(
            min_frequency, max_frequency, columns
        )
        self.buffer = ''

    def audio_process(self, session, buffer):
        data = calculate_levels(buffer, self.samplerate, self.frequency_limits, self.channels, self.bits)
        led.display_data(data[::-1])
    def audio_destroy(self, session):
        print "Destroying"
    def audio_set_volume(self, session, volume):
        print "Set volume to", volume
    def audio_set_metadata(self, session, metadata):
        print "Got", len(metadata),  "bytes of metadata"
    def audio_set_coverart(self, session, coverart):
        print "Got", len(coverart), "bytes of coverart"


path = "/home/pi/spectrum-analyzer/shairplay/src/lib/.libs/"
initialize_shairplay(path, SampleCallbacks)

while True:
    try:
        pass
    except KeyboardInterrupt:
        shutdown_shairplay()
        break


# TODO:
# - height normalization fixes.
# - command line to listen on stream or not
# - minor changes to install.sh to install shairplay
