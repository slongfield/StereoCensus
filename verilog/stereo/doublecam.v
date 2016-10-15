`timescale 1us/10ps
module doublecam (
	clock,
	lreset,
	loGray,
	llineClock,
	lframeClock,
	
	rreset,
	roGray,
	rlineClock,
	rframeClock
	);

	input clock, lreset, rreset;

	output [9:0] loGray, roGray;
	
	output llineClock, rlineClock, lframeClock, rframeClock;

	parameter LEFTFILE = "256.list";
	parameter RIGHTFILE = "512.list";

	simcam #(.INPUTFILE(LEFTFILE)) lCam(clock, lreset, loGray, llineClock, lframeClock);
	simcam #(.INPUTFILE(RIGHTFILE)) rCam(clock, rreset, roGray, rlineClock, rframeClock);

endmodule


module t_doublecam;
    reg clock;
    reg reset;
    wire [9:0] l_pixel, r_pixel;
    wire l_lineClock, r_linClock, l_frameClock, r_frameClock;
    
    doublecam DUT(.clock(clock),.lreset(reset),.rreset(reset),
                .loGray(l_pixel),.llineClock(l_lineClock),.lframeClock(l_frameClock),
                .roGray(r_pixel),.rlineClock(r_lineClock),.rframeClock(r_frameClock));

    initial clock <= 0;
    always #10 clock = ~clock;

    initial
    begin
        reset <= 0;
        #100;
        reset <= 1;
        #100;
        reset <= 0;
    
        $monitor($time, ": l: %d, ll %d, lf %d | r: %d, rl %d, rf %d\n",
                    l_pixel, l_lineClock, l_frameClock,
                    r_pixel, r_lineClock, r_frameClock);
    end

endmodule
    