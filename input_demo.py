import alsaaudio as aa


input = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NONBLOCK)
output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)

SAMPLE_RATE = 44100
NUM_CHANNELS = 2
FORMAT = aa.PCM_FORMAT_S16_LE
PERIOD_SIZE = 2048


for jack in (input, output):
    jack.setchannels(NUM_CHANNELS)
    jack.setformat(aa.PCM_FORMAT_S16_BE)
    jack.setrate(SAMPLE_RATE)
    jack.setperiodsize(PERIOD_SIZE)

while True:
    data = input.read()[-1]
    print len(data)
    output.write(data)

#
# output.setchannels(num_channels)
# output.setrate(sample_rate)
# output.setformat()

# while True:
