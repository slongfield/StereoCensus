//Simulated Camera file for stero vision simulation.  Currently supports 1 camera.

// Real Camera looks like this:
// camera (
//      CLOCK_50,                                               //      50 MHz
//      KEY,                                                    //      Pushbutton[3:0]
//      SW,                                                             //      Toggle Switch[17:0]
//      LEDG,                                                   //      LED Green[8:0]
//      //LEDR,                                                 //      LED Red[17:0]
//      GPIO_1,                                                 //      GPIO Connection 1
//      oGray1,
//      oX1,
//      oY1,
//      oGray2,
//      oX2,
//      oY2
//      );

// Only simulating one camera, and ignoring the LEDs/Toggles, since
//   they're for exposure time adjustment which we aren't simulating.
//   Added a reset in Bus Dimentions are the same as they are in the
//   camera

`timescale 1us/10ps
module simcam (
               clock,
               reset,
               oGray,
               lineClock,
               frameClock
               );
   
   input clock,reset;
   
   output reg [9:0] oGray;
   output reg       lineClock, frameClock;

   reg [15:0]       data [0:255];

   reg [10:0]       xMax;
   reg [10:0]       yMax;
   reg [10:0]       oX;
   reg [10:0]       oY;

   parameter INPUTFILE = "../simcam/256.list";

   //buf outputGray (oGray, outPix);

   initial begin
      $readmemh(INPUTFILE,data);
   end

   always @(negedge clock or posedge reset) begin
	   if(reset) begin
		 oX <= 0;
          	 oY <= 0;
     		 xMax <= 15;
      		 yMax <= 15;
         	 lineClock <= 1'b1;
        	 frameClock <= 1'b1;
		 oGray <= data[0];
   	   end else begin
        // $display("simcam: tick\n");

        oGray <= data[oX+oY*(yMax + 1)];

        //Reset the line and Frame clocks if they're set, so we only
        //   get one tick.
        lineClock <= 1'b0;
        frameClock <= 1'b0;

        //Increment X (and possibly Y), and set output to the new value
        oX = oX+1;
        if(oX > xMax) begin
           oX <= 0;
           oY <= oY + 1;
           lineClock <= 1;
           if(oY > yMax) begin
              oX <= 0;
              oY <= 0;
              frameClock <= 1'b1;
           end
        end
     end
     end
endmodule

module t_simcam;
    reg clock;
    reg reset;
    wire [9:0] oGray;
    wire lineClock, frameClock;
    
    simcam DUT(.clock(clock),.reset(reset),
                .oGray(oGray),.lineClock(lineClock),
                .frameClock(frameClock));

    initial clock <= 0;
    always #10 clock = ~clock;

    initial
    begin
        reset <= 0;
        #100;
        reset <= 1;
        #100;
        reset <= 0;
    
        $monitor($time, ": oGray: %d, lineClock %d, frameClock %d\n",
                    oGray, lineClock, frameClock);
    end

endmodule
    
