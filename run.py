# A simple run.py for the demo

import time
import sys
from leds import ColumnedLEDStrip
from music import calculate_levels, read_musicfile_in_chunks, calculate_column_frequency
from shairplay import initialize_shairplay, shutdown_shairplay, RaopCallbacks
import alsaaudio as aa
import random

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = 'sample.mp3'

columns = 12
gap_leds = 0
total_leds = 100
skip_leds = 4

led = ColumnedLEDStrip(leds=total_leds, columns=columns, gap_leds=gap_leds, skip_leds=skip_leds)
led.all_off()
time.sleep(0.1)

frequency_limits =  calculate_column_frequency(20, 20000, columns)

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

        min_frequency = 300
        max_frequency = samplerate / 20 * 10  # Abusing integer division
        self.frequency_limits = calculate_column_frequency(
            min_frequency, max_frequency, columns
        )
        self.buffer = ''

    def audio_process(self, session, buffer):
        # print "Processing", + len(buffer), "bytes of audio"
        if len(self.buffer) < 2048:
            self.buffer += buffer
        else:
            data = calculate_levels(buffer, self.samplerate, self.frequency_limits, self.channels, self.bits)
            # print data
            led.display_data(data)
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
