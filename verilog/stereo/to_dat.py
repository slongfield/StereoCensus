#!/usr/bin/python3
# to_dat.py
#
# Opens an image, and then writes out the values of the pixels.

import sys

from PIL import Image

usage = 'to_dat.py in.png'

if __name__ == '__main__':
    im = Image.open(sys.argv[1])
    im_grey = im.convert(mode='L')
    print im_grey.size()
