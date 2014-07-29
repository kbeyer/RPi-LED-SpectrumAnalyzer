""" Main entry point for running the demo. """


# Standard library
import time
import sys

# Third party library
import alsaaudio as aa

# Local library
from char import show_text
from hs_logo import draw_logo
from leds import ColumnedLEDStrip
from music import calculate_levels, read_musicfile_in_chunks, calculate_column_frequency
from shairplay import initialize_shairplay, shutdown_shairplay, RaopCallbacks

COLUMNS = 12
GAP_LEDS = 0
TOTAL_LEDS = 100
SKIP_LEDS = 4

SAMPLE_RATE = 44100
NUM_CHANNELS = 2
FORMAT = aa.PCM_FORMAT_S16_LE
PERIOD_SIZE = 2048

frequency_limits =  calculate_column_frequency(200, 10000, COLUMNS)


def analyze_airplay_input(led_strip):
    from os.path import join
    lib_path = join(sys.prefix, 'lib')
    initialize_shairplay(lib_path, get_shairplay_callback_class(led_strip))

    while True:
        try:
            pass
        except KeyboardInterrupt:
            shutdown_shairplay()
            break

def analyze_audio_file(led_strip, path):
    for chunk, sample_rate in read_musicfile_in_chunks(path, play_audio=True):
        data = calculate_levels(chunk, sample_rate, frequency_limits)
        led_strip.display_data(data)

def analyze_line_in(led_strip, hacker_school=True):
    start_time = time.time()

    while True:
        if hacker_school and time.time() - start_time > 60 * 2:
            hacker_school_display()
            start_time = time.time()

        size, chunk = input.read()
        if size > 0:
            L = (len(chunk)/2 * 2)
            chunk = chunk[:L]
            data = calculate_levels(chunk, SAMPLE_RATE, frequency_limits)
            led_strip.display_data(data[::-1])


def get_audio_input():
    input = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NONBLOCK)
    input.setchannels(NUM_CHANNELS)
    input.setformat(aa.PCM_FORMAT_S16_BE)
    input.setrate(SAMPLE_RATE)
    input.setperiodsize(PERIOD_SIZE)
    return input

def get_led_strip():
    led = ColumnedLEDStrip(
        leds=TOTAL_LEDS, columns=COLUMNS, gap_leds=GAP_LEDS, skip_leds=SKIP_LEDS
    )
    led.all_off()
    return led

def get_shairplay_callback_class(led_strip):

    class SampleCallbacks(RaopCallbacks):
        def audio_init(self, bits, channels, samplerate):
            print "Initializing", bits, channels, samplerate
            self.bits = bits
            self.channels = channels
            self.samplerate = samplerate

            min_frequency = 500
            max_frequency = samplerate / 30 * 10  # Abusing integer division
            self.frequency_limits = calculate_column_frequency(
                min_frequency, max_frequency, COLUMNS
            )
            self.buffer = ''

        def audio_process(self, session, buffer):
            data = calculate_levels(buffer, self.samplerate, self.frequency_limits, self.channels, self.bits)
            led_strip.display_data(data[::-1])
        def audio_destroy(self, session):
            print "Destroying"
        def audio_set_volume(self, session, volume):
            print "Set volume to", volume
        def audio_set_metadata(self, session, metadata):
            print "Got", len(metadata),  "bytes of metadata"
        def audio_set_coverart(self, session, coverart):
            print "Got", len(coverart), "bytes of coverart"

    return SampleCallbacks

def hacker_school_display(led_strip):
    draw_logo(led_strip)
    time.sleep(1)
    show_text(led_strip, 'NEVER GRADUATE!', x_offset=3, y_offset=1, sleep=0.5)


if __name__ == '__main__':
    from textwrap import dedent

    input_types = ('local', 'linein', 'airplay')
    usage = dedent("""\

    Usage: %s <input-type> [additional arguments]

    input-type: should be one of %s

    To play a local file, you can pass the path to the file as an additional
    argument.

    """) % (sys.argv[0], input_types)

    if len(sys.argv) == 1:
        print usage
        sys.exit(1)

    input_type = sys.argv[1]

    led_strip = get_led_strip()
    if input_type == 'local':
        path = sys.argv[2] if len(sys.argv) > 2 else 'sample.mp3'
        analyze_audio_file(led_strip, path)

    elif input_type == 'airplay':
        analyze_airplay_input(led_strip)

    elif input_type == 'linein':
        analyze_line_in(led_strip)

    else:
        print usage
        sys.exit(1)
