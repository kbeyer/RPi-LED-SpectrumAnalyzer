import logging

import alsaaudio as aa
import decoder
import numpy as np
import urllib2

CHUNK_SIZE = 2048

def read_music_from_url(url="http://mp3.streampower.be/radio1-high.mp3", chunk_size=CHUNK_SIZE, play_audio=False):

    #f=file('via_url.mp3', 'w')

    url=urllib2.urlopen(url)

    sample_rate = 44100 #musicfile.getframerate()
    num_channels = 2 #musicfile.getnchannels()

    if play_audio:
        output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
        output.setchannels(num_channels)
        output.setrate(sample_rate)
        output.setformat(aa.PCM_FORMAT_S16_LE)
        output.setperiodsize(CHUNK_SIZE)

    while True:
        #f.write(url.read(CHUNK_SIZE))
        chunk = url.read(CHUNK_SIZE)
        if len(chunk) == 0:
            break
        if play_audio:
            output.write(chunk)

        yield chunk, sample_rate


def read_musicfile_in_chunks(path, chunk_size=CHUNK_SIZE, play_audio=True):
    """ Read the music file at the given path, in chunks of the given size. """

    musicfile = decoder.open(path)
    sample_rate = musicfile.getframerate()
    num_channels = musicfile.getnchannels()

    if play_audio:
        output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
        output.setchannels(num_channels)
        output.setrate(sample_rate)
        output.setformat(aa.PCM_FORMAT_S16_LE)
        output.setperiodsize(CHUNK_SIZE)

    # fixme: we could do the writing to audio in a thread ... ?

    while True:
        chunk = musicfile.readframes(CHUNK_SIZE)
        if len(chunk) == 0:
            break
        if play_audio:
            output.write(chunk)

        yield chunk, sample_rate


def calculate_column_frequency(min_frequency, max_frequency, columns):
    """Split the given frequency range in 'column' number of ranges.

    The function splits up the given range into smaller ranges, which have
    equal number of octaves.

    """

    logging.debug('Calculating frequencies for %d columns.', columns)
    octaves = np.log2(max_frequency / min_frequency)
    logging.debug('Octaves in selected frequency range ... %s', octaves)
    octaves_per_column = octaves / columns

    frequency_limits = [
        min_frequency * 2**(octaves_per_column*n) for n in range(columns+1)
    ]

    return zip(frequency_limits[:-1], frequency_limits[1:])


def piff(val, sample_rate):
    """Return the power array index corresponding to a particular frequency."""

    return int(CHUNK_SIZE * val / sample_rate)


def calculate_levels(data, sample_rate, frequency_limits):
    """Calculate frequency response for each channel

    Initial FFT code inspired from the code posted here:
    http://www.raspberrypi.org/phpBB3/viewtopic.php?t=35838&p=454041

    Optimizations from work by Scott Driscoll:
    http://www.instructables.com/id/Raspberry-Pi-Spectrum-Analyzer-with-RGB-LED-Strip-/

    """

    # create a numpy array. This won't work with a mono file, stereo only.
    data_stereo = np.frombuffer(data, dtype=np.int16)
    data = data_stereo[::2]  # pull out the even values, just using left channel

    # if you take an FFT of a chunk of audio, the edges will look like
    # super high frequency cutoffs. Applying a window tapers the edges
    # of each end of the chunk down to zero.
    window = np.hanning(len(data))
    data = data * window

    # Apply FFT - real data
    # We drop the last element in array to make it the same size as CHUNK_SIZE
    fourier = np.fft.rfft(data)[:-1]

    # Calculate the power spectrum
    power = np.abs(fourier) ** 2

    columns = len(frequency_limits)

    # take the log10 of the resulting sum to approximate how human ears perceive sound levels
    matrix = [
        np.log10(
            np.sum(
                power[
                    piff(frequency_limits[i][0], sample_rate):
                    piff(frequency_limits[i][1], sample_rate)
                ]
            )
        )

        for i in range(columns)
    ]

    return matrix


if __name__ == '__main__':

    frequency_limits =  calculate_column_frequency(400, 12000)

    for chunk, sample_rate in read_musicfile_in_chunks('sample1.mp3', play_audio=True):
        data = calculate_levels(chunk, sample_rate, frequency_limits)
        print data