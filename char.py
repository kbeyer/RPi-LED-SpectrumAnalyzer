from raspledstrip.ledstrip import LEDStrip
from raspledstrip.color import wheel_color, SysColors


def char_to_columns(char, width=12, height=8):
    """ Return data for a character. """
    # fixme: it would be nice to have height / width = 1.5

class CharLEDStrip(LEDStrip):

    def __init__(self, leds=32, columns=3, gap_leds=4, skip_leds=0):
        LEDStrip.__init__(self, leds, True)
        self.driver.spi.max_speed_hz = 7000000 #12000000
        print 'Changed spi freq to %d' % self.driver.spi.max_speed_hz
        self.columns = columns
        self._column_data = [0] * columns
        self._gap_leds = gap_leds # + 1
        self._skip_leds = skip_leds
        self._column_leds = (leds - skip_leds - (self._gap_leds * (columns - 1)))/columns
        print 'Leds per col: %d' % self._column_leds
        self._color = 0.0

    def _normalize_height(self, height, h_min=3, h_range=13):
        # fixme: h_min = 9, h_range = 1, in the example code.
        height = (height - h_min) / float(h_range)
        if height < 0.05:
            height = 0.05

        elif height > 1.0:
            height = 1.0

        return height

    def _get_color(self):
        color = wheel_color(int(self._color))
        self._color = self._color + 1 if self._color <= 383.9 else 0.0
        return color

    def display_data(self, data, color=None):
        """Data is a list of heights.

        The number of columns should be equal to the number of columns!  We
        could improve this, based on how we use it.

        """

        self.fillOff()

        if color is None:
            color = SysColors.red

        for i, value in enumerate(data[self._skip_leds:]):
            if value > 0:
                self.set(i+self._skip_leds, color)

        self.update()


if __name__ == '__main__':
    import time
    import random

    columns = 12
    leds = 100
    led = CharLEDStrip(leds=leds, columns=columns, gap_leds=0, skip_leds=4)
    led.all_off()

    data = [ 1 if i > 50 else 0 for i in xrange(leds) ]
    led.display_data(data)
