// Module using the Hackmem 169 method, expanded to count up to 4095 bits
//
// Currently set up to count 20-bit numbers
// Should be generating a script to generate arbitrary sizes (or maybe see if
//	 we can't do it with parameters...?)

module hackmem169_4095 (clk, reset, bitsin, cntout);

// *** Parameters ***

parameter HAMMING_TOTAL_SIZE = 20;
parameter MASK_1 = 20'h11111;
parameter MASK_2 = 20'h33333;
parameter MASK_3 = 20'h77777;
parameter MASK_OUT = 20'h0F00F;
parameter HAMMING_DEPTH = 4;
// *** Input/Output ***

	input clk;
	input reset;
	input [HAMMING_TOTAL_SIZE:0] bitsin;

	output reg [HAMMING_DEPTH:0] cntout;

	wire [HAMMING_TOTAL_SIZE:0] bitsin_0;
	wire [HAMMING_TOTAL_SIZE:0] bitsin_1;	
	wire [HAMMING_TOTAL_SIZE:0] bitsin_2;
	wire [HAMMING_TOTAL_SIZE:0] bitsin_3;

	reg [HAMMING_TOTAL_SIZE:0] bitstore;


// *** Combinatorial logic ***

	// Stage 0, shift over to set up the bits to be
	// subtracted
	assign bitsin_0 = bitsin;
	assign bitsin_1 = (bitsin >> 3) & MASK_1;
	assign bitsin_2 = (bitsin >> 2) & MASK_2;
	assign bitsin_3 = (bitsin >> 1) & MASK_3;


// *** Syncronous logic ***

	always @(posedge clk or posedge reset) begin
		if (reset) begin
			cntout <= 0;
			bitstore <= 0;
		end else begin

			// Stage 1 Subtract so that each nibble contains the 
			// sum of its individual bits

			bitstore <= bitsin_0 - bitsin_1 - bitsin_2 - bitsin_3;

			// Shift, add and and, in order to make every third
			// nibble the bitcount, then and in order to isolate 
			// the sum that we want from the chaff.

			cntout <= ((bitstore + (bitstore >> 4) + (bitstore >> 8)) & MASK_OUT) % 4095;
		end
	end
endmodule

module t_hackmem2;
	reg clk;
	reg reset;

	reg [19:0] bitsin;

	wire [11:0] countout;

	hackmem169_4095 DUT(.clk(clk), .reset(reset), .bitsin(bitsin), .cntout(countout));

	initial begin
		clk = 0;
		bitsin = 0;
		reset = 0;
		#40
		reset = 1;
		#100
		reset = 0;
	end

	always #20 clk = ~clk;

	always @(posedge clk) begin
		bitsin[19:1] <= bitsin[18:0];
		bitsin[0] <= 1;
	end
endmodule
