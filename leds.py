from raspledstrip.ledstrip import LEDStrip
from raspledstrip.color import wheel_color


class ColumnedLEDStrip(LEDStrip):

    def __init__(self, leds=32, columns=3, gap_leds=4):
        LEDStrip.__init__(self, leds, True)
        self.driver.spi.max_speed_hz = 7000000 #12000000
        print 'Changed spi freq to %d' % self.driver.spi.max_speed_hz
        self.columns = columns
        self._column_data = [0] * columns
        self._gap_leds = gap_leds # + 1
        self._column_leds = (leds - (self._gap_leds * (columns - 1)))/columns
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

    def _display_column(self, column_number, height, color, decay):
        """Display the data for a specific column."""

        height = self._normalize_height(height)


        if height < self._column_data[column_number]:
            height = self._column_data[column_number] * decay


        self._column_data[column_number] = height

        if column_number % 2 == 0:
            start = column_number * (self._gap_leds + self._column_leds)
            end = int(self._column_leds * height) + start
        else:
            end = column_number * (self._gap_leds + self._column_leds) + self._column_leds - 1
            start = end - int(self._column_leds * height)

        if start != end:
            self.fill(color, start, end)

    def display_data(self, data, color=None, decay=0.5):
        """Data is a list of heights.

        The number of columns should be equal to the number of columns!  We
        could improve this, based on how we use it.

        """

        # FIXME: Whatever the f$#@ this is!  Why are we ignoring the color arg?!
        color = self._get_color()

        self.fillOff()
        for column, height in enumerate(data):
            self._display_column(column, height, color, decay)

        self.update()


if __name__ == '__main__':
    import time
    #import random
    led = ColumnedLEDStrip()
    led.all_off()

    for _ in xrange(100000):
        data = [1, 1, 1] # [random.random() for _ in range(led.columns)]
        led.display_data(data)
        print data
        time.sleep(0.01)