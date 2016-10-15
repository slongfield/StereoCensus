// Tree sum -- sum up the bits using a tree of adders
// 	Uses successive masking, shifting and adding to make the tree in order
// 	to hopefully make it more python-generatable.
//
// 	Designed to be a drop-in replacement for hackmem169
//
// 	Prototyped with HAMMING_TOTAL_SIZE of 20
//
// 	Stephen Longfield
// 	January 3, 2008
//
//

module treesum (clk, reset, bitsin, cntout);

// *** PARAMETERS ***

parameter HAMMING_TOTAL_SIZE = 20;
parameter MASK_1 = 20'b01010101010101010101;
parameter MASK_2 = 20'b00110011001100110011;
parameter MASK_3 = 20'b11110000111100001111;
parameter MASK_4 = 20'b11110000000011111111;
parameter MASK_5 = 20'b00001111111111111111;
parameter HAMMING_DEPTH = 4;

// Note: Cool feature used below:  tree will always be HAMMING_DEPTH tall,
// since it is a binary adder tree, and HAMMING_DEPTH is the log2 of the
// number of bits.

// **** Input/Output ****

input clk;
input reset;
input [HAMMING_TOTAL_SIZE-1:0] bitsin;

output wire [HAMMING_DEPTH:0] cntout;

reg [HAMMING_TOTAL_SIZE-1:0] bitstore [HAMMING_DEPTH:0];

// ***** Combinatorial Logic *****

assign cntout = bitstore[HAMMING_DEPTH][HAMMING_DEPTH:0];

// ****** Syncronous logic ******

always @(posedge clk or posedge reset) begin
	if(reset) begin
		bitstore[0] <= 0;
		bitstore[1] <= 0;
		bitstore[2] <= 0;
		bitstore[3] <= 0;
		bitstore[4] <= 0;
	end else begin
		bitstore[0] <= (bitsin & MASK_1) + ((bitsin & ~MASK_1)>>1);
		bitstore[1] <= (bitstore[0] & MASK_2) + ((bitstore[0] & ~MASK_2)>>2);
		bitstore[2] <= (bitstore[1] & MASK_3) + ((bitstore[1] & ~MASK_3)>>4);
		bitstore[3] <= (bitstore[2] & MASK_4) + ((bitstore[2] & ~MASK_4)>>8);
		bitstore[4] <= (bitstore[3] & MASK_5) + ((bitstore[3] & ~MASK_5)>>16);
	end
end

endmodule 


// Maybe parameterize this?
module t_treesum;
	reg clk;
	reg reset;

	reg [19:0] bitsin;

	wire [4:0] countout;

	treesum DUT(.clk(clk), .reset(reset), .bitsin(bitsin), .cntout(countout));

	
	initial clk <= 0;
	always #20 clk <= ~clk;

	initial begin
		bitsin <= 0;
		reset <= 0;
		#40
		reset <= 1;
		#100
		reset <= 0;
	end

	always @(posedge clk) begin
		bitsin[19:1] <= bitsin[18:0];
		bitsin[0] <= 1;
	end
endmodule
