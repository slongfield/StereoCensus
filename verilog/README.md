This directory contains a Verilog implementation of a very simple stereo vision
core without flow control, based on the census transform.

Rough block diagram of the census transform stereo vision core:
```        
            ____________      __________________    _____________
           |            |    |                  |  |             |
 Camera -> | Linebuffer | -> | Census Transform |->| Tapped FIFO |
           |____________|    |__________________|  |_____________|
                                                     ||||||||||||
            ____________      __________________    _VVVVVVVVVVVV_
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

The stereo/ directory contains the generators and simple tests for the stereo
vision core.
