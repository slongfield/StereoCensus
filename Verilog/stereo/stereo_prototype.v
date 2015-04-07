// Stereo Module - Prototype, will be made into generateable verilog
//
// Stephen Longfield Dec 15, 2008

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
	.oData
  );

// ******************************* Parameters ********************************

// This is the place where these parameters are set.  Will be set upon
// generation of the module.
// Will also be used to overload the test values in lower-level modules.

// Number of bits (minus 1) needed to store pixel data
parameter PIXEL_DEPTH = 18;  	
// How many bits (minus 1) needed to store number of pixels per line 
// 	(log2(PIXELS_PER_LINE+1)-1)
parameter PX_CNT_DEPTH = 9;
// How many bits (minus 1) needed to store the number of lines per frame
// 	 (log2(LINES_PER_FRAME+1)-1)
parameter LINE_CNT_DEPTH = 9;	
// How many pixels (minus 1) per line
parameter PIXELS_PER_LINE = 499;
// How many pixels (minus 1) per line
parameter LINES_PER_FRAME = 499;
// Total number of pixels (minus 1)
parameter TOTAL_PIXELS = 249999;
// How many pixles (minus 1) on each side of the hamming blocka
parameter HAMMING_BLOCK_SIZE = 12; // How many total pixels (minus 1) in each 
//	hamming block (HAMMING_BLOCK_SIZE+1)^2-2
parameter HAMMING_TOTAL_SIZE = 167;
// Number of bits (minus 1) needed to store the hamming block 
// 	(log2(HAMMING_TOTAL_SIZE+1)-1)
parameter HAMMING_DEPTH = 9;	
// Maximum dispartiy value (minus 1)
parameter MAX_DISPARITY = 19;
// How many bits (minus 1) needed to store MAX_DISPARITY 
// 	(log2(DISPARITY_DEPTH+1)-1;
parameter DISPARITY_DEPTH = 4;	

// Configure the inputs and outputs

input pxclk;
input reset;

input wire [PIXEL_DEPTH:0] iGrayR;
input wire [PIXEL_DEPTH:0] iGrayL;
input wire iHref;
input wire iVsync;

output reg [DISPARITY_DEPTH:0] oData;

// Registers and wires
wire [PX_CNT_DEPTH:0] lPxCount, rPxCount;
wire [PIXEL_DEPTH:0] lColOut [0:HAMMING_BLOCK_SIZE];
wire [PIXEL_DEPTH:0] rColOut [0:HAMMING_BLOCK_SIZE];
wire lLineEnable [0:HAMMING_BLOCK_SIZE];
wire rLineEnable [0:HAMMING_BLOCK_SIZE];
wire [PIXEL_DEPTH:0] lLinesOut [0:HAMMING_BLOCK_SIZE];
wire [PIXEL_DEPTH:0] rLinesOut [0:HAMMING_BLOCK_SIZE];
wire [HAMMING_TOTAL_SIZE:0] lHamming, rHamming;

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

// Need to generate the connections from lColOut and rColOut to inputs
 
hamReg2 #(.PIXEL_DEPTH(PIXEL_DEPTH), .BOX_WIDTH(HAMMING_BLOCK_SIZE+1)) lHamReg(.clk(pxclk), .reset(reset), .inputs({lColOut[0],lColOut[1],lColOut[2],lColOut[3],lColOut[4],lColOut[5],lColOut[6],lColOut[7],lColOut[8],lColOut[9],lColOut[10],lColOut[11],lColOut[12]}), .he(1'b1), .hamOut(lHamming));

hamReg2 #(.PIXEL_DEPTH(PIXEL_DEPTH), .BOX_WIDTH(HAMMING_BLOCK_SIZE+1)) rHamReg(.clk(pxclk), .reset(reset), .inputs({rColOut[0],rColOut[1],rColOut[2],rColOut[3],rColOut[4],rColOut[5],rColOut[6],rColOut[7],rColOut[8],rColOut[9],rColOut[10],rColOut[11],rColOut[12]}), .he(1'b1), .hamOut(rHamming));

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
