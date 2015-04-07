import datetime
import sys
import math
from gen_MinDistance4 import *

def genStereo(pixelDepth, pixelsPerLine, linesPerFrame, hammingBlockSize, maxDisparity):
    """Generates stereo.v, stereo_test.v, and mindistance4.v.  Other files are in the stereo folder already."""

    # Generate the other needed parameters

    pxCountDepth = int(math.ceil(math.log(float(pixelsPerLine),2)))
    lineCountDepth = int(math.ceil(math.log(float(linesPerFrame),2)))
    totalPixels = pixelsPerLine*linesPerFrame
    hammingTotalSize = hammingBlockSize**2
    hammingDepth = int(math.ceil(math.log(float(hammingTotalSize),2)))
    disparityDepth = int(math.ceil(math.log(float(maxDisparity),2)))

    stereoOut = open("stereo/stereo.v", 'w')

    stereoOut.write("""// Stereo Module
//
// Stephen Longfield Dec 15, 2008
""")
    stereoOut.write("// Generated fresh on " + str(datetime.date.today()) + "\n\n")

    stereoOut.write("""
module stereo(
	// Clock and Reset
	pxclk,
	reset,

	// Input grayscale data
	iGrayR,
	iGrayL,

	// Input Horizonal and vertical synching signals. 
	//   Left and right camera should be externally syncronized
	iHref,
	iVsync,

	// Output Disparity data
	oData
  );

// ******************************* Parameters ********************************

// This is the place where these parameters are set.  Will be set upon
// generation of the module.
// Will also be used to overload the test values in lower-level modules.""")

    stereoOut.write("""
// Number of bits (minus 1) needed to store pixel data
parameter PIXEL_DEPTH = """ + str(pixelDepth-1) + """;  	
// How many bits (minus 1) needed to store number of pixels per line 
// 	(log2(PIXELS_PER_LINE+1)-1)
parameter PX_CNT_DEPTH = """ + str(pxCountDepth-1) + """;
// How many bits (minus 1) needed to store the number of lines per frame
// 	 (log2(LINES_PER_FRAME+1)-1)
parameter LINE_CNT_DEPTH = """ + str(lineCountDepth) + """;	
// How many pixels (minus 1) per line
parameter PIXELS_PER_LINE = """ + str(pixelsPerLine-1) + """;
// How many pixels (minus 1) per line
parameter LINES_PER_FRAME = """ + str(linesPerFrame-1) + """;
// Total number of pixels (minus 1)
parameter TOTAL_PIXELS = """ + str(totalPixels-1)+ """;
// How many pixles (minus 1) on each side of the hamming block
parameter HAMMING_BLOCK_SIZE = """ + str(hammingBlockSize-1) + """; // How many total pixels (minus 1) in each 
//	hamming block (HAMMING_BLOCK_SIZE+1)^2-2
parameter HAMMING_TOTAL_SIZE = """ + str(hammingTotalSize-2) + """; 
// Number of bits (minus 1) needed to store the hamming block 
// 	(log2(HAMMING_TOTAL_SIZE+1)-1)
parameter HAMMING_DEPTH = """ + str(hammingDepth-1) + """;	
// Maximum dispartiy value (minus 1)
parameter MAX_DISPARITY = """ + str(maxDisparity-1) + """;
// How many bits (minus 1) needed to store MAX_DISPARITY 
// 	(log2(DISPARITY_DEPTH+1)-1;
parameter DISPARITY_DEPTH = """ + str(disparityDepth-1) + """;""")

    # A bit more code that doesn't need any generation...

    stereoOut.write("""
// Configure the inputs and outputs

input pxclk;
input reset;

input wire [PIXEL_DEPTH:0] iGrayR;
input wire [PIXEL_DEPTH:0] iGrayL;
input wire iHref;
input wire iVsync;

output wire [DISPARITY_DEPTH:0] oData;

// Registers and wires
wire [PX_CNT_DEPTH:0] lPxCount, rPxCount;
wire [PIXEL_DEPTH:0] lColOut [0:HAMMING_BLOCK_SIZE];
wire [PIXEL_DEPTH:0] rColOut [0:HAMMING_BLOCK_SIZE];
wire lLineEnable [0:HAMMING_BLOCK_SIZE];
wire rLineEnable [0:HAMMING_BLOCK_SIZE];
wire [PIXEL_DEPTH:0] lLinesOut [0:HAMMING_BLOCK_SIZE];
wire [PIXEL_DEPTH:0] rLinesOut [0:HAMMING_BLOCK_SIZE];
wire [HAMMING_TOTAL_SIZE:0] lHamming, rHamming;
reg [PIXEL_DEPTH:0] lBuffer, rBuffer;
reg [LINE_CNT_DEPTH:0] lLine, rLine;

// Instantiations

pixelcnt #(.PIXEL_CNT_DEPTH(PX_CNT_DEPTH)) lPixelCount (.pixelclock(pxclk),
       		.reset(~iHref|reset), .pixelcount(lPxCount));

pixelcnt #(.PIXEL_CNT_DEPTH(PX_CNT_DEPTH)) rPixelCount (.pixelclock(pxclk),
       		.reset(~iHref|reset), .pixelcount(rPxCount));

genvar k;
generate 
	for(k=0;k<HAMMING_BLOCK_SIZE+1;k=k+1) begin :LINES
		singleLine #(.PIXEL_DEPTH(PIXEL_DEPTH), 
			.ADDR_WIDTH(PX_CNT_DEPTH)) lLineRam2(
			.clk(pxclk),
			.addr(lPxCount),
			.datain(iGrayL),
			.re(~lLineEnable[k]),
			.oData(lLinesOut[k])
		);	

		singleLine #(.PIXEL_DEPTH(PIXEL_DEPTH), 
			.ADDR_WIDTH(PX_CNT_DEPTH)) rLineRam0(
			.clk(pxclk),
			.addr(rPxCount),
			.datain(iGrayR),
			.re(~rLineEnable[k]),
			.oData(rLinesOut[k])
		);
	end
endgenerate
""")

    # Generate the hamReg connections from [l|r]ColOut to inputs, as the inputs
    #   array is simply a concatination of all of the [l|r]ColOut lines

    # lHamReg
    stereoOut.write("hamReg2 #(.PIXEL_DEPTH(PIXEL_DEPTH), .BOX_WIDTH(HAMMING_BLOCK_SIZE+1)) lHamReg(.clk(pxclk), .reset(reset), .inputs({")

    for i in range(hammingBlockSize):
        if(i != hammingBlockSize-1):
            stereoOut.write("lColOut[" + str(i) + "],")
        else:
            stereoOut.write("lColOut[" + str(i) + "]")

    stereoOut.write("}), .he(1'b1), .hamOut(lHamming));\n")

    # rHamReg
    stereoOut.write("\n");
    stereoOut.write("hamReg2 #(.PIXEL_DEPTH(PIXEL_DEPTH), .BOX_WIDTH(HAMMING_BLOCK_SIZE+1)) rHamReg(.clk(pxclk), .reset(reset), .inputs({")

    for i in range(hammingBlockSize):
        if(i != hammingBlockSize-1):
            stereoOut.write("rColOut[" + str(i) + "],")
        else:
            stereoOut.write("rColOut[" + str(i) + "]")

    stereoOut.write("}), .he(1'b1), .hamOut(rHamming));\n")

    stereoOut.write("""

mindistance4 #(.HAMMING_TOTAL_SIZE(HAMMING_TOTAL_SIZE), .HAMMING_DEPTH(HAMMING_DEPTH), .MAX_DISPARITY(MAX_DISPARITY), .DISPARITY_DEPTH(DISPARITY_DEPTH)) md4 (.clk(pxclk), .reset(reset), .lham(lHamming), .rham(rHamming), .dout(oData));


// ********************* Combinatorial Logic ************************

//Routing system for data from lineRams into the colums

// The bottom element is always the most recently acquired one
assign rColOut[HAMMING_BLOCK_SIZE] = rBuffer;
assign lColOut[HAMMING_BLOCK_SIZE] = lBuffer;

genvar i,j;
generate
	for(i=0; i<HAMMING_BLOCK_SIZE+1; i=i+1) begin :ENABLES
		assign lLineEnable[i] = ((lLine%(HAMMING_BLOCK_SIZE+1))==i);
		assign rLineEnable[i] = ((rLine%(HAMMING_BLOCK_SIZE+1))==i);
		for(j=0; j<HAMMING_BLOCK_SIZE; j=j+1) begin :INNER
			// A kind of shift register, relative to i and j.  For
			// DBS+1 = 4:
			// j i  0  1  2  3
			// 0    1  2  3  0
			// 1    2  3  0  1
			// 2    3  0  1  2
			// In   0  1  2  3
			// This represents the order in which the blockrams
			// are connected to the output column.  The last
			// element in the column is always the newest pixel.
			//
			bufif1 r[PIXEL_DEPTH:0] (rColOut[j],rLinesOut[(i+j+1)%(HAMMING_BLOCK_SIZE+1)],rLineEnable[i]);
			bufif1 l[PIXEL_DEPTH:0] (lColOut[j],lLinesOut[(i+j+1)%(HAMMING_BLOCK_SIZE+1)],lLineEnable[i]);
		end
	end
endgenerate

// Data buffers... data comes in on falling clock edge, but we want to use it
// on the positive clock edge
always @(posedge pxclk or posedge reset) begin
	if(reset) begin
		lBuffer <= 0;
		rBuffer <= 0;
	end else begin
		lBuffer <= iGrayL;
		rBuffer <= iGrayR;
	end
end

// New linecounter mode... could/should be put into a module of its own?
always @(negedge iHref or posedge reset) begin
	if(reset) begin
		lLine <= 0;
	end else begin
		if(~iVsync) begin
			lLine <= lLine + 1;
		end else begin
			lLine <= 0;
		end
	end
end

always @(negedge iHref or posedge reset) begin
	if(reset) begin
		rLine <= 0;
	end else begin
		if(~iVsync) begin
			rLine <= rLine + 1;
		end else begin
			rLine <= 0;
		end
	end
end


endmodule""")
        
    stereoOut.close()

    # Whoo!  Generated the stereo file!  Now generate minDistance4

    gen_MinDistance4(hammingTotalSize,hammingDepth,maxDisparity,disparityDepth,"stereo/mindistance4.v")

    # Wow, that was easy.  Generate the test file.

    stereoTestOut = open("stereo_test.v", 'w')

    # Generating as one big block.
    # Some comments:
    #   Don't have a good way to do a leftfile and right file input, since that
    #   might not always be needed

    stereoTestOut.write("""// Stereo_test module
//
// Stephen Longfield Dec 15, 2008
// Generated fresh on """ + str(datetime.date.today()) + """\n\n

module stereo_test;

// Insert parameters while generating.  Not a full list of parameters
 
parameter LEFTFILE = "left.list";
parameter RIGHTFILE = "right.list";
parameter PIXEL_DEPTH = """ + str(pixelDepth-1) + """;
parameter PIXELS_PER_LINE = """ + str(pixelsPerLine-1) + """;
parameter LINES_PER_FRAME = """ + str(linesPerFrame-1) + """;
parameter TOTAL_PIXELS = """ + str(totalPixels-1) + """;
parameter PX_CNT_DEPTH = """ + str(pxCountDepth-1) + """;
parameter LINE_CNT_DEPTH = """ + str(lineCountDepth-1) + """;
parameter DISPARITY_DEPTH = """ + str(disparityDepth-1) + """;		

// Registers and wires
reg pxclk;
reg reset;
wire [PIXEL_DEPTH:0] lData;
wire [PIXEL_DEPTH:0] rData;
wire [DISPARITY_DEPTH:0] disparity;
wire lHref, rHref, Href;
wire lVsync, rVsync, Vsync;
integer oFile;

// Combinatorial
// These are only somewhat valid... valid since lCam and rCam are always
// 	synced.  Would not work if they weren't.  Solution: Buffer one of them
assign Vsync = lVsync | rVsync;
assign Href = lHref | rHref;


// Cameras

simcam2 #(.PIXEL_DEPTH(PIXEL_DEPTH), .INPUTFILE(LEFTFILE), 
	  .TOTAL_PIX(TOTAL_PIXELS), .PIX_PER_LINE(PIXELS_PER_LINE) ,
  	  .PIX_PER_LINE_DEPTH(PX_CNT_DEPTH), .LINES_PER_FRAME(LINES_PER_FRAME),
  	  .LINES_PER_FRAME_DEPTH(LINE_CNT_DEPTH)) lCam(.pxclk(pxclk),
	  .reset(reset), .oData(lData), .href(lHref), .vsync(lVsync));

simcam2 #(.PIXEL_DEPTH(PIXEL_DEPTH), .INPUTFILE(RIGHTFILE), 
	  .TOTAL_PIX(TOTAL_PIXELS), .PIX_PER_LINE(PIXELS_PER_LINE) ,
  	  .PIX_PER_LINE_DEPTH(PX_CNT_DEPTH), .LINES_PER_FRAME(LINES_PER_FRAME),
  	  .LINES_PER_FRAME_DEPTH(LINE_CNT_DEPTH)) rCam(.pxclk(pxclk),
	  .reset(reset), .oData(rData), .href(rHref), .vsync(rVsync));

// Connect to a stereo generated at the same time as this stereo_test module,
// or there could be parameter mismatch.
//
// Would not work to overload parameters here, as there is actually some code
// difference as well.

stereo stereo(	.pxclk(pxclk),
		.reset(reset),
		.iGrayR(rData),
		.iGrayL(lData),
		.iHref(Href),
		.iVsync(Vsync),
		.oData(disparity)
);


// ******* test *********

initial pxclk <= 0;
always #20 pxclk = ~pxclk;

initial oFile = $fopen("out.list");

initial
begin
	reset <= 0;
	#100
	reset <= 1;
	#100
	reset <= 0;
end

// Always outputs the data to a file.  Could be done a bit better.  For
// example, only after reset has gone low, or something.  meh.
always @(posedge pxclk) begin
	$fdisplay(oFile,"%d\\n",disparity);
end
endmodule""")


if __name__ == "__main__":
    genStereo(16, 384, 288, 15, 15)    
