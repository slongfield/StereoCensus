#!/usr/bin/python3
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
#   Currently, the window size is fixed at 19x19, the max disparity is 100, and
#   the disparity scale is 2.
#
# (c) 2016 Stephen Longfield, Jr.

import getopt
import numpy as np
import sys

from PIL import Image

usage = 'python_census.py --left=img_L.png --right=img_R.png -out=out.png'


class StereoCensus(object):
    """Computes the census transform algorithm for stereo vision."""

    def __init__(self, max_disparity=100, disparity_scale=2):
        self.left_img = None
        self.right_img = None
        self.max_disparity = max_disparity
        self.disparity_scale = disparity_scale

    def load_image_greyscale(self, file_name):
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

    def load_images(self, left_file, right_file):
        """Loads images from files.

        Args:
            left_file: File to load the left image from
            right_file: File to load the right image from

        raises:
            IOError: if the files cannot be opened
            ValueError: if the images are not the same size
        """
        self.left_img = self.load_image_greyscale(left_file)
        self.right_img = self.load_image_greyscale(right_file)
        if np.shape(self.left_img) != np.shape(self.right_img):
            raise ValueError("Image dimensions must be equal")

    def write_image(self, file_name):
        """Write the computed disparities out to a file.

        args:
            img: a 2d numpy array

        raises:
            IOError: the file cannot be opened
        """

        # Convert from row-major to column-major
        img_column = np.transpose(self.disparities, (1, 0))
        img_scaled = img_column * self.disparity_scale

        im = Image.fromarray(img_scaled)

        im_grey = im.convert(mode='L')

        im_grey.save(file_name)

    def census_signature_one(self, array):
        """Computes a single census signature.

        Takes in an NxM 2d np array, and compares each element in the array to
        the central element, producing a list of Booleans--true when that
        element is greater than the center pixel, false when it is smaller. This
        list does not include the original center pixel.

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

    def census_signature(self, img):
        """Compute the census signature for each position in the image.

        args:
            img: 2d np.array of numbers

        returns:
            census_img: 3d np.array, where the first two dimensions are equal
            equal to the input img dimensions shrunk by the window size (19x19),
            and the third dimension is 1 less that area.
        """

        (x_size, y_size) = np.shape(img)

        census_img = np.zeros((x_size - 19 + 1, y_size - 19 + 1, 19 * 19 - 1))

        for x in range(x_size - 19 + 1):
            for y in range(y_size - 19 + 1):
                census_img[x, y] = self.census_signature_one(
                    img[x:x + 19, y:y + 19])

        return census_img

    def hamming_distance(self, a, b):
        """Compute the Hamming distance between two np.arrays."""
        return np.count_nonzero(a != b)

    def min_hamming_index(self, x, y, search_width):
        """Finds the index of the candidate list that has the minimum Hamming
        distance from the reference.

        args:
            x: starting x coordinate
            y: starting y coordinate
            search_width: how far to the right to search

        returns:
            index: (int) index of the candidate with the minimum hamming
              distance
        """
        min_val = self.hamming_distance(self.left_census[x][y],
                                        self.right_census[x][y])
        min_index = 0
        max_x = np.shape(self.right_census)[0]
        for i, x_check in enumerate(range(x + 1, x + search_width + 1)):
            if x_check >= max_x:
                break
            c_val = self.hamming_distance(self.left_census[x][y],
                                          self.right_census[x_check][y])
            if c_val < min_val:
                min_val = c_val
                min_index = i + 1
        return min_index

    def stereo_census(self):
        """Compute the census stereo vision algorithm.

        Assumes that left_img and right_img have already been loaded.

        returns:
            stereo: a 2d np.array of the same dimentions as the input images.
        """

        self.left_census = self.census_signature(self.left_img)
        self.right_census = self.census_signature(self.right_img)

        left_shape = np.shape(self.left_census)
        self.disparities = np.zeros((left_shape[0], left_shape[1]))
        for y in range(np.shape(self.disparities)[1]):
            print("Processing line %d of %d" %
                  (y, np.shape(self.disparities)[1]), end='\r')
            for x in range(np.shape(self.disparities)[0]):
                self.disparities[x, y] = (
                    self.min_hamming_index(x, y,
                                           self.max_disparity))


def main(argv):
    left = None
    right = None
    out = None
    max_disparity = 100
    try:
        opts, args = getopt.getopt(
            argv, 'hl:r:o:m:', ['help', 'left=', 'right=', 'out=',
                                "max_disparity="])
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
        elif opt in ('-m', '--max_disparity'):
            if arg.isdigit():
                max_disparity = int(arg)
        else:
            print(usage)
            sys.exit(2)
    if left is None or right is None or out is None:
        print(usage)
        sys.exit(2)

    try:
        stereo = StereoCensus(max_disparity=max_disparity)
        stereo.load_images(left, right)
        stereo.stereo_census()
        stereo.write_image(out)
    except IOError as e:
        print("Failed: %s: %s" % (e.strerror, e.filename))
    except ValueError as e:
        print("Failed: %s" % (e.strerror))


if __name__ == '__main__':
    main(sys.argv[1:])
