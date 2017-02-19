#!/usr/bin/python3
# from_dat.py
#
# This is the inverse of to_dat.py
#
# (c) 2017 Stephen Longfield, Jr.

usage = 'from_dat.py --width=640 --in=in.dat --out=out.png --scale=2 --offset=40'

import getopt
import numpy as np
import sys

from PIL import Image


def dat_to_img(inp, width, outp, scale, offset):
    vals = []
    line_val = []
    if offset:
        line_val = [0] * offset
    count = offset
    with open(inp) as f:
        for line in f:
            line_val.append(int(line) * scale)
            count += 1
            if count == width:
                count = 0
                vals.append(line_val)
                line_val = []

    im = Image.new('L', (width, len(vals)), (255, 255, 255))
    for y, line in enumerate(vals):
        for x, pixel in enumerate(line):
            im.putpixel((x, y), pixel)
    im.save(outp)


def main(argv):
    scale = 1
    offset = 0
    try:
        opts, args = getopt.getopt(
            argv, 'hw:h:i:o:s:f:', ['help', 'width=', 'height=', 'in=',
                                    'out=', 'scale=', 'offset='])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage)
            sys.exit(2)
        elif opt in ('-w', '--width'):
            width = int(arg)
        elif opt in ('-i', '--in'):
            inp = arg
        elif opt in ('-o', '--out'):
            outp = arg
        elif opt in ('-s', '--scale'):
            scale = int(arg)
        elif opt in ('-f', '--offset'):
            offset = int(arg)
        else:
            pring(usage)
            sys.exit(2)
    dat_to_img(inp, width, outp, scale, offset)

if __name__ == '__main__':
    main(sys.argv[1:])
