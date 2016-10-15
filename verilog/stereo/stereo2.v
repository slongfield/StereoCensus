// Second revision of the stereo vision module.


`timescale 1us/10ps

module stereo2 (
	pxclk,
	reset,
	lGrey, //PIXEL_DEPTH
	rGrey,
	disparity, 	// The output disparity.. Should be DISPARITY_DEPTH size
	valid				// If the disparity is valid
);

// ********************** Parameters  *******************************

parameter NUM_LINES = 3; // Number of lines to keep track of
parameter PIXEL_DEPTH = 9;   // How many bits (minus 1) to store the pixel data
parameter PX_CNT_DEPTH = 3;  // How many bits (minus 1) to store the number of pixels per line
parameter LINE_CNT_DEPTH = 3; // How many bits (minus 1) to store the number of lines per frame
parameter DISPARITY_DEPTH = 1; // How many bits (minus 1) to store the disparity.
parameter PIXELS_PER_LINE = 15; // How many pixels (minus 1) in one line
parameter LINES_PER_FRAME = 15; // How many lines (minus 1) in one frame
parameter DISPARITY_BLOCK_SIZE = 2; // Disparity block dimension (minus 1).  Assumes square.
parameter HAMMING_SIZE = 7; // Hamming size (minus 1).  Is the DISPARITY_BLOCK_SIZE plus 1, squared, and then minus 1.
parameter MAX_DISPARITY = 4; // The maximum disparity value (should fit into the value specified by DISPARITY_DEPTH)

// ********************* Input/Outputs ******************************

input pxclk;
input reset;
input [PIXEL_DEPTH:0] lGrey;
input [PIXEL_DEPTH:0] rGrey;

output wire [DISPARITY_DEPTH:0] disparity;
output reg valid;

// ********************** Declirations ******************************

	reg [LINE_CNT_DEPTH:0] lLine, rLine; // Line counters
	reg [PX_CNT_DEPTH:0] lPixel, rPixel; // Pixel counters

	wire lLineEnable [0:DISPARITY_BLOCK_SIZE];
	wire rLineEnable [0:DISPARITY_BLOCK_SIZE];
	
	// Lines out from the Line Rams
	wire [PIXEL_DEPTH:0] lLinesOut [0:DISPARITY_BLOCK_SIZE];
	wire [PIXEL_DEPTH:0] rLinesOut [0:DISPARITY_BLOCK_SIZE];

	// Lines ordered into columns
	wire [PIXEL_DEPTH:0] lColOut [0:DISPARITY_BLOCK_SIZE];
	wire [PIXEL_DEPTH:0] rColOut [0:DISPARITY_BLOCK_SIZE];

	// Enable the process of hamming
	reg enableHamming;

	// Delay registers for the input pixel, to compensate for lineRam
	// delay
	reg [PIXEL_DEPTH:0] rGreyDelay;
	reg [PIXEL_DEPTH:0] lGreyDelay;

	wire [HAMMING_SIZE:0] rHammingOut, lHammingOut, lHammingOut2;


// ********************* Combinatorial Logic ************************


//Routing system for data from lineRams into the colums

// The bottom element is always the most recently acquired one
assign rColOut[DISPARITY_BLOCK_SIZE] = rGreyDelay;
assign lColOut[DISPARITY_BLOCK_SIZE] = lGreyDelay;

genvar i,j;
generate
	for(i=0; i<DISPARITY_BLOCK_SIZE+1; i=i+1) begin :ENABLES
		assign lLineEnable[i] = ((lLine%(DISPARITY_BLOCK_SIZE+1))==i);
		assign rLineEnable[i] = ((rLine%(DISPARITY_BLOCK_SIZE+1))==i);
		for(j=0; j<DISPARITY_BLOCK_SIZE; j=j+1) begin :INNER
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
			bufif1 r[PIXEL_DEPTH:0] (rColOut[j],rLinesOut[(i+j+1)%(DISPARITY_BLOCK_SIZE+1)],rLineEnable[i]);
			bufif1 l[PIXEL_DEPTH:0] (lColOut[j],lLinesOut[(i+j+1)%(DISPARITY_BLOCK_SIZE+1)],lLineEnable[i]);
		end
	end
endgenerate


// ************************ Sync Logic ******************************

always @(posedge pxclk or posedge reset) begin
	if(reset) begin
		lLine <= 0;
		rLine <= 0;
		lPixel <= 0;
		rPixel <= 0;
		valid <= 0;
		enableHamming <= 0;
	end else begin
		// Push pixels through the shift registers
		rGreyDelay <= rGrey;
		lGreyDelay <= lGrey;
		// Incriment Left Pixel values and Lines
		if(lPixel < PIXELS_PER_LINE) begin
			lPixel <= lPixel + 1;
		end else begin
			lPixel <= 0;
			valid <= 0;
			enableHamming <= 0;
			if(lLine < LINES_PER_FRAME) begin
				lLine <= lLine + 1;
			end else begin
				lLine <= 0;
			end
		end
		// Incriment Right Pixel values and Lines
		if(rPixel < PIXELS_PER_LINE) begin
			rPixel <= rPixel + 1;
		end else begin
			rPixel <= 0;
			valid <= 0;
			enableHamming <= 0;
			if(rLine < LINES_PER_FRAME) begin
				rLine <= rLine + 1;
			end else begin
				rLine <= 0;
			end
		end

		// Set hamming enable after we have enough pixels
		if ((rLine > DISPARITY_BLOCK_SIZE) && (rPixel > DISPARITY_BLOCK_SIZE) && (lLine > DISPARITY_BLOCK_SIZE) && (lPixel > DISPARITY_BLOCK_SIZE)) begin
			// Set valid after we have enougn hamming strings
			if ((rLine > (DISPARITY_BLOCK_SIZE + MAX_DISPARITY)) && (lLine > (DISPARITY_BLOCK_SIZE + MAX_DISPARITY))) begin
				valid <= 1;
			end else begin
				valid <= 0;
			end
		       enableHamming <= 1;
	       end else begin
		       enableHamming <= 0;
		       valid <= 0;
		end

	end
end

// ********************** Instantiations ****************************

wire [NUM_LINES*PIXEL_DEPTH-1:0] lCols,rCols;

genvar n;
generate
for(n=0;n<NUM_LINES;n=n+1) begin
	assign lCols[(n+1)*PIXEL_DEPTH-1:n*PIXEL_DEPTH] = lColOut[n];
	assign rCols[(n+1)*PIXEL_DEPTH-1:n*PIXEL_DEPTH] = rColOut[n];
end
endgenerate


hamReg2  #(.BOX_WIDTH(NUM_LINES), .PIXEL_DEPTH(PIXEL_DEPTH)) lHamming (
	.clk(pxclk),
	.reset(reset),
	.inputs(lCols),
	.he(enableHamming),
	.hamOut(lHammingOut)
);


hamReg2  #(.BOX_WIDTH(NUM_LINES), .PIXEL_DEPTH(PIXEL_DEPTH)) rHamming (
	.clk(pxclk),
	.reset(reset),
	.inputs(rCols),
	.he(enableHamming),
	.hamOut(rHammingOut)
);

mindistance2 #(.NUM_LINES(NUM_LINES), .HAMMING_SIZE(HAMMING_SIZE), .MAX_DISPARITY(MAX_DISPARITY), .DISPARITY_DEPTH(DISPARITY_DEPTH), .TREE_HEIGHT(2)) mind(
	.clk(pxclk),
	.reset(reset),
	.lham(lHammingOut),
	.rham(rHammingOut),
	.dout(disparity)
);

genvar k;
generate 
	for(k=0;k<3;k=k+1) begin :LINES
		singleLine lLineRam2(
			.clk(pxclk),
			.addr(lPixel),
			.datain(lGrey),
			.re(~lLineEnable[k]),
			.oData(lLinesOut[k])
		);	

		singleLine rLineRam0(
			.clk(pxclk),
			.addr(rPixel),
			.datain(rGrey),
			.re(~rLineEnable[k]),
			.oData(rLinesOut[k])
		);
	end
endgenerate

endmodule
