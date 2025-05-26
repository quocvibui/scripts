# Project's idea from "Code as Creative Medium", by Golan Levin and Tega Brain
"""
Collage Machine
---------------
Collect a directory of images. Write a program that uses these to generate collages
of images. Include some unpredictability within it so that it generates a different
collage each time it runs
"""

import os
import random
from p5 import *

images_names = os.listdir("images") # all images we are going to be generating

img = [] # we are going to loading images files into this set

g_x = 800
g_y = 400

def setup():
    size(g_x, g_y)

    for photo in images_names:
        img.append(load_image(f"images/{photo}")) 
    
def draw():
    background(255, 255, 255)

    for i in range(0, 5):
        for photo in img:
            x = random.randint(0, g_x)
            y = random.randint(0, g_y)
            tint(255, 64)
            image(photo, x, y, int(g_x / 3), int(g_y / 3))

    no_loop()

if __name__ == '__main__':
    run()