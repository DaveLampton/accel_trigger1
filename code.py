# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid
white background, a smaller black rectangle, and some white text.
"""

import board
import busio
import adafruit_lis3dh
import displayio
import terminalio
import time
from adafruit_display_text import label
import adafruit_displayio_ssd1306

i2c = busio.I2C(board.SCL, board.SDA)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x18)
# Range can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G
lis3dh.range = adafruit_lis3dh.RANGE_2_G

#------------------------------------------------------------------------------------
displayio.release_displays()

display_bus = displayio.I2CDisplay(i2c, device_address=0x3D)

WIDTH = 128
HEIGHT = 64  # Change to 64 if needed
BORDER = 5

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group(max_size=10)
display.show(splash)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)

# Create the label
text_area = label.Label(
    terminalio.FONT, text=" "*15, color=0xFFFFFF, x=18, y=HEIGHT // 2 - 1
)
splash.append(text_area)

while True:
    x, y, z = lis3dh.acceleration
    vertical = z - adafruit_lis3dh.STANDARD_GRAVITY
    # Update the label
    if vertical > 0:
        text_area.text = "Z =  %0.2f m/s^2" % vertical
    else:
        text_area.text = "Z = %0.2f m/s^2" % vertical
    time.sleep(0.0001)