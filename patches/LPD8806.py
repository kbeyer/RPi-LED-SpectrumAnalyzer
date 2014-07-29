class LPD8806(object):
    """Main driver for LPD8806 based LED strips"""

    def __init__(self, leds, use_py_spi = False, dev="/dev/spidev0.0"):
        self.leds = leds
        self.dev = dev
        self.use_py_spi = use_py_spi

        if self.use_py_spi:
            import spidev
            self.spi = spidev.SpiDev()
            self.spi.open(0,0)
            self.spi.max_speed_hz = 16000000
            print 'py-spidev MHz: %d' % (self.spi.max_speed_hz / 1000000.0 )
        else:
            self.spi = open(self.dev, "wb")


    #define channel order for this chip
    def channelOrder(*arg):
        return [1,0,2] #GRB - Strands from Adafruit and some others (default)

    #define gamma for this chip
    def gamma(*arg):
      gamma = bytearray(256)
      for i in range(256):
        # Color calculations from
        # http://learn.adafruit.com/light-painting-with-raspberry-pi
        gamma[i] = 0x80 | int(
                pow(float(i) / 255.0, 2.5) * 127.0 + 0.5
            )

      return gamma


    #Push new data to strand
    def update(self, buffer):
        temp_buffer = []
        if self.use_py_spi:
            for x in range(self.leds):
                temp_buffer = temp_buffer + [i for i in buffer[x]]

            self.spi.xfer2(temp_buffer)
            self.spi.xfer2([0x00,0x00,0x00]) #zero fill the last to prevent stray colors at the end
            self.spi.xfer2([0x00]) #once more with feeling - this helps :)
        else:
            for x in range(self.leds):
                self.spi.write(buffer[x])
                self.spi.flush()
            #seems that the more lights we have the more you have to push zeros
            #not 100% sure why this is yet, but it seems to work
            self.spi.write(bytearray(b'\x00\x00\x00')) #zero fill the last to prevent stray colors at the end
            self.spi.flush()
            self.spi.write(bytearray(b'\x00\x00\x00'))
            self.spi.flush()
            self.spi.write(bytearray(b'\x00\x00\x00'))
            self.spi.flush()
            self.spi.write(bytearray(b'\x00\x00\x00'))
            self.spi.flush()
