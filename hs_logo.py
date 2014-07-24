from raspledstrip.color import SysColors, color_hex
from raspledstrip.ledstrip import LEDStrip


def draw_logo():
    led = LEDStrip(100)

    background_color = SysColors.off
    dark_border = color_hex("#0f173c")
    dark_green = SysColors.white25 #color_hex("2e3b21")
    light_green = color_hex("#6bc325") # SysColors.green

    led.fill(background_color)

    led.fill(dark_border, 28, 32)
    led.fill(dark_border, 35, 37)
    led.fill(dark_border, 39, 39)
    led.fill(dark_border, 43, 44)
    led.fill(dark_border, 48, 48)
    led.fill(dark_border, 50, 53)
    led.fill(dark_border, 55, 55)
    led.fill(dark_border, 59, 60)
    led.fill(dark_border, 64, 64)
    led.fill(dark_border, 66, 68)
    led.fill(dark_border, 71, 75)

    led.fill(light_green, 41, 41)
    led.fill(light_green, 57, 57)
    led.fill(light_green, 61, 61)

    led.fill(dark_green, 42,42)
    led.fill(dark_green, 45,47)
    led.fill(dark_green, 40,40)
    led.fill(dark_green, 62,63)
    led.fill(dark_green, 58,58)
    led.fill(dark_green, 56,56)

    led.fill(SysColors.off, 0, 19)
    led.fill(SysColors.off, 20, 27)
    led.fill(SysColors.off, 76, 83)
    led.fill(SysColors.off, 84)

    led.update()
