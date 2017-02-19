#!/usr/bin/python3
# to_dat.py
#
# Opens an image, and then writes out the values of the pixels.
#
# (c) 2017 Stephen Longfield, Jr.

import sys

from PIL import Image

usage = 'to_dat.py in.png'

if __name__ == '__main__':
    im = Image.open(sys.argv[1])
    im_grey = im.convert(mode='L')
    pix = im_grey.load()
    for y in range(im_grey.size[1]):
        for x in range(im_grey.size[0]):
            print(pix[x, y])
