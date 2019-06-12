import python_census as census

import numpy as np
import pytest
import sys


@pytest.fixture
def census_obj():
    return census.StereoCensus(90)


def test_hamming_distance_same_length(census_obj):
    a = np.array([True, False, False, True])
    b = np.array([False, True, False, True])
    hamming = census_obj.hamming_distance(a, b)
    assert hamming == 2


def test_min_hamming_distance(census_obj):
    census_obj.left_census = np.array([[[True, False, False, False]]])

    census_obj.right_census = ([[[False, False, True, False]],
                                [[True, False, True, True]],
                                [[True, False, True, False]],
                                [[True, True, True, True]]])

    min_index = census_obj.min_hamming_index(0, 0, 4)

    assert min_index == 2


def test_single_census_signature(census_obj):
    a = np.array([[9, 8, 7],
                  [6, 5, 4],
                  [3, 2, 1]])

    b = census_obj.census_signature_one(a)

    assert (b == np.array([True,  True,  True,
                           True,         False,
                           False, False, False])).all()


def test_census_signature(census_obj):
    image_20_20_count = np.reshape(np.linspace(0, 20 * 20 - 1, 20 * 20), (20,
                                                                          20))

    signature_20_20 = np.zeros((2, 2, 360))
    for x in range(2):
        for y in range(2):
            signature_20_20[x][y] = np.array([a > 179 for a in range(360)])

    np.set_printoptions(threshold=sys.maxsize)
    sig = census_obj.census_signature(image_20_20_count)
    assert (sig == signature_20_20).all()


def test_stereo_census(census_obj):
    census_obj.left_img = np.zeros((38, 19))
    census_obj.right_img = np.zeros((38, 19))

    # Deterministic random feature to search for
    np.random.seed(12345)
    feature = np.random.rand(19, 19)

    census_obj.left_img[0:19, 0:19] = feature
    census_obj.right_img[10:29, 0:19] = feature

    census_obj.stereo_census()

    assert census_obj.disparities[0, 0] == 10
