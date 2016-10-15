// Stereo Module
//
// Stephen Longfield Dec 15, 2008
// Generated fresh on 2009-01-23

// params 16 450 375 60 90 


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
// Will also be used to overload the test values in lower-level modules.
// Number of bits (minus 1) needed to store pixel data
parameter PIXEL_DEPTH = 15;  	
// How many bits (minus 1) needed to store number of pixels per line 
// 	(log2(PIXELS_PER_LINE+1)-1)
parameter PX_CNT_DEPTH = 8;
// How many bits (minus 1) needed to store the number of lines per frame
// 	 (log2(LINES_PER_FRAME+1)-1)
parameter LINE_CNT_DEPTH = 9;	
// How many pixels (minus 1) per line
parameter PIXELS_PER_LINE = 449;
// How many pixels (minus 1) per line
parameter LINES_PER_FRAME = 374;
// Total number of pixels (minus 1)
parameter TOTAL_PIXELS = 168749;
// How many pixles (minus 1) on each side of the hamming block
parameter HAMMING_BLOCK_SIZE = 59; // How many total pixels (minus 1) in each 
//	hamming block (HAMMING_BLOCK_SIZE+1)^2-2
parameter HAMMING_TOTAL_SIZE = 3598; 
// Number of bits (minus 1) needed to store the hamming block 
// 	(log2(HAMMING_TOTAL_SIZE+1)-1)
parameter HAMMING_DEPTH = 11;	
// Maximum dispartiy value (minus 1)
parameter MAX_DISPARITY = 89;
// How many bits (minus 1) needed to store MAX_DISPARITY 
// 	(log2(DISPARITY_DEPTH+1)-1;
parameter DISPARITY_DEPTH = 6;
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
wire [0:HAMMING_BLOCK_SIZE] lLineEnable;
wire [0:HAMMING_BLOCK_SIZE] rLineEnable;
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
hamReg2 #(.PIXEL_DEPTH(PIXEL_DEPTH), .BOX_WIDTH(HAMMING_BLOCK_SIZE+1)) lHamReg(.clk(pxclk), .reset(reset), .inputs({lColOut[0],lColOut[1],lColOut[2],lColOut[3],lColOut[4],lColOut[5],lColOut[6],lColOut[7],lColOut[8],lColOut[9],lColOut[10],lColOut[11],lColOut[12],lColOut[13],lColOut[14],lColOut[15],lColOut[16],lColOut[17],lColOut[18],lColOut[19],lColOut[20],lColOut[21],lColOut[22],lColOut[23],lColOut[24],lColOut[25],lColOut[26],lColOut[27],lColOut[28],lColOut[29],lColOut[30],lColOut[31],lColOut[32],lColOut[33],lColOut[34],lColOut[35],lColOut[36],lColOut[37],lColOut[38],lColOut[39],lColOut[40],lColOut[41],lColOut[42],lColOut[43],lColOut[44],lColOut[45],lColOut[46],lColOut[47],lColOut[48],lColOut[49],lColOut[50],lColOut[51],lColOut[52],lColOut[53],lColOut[54],lColOut[55],lColOut[56],lColOut[57],lColOut[58],lColOut[59]}), .he(1'b1), .hamOut(lHamming));

hamReg2 #(.PIXEL_DEPTH(PIXEL_DEPTH), .BOX_WIDTH(HAMMING_BLOCK_SIZE+1)) rHamReg(.clk(pxclk), .reset(reset), .inputs({rColOut[0],rColOut[1],rColOut[2],rColOut[3],rColOut[4],rColOut[5],rColOut[6],rColOut[7],rColOut[8],rColOut[9],rColOut[10],rColOut[11],rColOut[12],rColOut[13],rColOut[14],rColOut[15],rColOut[16],rColOut[17],rColOut[18],rColOut[19],rColOut[20],rColOut[21],rColOut[22],rColOut[23],rColOut[24],rColOut[25],rColOut[26],rColOut[27],rColOut[28],rColOut[29],rColOut[30],rColOut[31],rColOut[32],rColOut[33],rColOut[34],rColOut[35],rColOut[36],rColOut[37],rColOut[38],rColOut[39],rColOut[40],rColOut[41],rColOut[42],rColOut[43],rColOut[44],rColOut[45],rColOut[46],rColOut[47],rColOut[48],rColOut[49],rColOut[50],rColOut[51],rColOut[52],rColOut[53],rColOut[54],rColOut[55],rColOut[56],rColOut[57],rColOut[58],rColOut[59]}), .he(1'b1), .hamOut(rHamming));


mindistance4 #(.HAMMING_TOTAL_SIZE(HAMMING_TOTAL_SIZE), .HAMMING_DEPTH(HAMMING_DEPTH), .MAX_DISPARITY(MAX_DISPARITY), .DISPARITY_DEPTH(DISPARITY_DEPTH)) md4 (.clk(pxclk), .reset(reset), .lham(lHamming), .rham(rHamming), .dout(oData));


// ********************* Combinatorial Logic ************************

//Routing system for data from lineRams into the colums

// The bottom element is always the most recently acquired one
assign rColOut[HAMMING_BLOCK_SIZE] = rBuffer;
assign lColOut[HAMMING_BLOCK_SIZE] = lBuffer;

reg [0:LINE_CNT_DEPTH] lLinemod [0:HAMMING_BLOCK_SIZE];
reg [0:LINE_CNT_DEPTH] rLinemod [0:HAMMING_BLOCK_SIZE];



genvar i,j,m;
generate
	for(i=0; i<HAMMING_BLOCK_SIZE+1; i=i+1) begin :ENABLES
		always @(negedge iHref or posedge reset) begin
			if(reset) begin
				lLinemod[i] <= 0;
				rLinemod[i] <= 0;
			end else begin
				if(~iVsync) begin
					if (lLinemod[i] < HAMMING_BLOCK_SIZE) begin
						lLinemod[i] <= lLinemod[i] + 1;
					end else begin
						lLinemod[i] <= 0;
					end
					if (rLinemod[i] < HAMMING_BLOCK_SIZE) begin
						rLinemod[i] <= rLinemod[i] + 1;
					end else begin
						rLinemod[i] <= 0;
					end
				end else begin
					lLinemod[i] <= 0;
					rLinemod[i] <= 0;
				end
			end
		end
		assign lLineEnable[i] = (lLinemod[i] == i);
		assign rLineEnable[i] = (rLinemod[i] == i);
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
			for(m=0; m<PIXEL_DEPTH+1;m=m+1) begin :BUFFERS
				bufif1 r (rColOut[j][m],rLinesOut[(i+j+1)%(HAMMING_BLOCK_SIZE+1)][m],rLineEnable[i]);
				bufif1 l (lColOut[j][m],lLinesOut[(i+j+1)%(HAMMING_BLOCK_SIZE+1)][m],lLineEnable[i]);
			end
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


endmodule