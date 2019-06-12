#!/bin/bash
# check.sh
#
# Runs all of the tests.
# Creates some example output in verilog/stereo/generated/gen.png
set -e
pushd verilog
# Set up the Python environment.
make venv
. venv/bin/activate
# Test library of simple primitives.
pushd lib
make clean
make check
popd
# Test library of stereo-census related primitives.
pushd census
make clean
make check
popd
# Test golden reference model.
pushd model
py.test
popd
# Test stereo vision core.
pushd stereo
make clean
make check
popd
deactivate
make clean
popd
