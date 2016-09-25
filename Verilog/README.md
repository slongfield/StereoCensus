The Verilog in this directory is currently undergoing a re-write to be more
readable, and better tested (using Verilator).

Rough block diagram of the Census transform stereo vision core:
```        
           _____________     ___________________
           |            |    |                  |
 Camera -> | Linebuffer | -> | Census Transform |
           |____________|    |__________________|   
                                      |
                              ________V__________    _______________
                             |                   |   |              | 
                             | Hamming distances |-->| Index of min |-> out
                             |___________________|   |______________|
                                      ^
           _____________     _________|_________
           |            |    |                  |
 Camera -> | Linebuffer | -> | Census Transform |
           |____________|    |__________________|   
```

All of the interfaces are ready-valid interfaces.
