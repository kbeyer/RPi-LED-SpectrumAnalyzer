from raspledstrip.color import SysColors, color_hex

def draw_logo(led_strip):

    background_color = SysColors.off
    dark_border = color_hex("#0f173c")
    dark_green = SysColors.white25 #color_hex("2e3b21")
    light_green = color_hex("#6bc325") # SysColors.green

    led_strip.fill(background_color)

    led_strip.fill(dark_border, 28, 32)
    led_strip.fill(dark_border, 35, 37)
    led_strip.fill(dark_border, 39, 39)
    led_strip.fill(dark_border, 43, 44)
    led_strip.fill(dark_border, 48, 48)
    led_strip.fill(dark_border, 50, 53)
    led_strip.fill(dark_border, 55, 55)
    led_strip.fill(dark_border, 59, 60)
    led_strip.fill(dark_border, 64, 64)
    led_strip.fill(dark_border, 66, 68)
    led_strip.fill(dark_border, 71, 75)

    led_strip.fill(light_green, 41, 41)
    led_strip.fill(light_green, 57, 57)
    led_strip.fill(light_green, 61, 61)

    led_strip.fill(dark_green, 42,42)
    led_strip.fill(dark_green, 45,47)
    led_strip.fill(dark_green, 40,40)
    led_strip.fill(dark_green, 62,63)
    led_strip.fill(dark_green, 58,58)
    led_strip.fill(dark_green, 56,56)

    led_strip.fill(SysColors.off, 0, 19)
    led_strip.fill(SysColors.off, 20, 27)
    led_strip.fill(SysColors.off, 76, 83)
    led_strip.fill(SysColors.off, 84)

    led_strip.update()
