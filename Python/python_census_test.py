import python_census as census

import numpy as np
import pytest


def test_hamming_distance_same_length():
    a = np.array([True, False, False, True])
    b = np.array([False, True, False, True])
    hamming = census.hamming_distance(a, b)
    assert hamming == 2


def test_min_hamming_distance():
    a = np.array([True, False, False, False])

    a_dist1 = np.array([True, False, True, False])
    a_dist2 = np.array([True, False, True, True])
    a_dist2b = np.array([False, False, True, False])
    a_dist3 = np.array([True, True, True, True])

    min_index = census.min_hamming_index(a, [a_dist2, a_dist2b, a_dist1,
                                             a_dist3])

    assert min_index == 2


def test_single_census_signature():
    a = np.array([[9, 8, 7],
                  [6, 5, 4],
                  [3, 2, 1]])

    b = census.census_signature_one(a)

    assert (b == np.array([True,  True,  True,
                           True,         False,
                           False, False, False])).all()


def test_census_signature():
    image_20_20_count = np.reshape(np.linspace(0, 20 * 20 - 1, 20 * 20), (20,
                                                                          20))

    signature_20_20 = np.zeros((2, 2, 360))
    for x in range(2):
        for y in range(2):
            signature_20_20[x][y] = np.array([a > 179 for a in range(360)])

    np.set_printoptions(threshold=np.nan)
    sig = census.census_signature(image_20_20_count)
    assert (sig == signature_20_20).all()


def test_stereo_census():
    left = np.zeros((38, 19))
    right = np.zeros((38, 19))

    # Deterministic random feature to search for
    np.random.seed(12345)
    feature = np.random.rand(19,19)

    left[0:19, 0:19] = feature
    right[10:29, 0:19] = feature

    stereo = census.stereo_census(left, right)

    assert stereo[0, 0] == 10
