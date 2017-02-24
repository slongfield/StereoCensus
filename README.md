# StereoCensus
Verilog implementation of the census transform stereo vision algorithm.

This is based on work first published as "A parameterized stereo vision core
for FPGAs" By Stephen Longfield and Mark Chang, FCCM09. Any
academic work derived from this code should cite that paper.

As an example, with a maximum disparity of 100, and a window of 19x19 pixels,
this generates the below depth map from the Middlebury Cones dataset (brighter
is closer to the camera):

![Example output](http://i.imgur.com/ejI5MJz.png)

Note that there are more errors around the edges of the image, where there's
less to compare between the image pairs, as well as in areas where the image has
fewer features.

To reproduce, run ```make gen\_test``` in the ```verilog/stereo``` directory. 
