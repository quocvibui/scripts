# Project's idea from "Code as Creative Medium", by Golan Levin and Tega Brain
"""
Color of a Pixel
---------------
Display an image. Create an interactive system that cotinually fetches the color
of the pixel under the mouse as it passes over this image. Use this color to fill
a shape drawn to the screen as the mouse is moved around
"""

from p5 import *

# Mouse
# Circle that moves around with the mouse's position
# For the mouse position's fetch the pixel information and know its color

g_x = 800
g_y = 400

img = []

def setup():
    size(g_x, g_y)
    img.append(load_image("images/2.jpg"))

def draw():
    background(255, 255, 255)
    image(img[0], 0, 0, g_x, g_y)

if __name__ == '__main__':
    run()