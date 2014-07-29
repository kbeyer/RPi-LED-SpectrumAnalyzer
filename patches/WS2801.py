import datetime as dt

class WS2801(object):
    """Main driver for WS2801 based LED strips"""

    def __init__(self, leds, use_py_spi = True, dev="/dev/spidev0.0"):
        self.leds = leds
        self.dev = dev
        self.use_py_spi = use_py_spi
        self.last_update = dt.datetime.now()

        if self.use_py_spi:
            import spidev
            self.spi = spidev.SpiDev()
            self.spi.open(0,1)
            self.spi.max_speed_hz = 2000000
            print 'py-spidev MHz: %d' % (self.spi.max_speed_hz / 1000000.0 )
        else:
            self.spi = open(self.dev, "wb")

    #define channel order for this chip
    def channelOrder(*arg):
      return [1,2,0] # BRG - Strands from many other manufacturers


    #define gamma for this chip
    def gamma(*arg):
      gamma = bytearray(256)
      for i in range(256):
        gamma[i] = int(pow(float(i) / 255.0, 2.5) * 255.0)

      return gamma


    #Push new data to strand
    def update(self, buffer):
        temp_buffer = []

        since_last_update = (dt.datetime.now() - self.last_update).microseconds

        # print 'ELAPSED: %d' % (since_last_update)
        # if (since_last_update < 901):
        #   print '<ELAPSED: %d' % (since_last_update)

        if self.use_py_spi:

            #print 'BUFFER: %r' % (buffer)

            # for x in range(self.leds):
            #     self.spi.writebytes()
                #temp_buffer = temp_buffer + [i for i in buffer[x]]

            #print 'TEMP: %r' % (temp_buffer)
            #print 'LENGTH: %d' % (len(temp_buffer))
            temp_buffer = [int(i) for x in xrange(self.leds) for i in buffer[x]]
            self.spi.xfer2(temp_buffer)
        else:
            for x in range(self.leds):
                self.spi.write(buffer[x])
                self.spi.flush()
                print 'TEMP: %r' % (buffer[x])
                print 'LENGTH: %d' % (len(temp_buffer))

        # WS2801 requires 500 micro-second delay between writebytes
        # for low frequencies ... this will happen implicitly
        # for high frequencies it must be explicit
        # time.sleep(0.0005)
        self.last_update = dt.datetime.now()
