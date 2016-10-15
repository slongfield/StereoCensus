// Array of registers to calculate the hamming string
// This is designed for the 3x3 case.  
// As far as I can tell, will need to python-generate larger hamRegs
// Mostly due to the three inputs

// Done as an array of regs in hardware so we can access any of them at
//  any time, as opposed to memory, which limits how often and with what
//  topology we can access things

`timescale 1us/10ps
module hamReg2(
	      clk, 	// Clock in
	      reset,	// Async reset
	      inputs,   // Inputs
	      he,	// Ham Enable
	      hamOut   	// Output hamming string
);

parameter PIXEL_DEPTH = 9;
parameter BOX_WIDTH = 3;
// The BOX_WIDTH parameter should be odd, so there is a definate center

input clk;
input reset;
input [(PIXEL_DEPTH+1)*BOX_WIDTH-1:0] inputs;
input he;

output [BOX_WIDTH*BOX_WIDTH-2:0] hamOut;
reg [0:BOX_WIDTH*BOX_WIDTH-1] hamming;

wire [PIXEL_DEPTH:0] inCols [BOX_WIDTH-1:0];
genvar n;
generate
for (n=0;n<BOX_WIDTH;n=n+1) begin :COLS
	assign inCols[n] = inputs[(n+1)*(PIXEL_DEPTH+1)-1:n*(PIXEL_DEPTH+1)];
end
endgenerate

assign hamOut = {hamming[0:((BOX_WIDTH*BOX_WIDTH)>>1)-1],hamming[((BOX_WIDTH*BOX_WIDTH)>>1)+1:BOX_WIDTH*BOX_WIDTH-1]};

reg [PIXEL_DEPTH:0] pixReg [0:BOX_WIDTH-1][0:BOX_WIDTH-1];

genvar i,j;
generate
for(i=0;i<BOX_WIDTH;i=i+1) begin :INNER
	for(j=0;j<BOX_WIDTH;j=j+1) begin :OUTER
		always @(posedge clk or posedge reset) begin
			if(reset) begin
				pixReg[i][j] <= 0;
				hamming[i*(BOX_WIDTH)+j] <= 0;
			end else begin
				if(j==0) begin
					pixReg[i][j] <= inCols[i];
				end else begin
					pixReg[i][j] <= pixReg[i][j-1];
				end
				//Pack bits into the hamming string.
				hamming[i*BOX_WIDTH+j] <= pixReg[i][j]>pixReg[BOX_WIDTH>>1][BOX_WIDTH>>1];
				// Ignore them if hamming isn't enabled.
				//if(he==0) hamming <= 0;
			end
		end
	end
end
endgenerate
endmodule 

module t_hamreg;


parameter PIXEL_DEPTH = 9;
parameter BOX_WIDTH = 3;

	reg clk;
	reg reset;
	wire [(PIXEL_DEPTH+1)*BOX_WIDTH-1:0] inputs;
	reg he;
	wire [BOX_WIDTH*BOX_WIDTH-2:0] hamOut;
	wire [7:0] myOut;
	wire correct;

	reg [PIXEL_DEPTH:0] line1;
	reg [PIXEL_DEPTH:0] line2;
	reg [PIXEL_DEPTH:0] line3;

	assign inputs = {line1,line2,line3};

	assign myOut = {(line2>line1-2),(line2>line1-1),(line2>line1),(line2>line2-2),(line2>line2),(line2>line3-2),(line2>line3-1),(line2>line3)};

	assign correct = (hamOut == 167'b00000000000000000000000000000000000000000000000000000000000000000000000000000000001111111111111111111111111111111111111111111111111111111111111111111111111111111111111);
	// Attempted to generate hamming strings for 167 bit long output... 
	// After 1/2 hour, computer still hadn't finished.  Not sure what went
	// wrong.  However, since the numbers are always increasing, this
	// should always be the output.

	hamReg2 DUT(.clk(clk), .reset(reset), .inputs(inputs), .he(he), .hamOut(hamOut));

	initial clk <= 0;
	always #20 clk <= ~clk;

	initial begin
		reset <= 1;
		he = 1;
		line1 = 0;
		line2 = 10;
		line3 = 20;
		#100 
		reset <= 0;
	end

	always @(posedge clk) begin
		line1 <= line1 + 1;
		line2 <= line2 + 1;
		line3 <= line3 + 1;
	end

endmodule
