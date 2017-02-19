#!/bin/bash
# check.sh
# 
# Runs all of the tests.
# Creates some example output in verilog/stereo/generated/gen.png

pushd verilog
# Library of simple primitives.
pushd lib
make clean
make check
popd
# Library of stereo-census related primatives.
pushd census
make clean
make check
popd
# Golden reference model.
pushd model
py.test
popd
# Stereo vision core.
pushd stereo
make clean
make check
popd
popd

