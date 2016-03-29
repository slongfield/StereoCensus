### Python model

`python_census.py` is a Python model of the Census transform stereo algorithm,
useful for evaluating accuracy of a given parameter set.

To run:
<code>python_census.py -l img_left.png -r img_right.png -o img_out.png</code>

It runs with Numpy and Pillow under Python 3
  * Lasted tested working with Numpy v1.10.4, Pillow 1.1.7, Python 2.7.6 or
    Python 3.4.3

`python_census_test.py` are the unit tests, written with py.test
