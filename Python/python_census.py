#!/usr/bin/python
# python_census.py
#
# Implementation of the census transform stereo vision algorithm using Numpy.
# Reads in two images using the Python Imaging Library, computes the stereo for
# each pixel using the census transform, and outputs the computed
#
# Usage:
#   python_census.py -left=img_L.png -right=img_R.png -out=out.png
# TODO(slongfield)
#   Optional options:
#       -window_height -- height of the census window in pixels
#       -window_width  -- width of the census window in pixels
#       -max_disparity -- maximum value for the census disparity
#       -disparity_scale -- how much to scale the disparity by when saving
#   Currently, the window size is fixed at 19x19, the max disparity is 100, and
#   the disparity scale is 2.
#
# (c) 2016 Stephen Longfield, Jr.

import getopt
import numpy as np
import sys

from PIL import Image

usage = 'python --left=img_L.png --right=img_R.png -out=out.png'


def load_image_greyscale(file_name):
    """Load an image from a file

    Uses PIL to load an image from a file, convert it to greyscale, and then 
    returns an 2d np array.

    args:
        file_name: File name containing image of interest

    returns:
        array: 2d np.array of values

    raises:
        IOError: the file cannot be opened
    """
    im = Image.open(file_name)
    im_grey = im.convert(mode='L')
    im_array = np.asarray(im_grey)

    # Convert from column-major to row-major
    return np.transpose(im_array, (1, 0))


def write_image(img, file_name):
    """Write an image out to a file.

    args:
        img: a 2d numpy array 

    raises:
        IOError: the file cannot be opened
    """

    # Convert from row-major to column-major
    img_column = np.transpose(img, (1, 0))
    img_scaled = img_column * 2

    im = Image.fromarray(img_scaled)

    im_grey = im.convert(mode='L')

    im_grey.save(file_name)


def census_signature_one(array):
    """Computes a single census signature.

    Takes in an NxM 2d np array, and compares each element in the array to
    the central element, producing a list of Booleans--true when that element
    is greater than the center pixel, false when it is smaller. This list does
    not include the original center pixel.

    args:
        array: NxM 2d np.array of numbers

    returns:
        signature: NxM-1 long 1d np.array of Booleans 
    """
    center_pos = (np.shape(array)[0] // 2, np.shape(array)[1] // 2)
    center_val = array[center_pos[0], center_pos[1]]

    signature = array > center_val

    mask = np.ones(signature.shape, dtype=np.bool)
    mask[center_pos] = False

    return signature[mask]


def census_signature(img):
    """Compute the census signature for each position in the image.

    args:
        img: 2d np.array of numbers

    returns:
        census_img: 3d np.array, where the first two dimensions are equal equal
        to the input img dimensions shrunk by the window size (19x19), and the
        third dimension is 1 less that area.
    """

    (x_size, y_size) = np.shape(img)

    census_img = np.zeros((x_size - 19 + 1, y_size - 19 + 1, 19 * 19 - 1))

    for x in range(x_size - 19 + 1):
        for y in range(y_size - 19 + 1):
            census_img[x, y] = census_signature_one(img[x:x + 19, y:y + 19])

    return census_img


def hamming_distance(a, b):
    """Compute the Hamming distance between two np.arrays."""
    return sum(np.not_equal(a, b))


def min_hamming_index(ref, candidates):
    """Finds the index of the candidate list that has the minimum Hamming
    distance from the reference.

    args:
        ref: reference census signature
        candidates: 1d np.array of booleans

    returns:
        index: (int) index of the candidate with the minimum hamming distance
    """
    min_val = hamming_distance(ref, candidates[0])
    min_index = 0
    for i, c in enumerate(candidates[1:]):
        c_val = hamming_distance(ref, c)
        if c_val < min_val:
            min_val = c_val
            min_index = i + 1
    return min_index


def stereo_census(left_img, right_img):
    """Compute the census stereo vision algorithm.

    args:
        left_img: a 2d np.array representing the left image
        right_img: a 2d np.array representing the right image, with the same
        dimensions as left_img.

    returns:
        stereo: a 2d np.array of the same dimentions as the input images.

    raises:
        ValueError: if the images are not the same size
    """
    if np.shape(left_img) != np.shape(right_img):
        raise ValueError("Image dimensions must be equal")

    left_census = census_signature(left_img)
    right_census = census_signature(right_img)
    left_shape = np.shape(left_census)
    stereo = np.zeros((left_shape[0], left_shape[1]))
    for y in range(np.shape(stereo)[1]):
        print("Processing line %d of %d" % (y, np.shape(stereo)[1]), end='\r')
        for x in range(np.shape(stereo)[0]):
            stereo[x, y] = min_hamming_index(left_census[x, y],
                                             right_census[x:x + 100, y])
    return stereo


def main(argv):
    left = None
    right = None
    out = None
    try:
        opts, args = getopt.getopt(
            argv, 'hl:r:o:', ['help', 'left=', 'right=', 'out='])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage)
            sys.exit(2)
        elif opt in ('-l', '--left'):
            left = arg
        elif opt in ('-r', '--right'):
            right = arg
        elif opt in ('-o', '--out'):
            out = arg
    if left is None or right is None or out is None:
        print(usage)
        sys.exit(2)

    try:
        left_img = load_image_greyscale(left)
        right_img = load_image_greyscale(right)
        disparities = stereo_census(left_img, right_img)
        write_image(disparities, out)
    except IOError as e:
        print("Failed: %s: %s" % (e.strerror, e.filename))
    except ValueError as e:
        print("Failed: %s" % (e.strerror))


if __name__ == '__main__':
    main(sys.argv[1:])
