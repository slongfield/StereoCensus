//Module using the Hackmem 169 Method to count up to 63 bits
//Contains a two-stage pipeline.

//Note: currently configured for 8-bit numbers


module hackmem169_63 (clk, reset, bitsin, cntout);
	input clk;
	input reset;
	input [7:0] bitsin;	 
	
	output reg [4:0] cntout;
	
	reg [7:0] storeg;
	
	wire [7:0] a;
	wire [7:0] b;
	
	// Initialize values to 0
	initial begin
		cntout <= 0;
		storeg <= 0;
	end

	//a = (in >> 1) &0333
	buf (a[0],bitsin[1]);
	buf (a[1],bitsin[2]);
	buf (a[2],0);
	buf (a[3],bitsin[4]);
	buf (a[4],bitsin[5]);
	buf (a[5],0);
	buf (a[6],bitsin[7]);
	buf (a[7],0);
	
	//b = (in >> 2) &0111
	buf (b[0],bitsin[2]);
	buf (b[1],0);
	buf (b[2],0);
	buf (b[3],bitsin[5]);
	buf (b[4],0);
	buf (b[5],0);
	buf (b[6],0);
	buf (b[7],0);

		
	always @(posedge clk)
		begin
			storeg <= bitsin - a - b;
			cntout <= ((storeg+(storeg>>3)) & 8'b11000111)%63;
		end
endmodule

module t_hackmem;
	reg clk;
	reg reset;

	reg [7:0] bitsin;
	reg [7:0] bitsin1;
	reg [7:0] bitsin2;
	wire [4:0] countout;

	wire correct;

	hackmem169_63 DUT(.clk(clk), .bitsin(bitsin), .cntout(countout));

	assign correct = ((bitsin2[0]+bitsin2[1]+bitsin2[2]+bitsin2[3]+bitsin2[4]+bitsin2[5]+bitsin2[6]+bitsin2[7]) == countout);

	initial begin 
		clk = 0;
		bitsin = 0;
	end

	always #20 clk = ~clk;

	always @(posedge clk) begin
	       bitsin1 <= bitsin;
	       bitsin2 <= bitsin1;
	       bitsin <= bitsin+1;
        end

endmodule
