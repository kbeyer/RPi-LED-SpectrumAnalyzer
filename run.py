# A simple run.py for the demo

import time
import sys
from leds import ColumnedLEDStrip
from music import calculate_levels, read_musicfile_in_chunks, calculate_column_frequency

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = 'sample.mp3'

columns = 10
gap_leds = 0
total_leds = 80

led = ColumnedLEDStrip(leds=total_leds, columns=columns, gap_leds=gap_leds)
led.all_off()
time.sleep(0.1)

frequency_limits =  calculate_column_frequency(20, 20000, columns)

for chunk, sample_rate in read_musicfile_in_chunks(path, play_audio=True):
    data = calculate_levels(chunk, sample_rate, frequency_limits)
    led.display_data(data)