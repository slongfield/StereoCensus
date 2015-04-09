/*
 `include "doublecam.v"
 `include "pixelcnt.v"
 `include "singleLine.v"
 `include "hamReg.v"
 */
`timescale 1us/10ps
module test();
   wire [9:0] lGray, rGray;
   wire [3:0] rpcnt, lpcnt;
   wire       lLine, rLine;
   wire       lFrame, rFrame;
   reg        reset, pxclk;
   wire [1:0] disparity;
   wire       valid;

   initial pxclk <= 0;
   always #10 pxclk <= ~pxclk;

   

   initial begin
      reset <= 1;	
      #111
      reset <= 0;
   end

   // Instantiate a camera
   doublecam #(.RIGHTFILE("box1.list"), 
               .LEFTFILE("box0.list")) dcam(
	                                   pxclk, 
                                           reset, 
                                           rGray, 
                                           rLine,
                                           rFrame,
                                           reset,
                                           lGray,
                                           lLine, 
                                           lFrame);
   
   // Count what pixel we're currently on
   pixelcnt rpcount( pxclk, rLine, rpcnt);
   pixelcnt lpcount( pxclk, lLine, lpcnt);

   stereo2 stereo(
		 .pxclk(pxclk),
		 .reset(reset),
		 .lGrey(lGray),
		 .rGrey(rGray),
		 .disparity(disparity),
		 .valid(valid)
	         );

   initial begin
      $monitor($time, ": LEFT %d RIGHT %d, LEFT_HAM %d RIGHT_HAM %d, DISPARITY %d",
               lGray,rGray,stereo.lHammingOut,stereo.rHammingOut,disparity);
   end 

   initial
   #5200 //$writememh("out.list",outdata);
     $stop;
   
endmodule
