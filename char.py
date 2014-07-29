from PIL import Image, ImageDraw, ImageFont
import time
import numpy as np
import os
fontpath = "/usr/share/fonts/truetype/freefont"


from raspledstrip.ledstrip import LEDStrip
from raspledstrip.color import SysColors, color_hex


# fixme: this code is specific to our setup.  Anybody using this will need to
# tweak this function for their setup.
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

def show_text(led, text, x_offset=0, y_offset=0, sleep=0.5):
    for char in text:
        img = txt2img(char)
        arr = np.array(img.getdata()).reshape(img.size[::-1]).T[::, ::-1]

        for x, y in np.argwhere(arr < 100):
            led_num = xy_to_led_coordinates(x+x_offset, y-y_offset)
            led.set(led_num, color_hex("#6bc325"))
        led.update()
        time.sleep(sleep)
        led.all_off()



if __name__ == '__main__':
    led = LEDStrip(100)
    led.all_off()

    show_text(led, 'NEVER GRADUATE!', x_offset=3, y_offset=1)
