#!/usr/bin/python3
"""from_dat.py

 This is the inverse of to_dat.py

 (c) 2019 Stephen Longfield, Jr."""

import argparse
from PIL import Image


def dat_to_img(inp, width, outp, scale, offset):
    """Transforms a dat file to image using PIL"""
    vals = []
    line_val = []
    if offset:
        line_val = [0] * offset
    count = offset
    with open(inp) as dat_file:
        for line in dat_file:
            line_val.append(int(line) * scale)
            count += 1
            if count == width:
                count = 0
                vals.append(line_val)
                line_val = []

    img = Image.new('L', size=(width, len(vals)), color=255)
    for row, line in enumerate(vals):
        for col, pixel in enumerate(line):
            img.putpixel((col, row), pixel)
    img.save(outp)


def main():
    """Main method."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--width", type=int, help="Expected width of the image")
    parser.add_argument("-t", "--height", type=int, help="Expected height of the image")
    parser.add_argument("-i", "--inp", type=str, help="Input file")
    parser.add_argument("-o", "--outp", type=str, help="Output file")
    parser.add_argument("-s", "--scale", type=int, help="Width scale", default=1)
    parser.add_argument("-f", "--offset", type=int, help="Horizontal offset", default=0)
    args = parser.parse_args()
    dat_to_img(args.inp, args.width, args.outp, args.scale, args.offset)

if __name__ == '__main__':
    main()
