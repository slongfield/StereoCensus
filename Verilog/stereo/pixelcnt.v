// pixelcnt takes an input of a pixelclock and a 
// reset typically lineclock, and outputs the 
// current pixel position

`timescale 1us/10ps
module pixelcnt (
	         pixelclock,
	         reset,
	         pixelcount);				  
   
   input pixelclock, reset;

   parameter PIXEL_CNT_DEPTH = 3;

   output reg [PIXEL_CNT_DEPTH:0] pixelcount;
   
   always @(negedge pixelclock or posedge reset) begin
	   if(reset) begin
		   pixelcount <= 0;
	   end else begin
		pixelcount <= pixelcount +1;
		if (reset == 1) begin
	   		pixelcount <= 0;
		end
	   end
   end
endmodule // pixelcnt


module t_pixelcnt;
   reg clock;
   reg reset;
   wire [3:0] pixelcount;

   // device
   pixelcnt DUT(.pixelclock(clock),
                .reset(reset),
                .pixelcount(pixelcount));

   initial clock <= 0;
   always #10 clock = ~clock;

   initial
   begin
      reset <= 0;
      #100;
      reset <= 1;
      #100;
      reset <= 0;
      #100;

      $monitor($time, "%d\n",pixelcount);
   end
      
endmodule
 
