from PIL import Image, ImageDraw, ImageFont
import os
fontpath = "/usr/share/fonts/truetype/freefont"


from raspledstrip.ledstrip import LEDStrip
from raspledstrip.color import wheel_color, SysColors


def xy_to_led_coordinates(x, y, origin_led=99, strip_along='y', x_length=12, y_length=8):
    if x % 2 == 0:
        led = origin_led - (y_length * x) - y

    else:
        led = origin_led - (y_length * x) + y - (y_length - 1)

    return led


def txt2img(label, fontname="FreeMono.ttf", fgcolor=0,
            bgcolor=255, rotate_angle=0, n=1):
    """Render label as image."""

    # font = # ImageFont.truetype(os.path.join(fontpath,fontname), 12)
    font = ImageFont.load_default()

    imgOut = Image.new("L", (20,49), bgcolor)

    # calculate space needed to render text
    # square blocks of size nxn are rendered
    draw = ImageDraw.Draw(imgOut)
    sizex, sizey = draw.textsize(label*n, font=font)

    imgOut = imgOut.resize((sizex,sizey*n))

    # render label into image draw area
    draw = ImageDraw.Draw(imgOut)
    for i in range(n):
        draw.text((0, sizey*i), label*n, fill=fgcolor, font=font)

    if rotate_angle:
        imgOut = imgOut.rotate(rotate_angle)

    return imgOut


# class CharLEDStrip(LEDStrip):

#     def __init__(self, leds=32, columns=3, gap_leds=4, skip_leds=0):
#         LEDStrip.__init__(self, leds, True)
#         self.driver.spi.max_speed_hz = 7000000 #12000000
#         print 'Changed spi freq to %d' % self.driver.spi.max_speed_hz
#         self.columns = columns
#         self._column_data = [0] * columns
#         self._gap_leds = gap_leds # + 1
#         self._skip_leds = skip_leds
#         self._column_leds = (leds - skip_leds - (self._gap_leds * (columns - 1)))/columns
#         print 'Leds per col: %d' % self._column_leds
#         self._color = 0.0

#     def _normalize_height(self, height, h_min=3, h_range=13):
#         # fixme: h_min = 9, h_range = 1, in the example code.
#         height = (height - h_min) / float(h_range)
#         if height < 0.05:
#             height = 0.05

#         elif height > 1.0:
#             height = 1.0

#         return height

#     def _get_color(self):
#         color = wheel_color(int(self._color))
#         self._color = self._color + 1 if self._color <= 383.9 else 0.0
#         return color

#     def display_data(self, data, color=None):
#         """Data is a list of heights.

#         The number of columns should be equal to the number of columns!  We
#         could improve this, based on how we use it.

#         """

#         self.fillOff()

#         if color is None:
#             color = SysColors.red

#         for i, value in enumerate(data[self._skip_leds:]):
#             if value > 0:
#                 self.set(i+self._skip_leds, color)

#         self.update()


if __name__ == '__main__':
    assert xy_to_led_coordinates(0, 0) == 99
    assert xy_to_led_coordinates(4, 6) == 61
    assert xy_to_led_coordinates(5, 5) == 57
    assert xy_to_led_coordinates(11, 0) == 4
    assert xy_to_led_coordinates(10, 0) == 19
    assert xy_to_led_coordinates(10, 7) == 12

    from raspledstrip.ledstrip import LEDStrip
    import numpy as np
    import time

    led = LEDStrip(100)
    led.all_off()

    for char in 'A':
        img = txt2img(char)
        img.save('/tmp/foo.png', format='PNG')
        arr = np.array(img.getdata()).reshape(img.size)[::, ::-1]
        print arr
        print
        print (arr < 10) * 1
        print
        print arr[1]
        print
        continue
        for x, y in np.argwhere(arr < 100):
            led_num = xy_to_led_coordinates(x, y)
            print led_num
            led.set(led_num, SysColors.red)
        time.sleep(1)
        led.update()
