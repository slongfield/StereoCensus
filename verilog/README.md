This directory contains a Verilog implementation of a very simple stereo vision
core without flow control, based on the census transform.

Rough block diagram of the census transform stereo vision core:
```        
           _____________     ___________________   ______________
           |            |    |                  |  |             |
 Camera -> | Linebuffer | -> | Census Transform |->| Tapped FIFO |
           |____________|    |__________________|  |_____________|
                                                     ||||||||||||
           _____________     ___________________    _VVVVVVVVVVVV_
           |            |    |                  |  |              |
 Camera -> | Linebuffer | -> | Census Transform |->|     XORs     |
           |____________|    |__________________|  |______________|
                                                          |
                                                  ________V__________ 
                                                 |                   |
                                                 | Pouplation counts |
                                                 |___________________| 
                                                          |
                                                    ______V________
                                                    |              | 
                                                    |    Argmin    |-> out
                                                    |______________|
```

The lib/ directory contains generic buffers, tapped fifos, and fifo elements, and
the census/ directory contains more specific processing elements, or generators
for those elements, as needed.

'make check_stereo' in this directory will generate a simple stereo vision census core,
and test it agains the python golden reference model, using the test and
generation utilities in the test/ directory. 

'make check' will run the unit tests from each of the subdirectories.
