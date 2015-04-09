//
// some comment here
//

module mindistance2(clk, reset, lham, rham, dout);

   //Default values from test case
   parameter NUM_LINES = 3; // see stereo2.v
   parameter HAMMING_SIZE = 7; // Hamming size (minus 1).  See stereo2.v
   parameter MAX_DISPARITY = 4; // see stereo.v
   parameter DISPARITY_DEPTH = 1; // see stereo2.v
   parameter TREE_HEIGHT = 2; // Height minus 1

   input clk;
   input reset;
   input [HAMMING_SIZE:0] lham, rham;

   output wire [DISPARITY_DEPTH:0] dout;

   reg [HAMMING_SIZE:0]            lhamreg [(MAX_DISPARITY-1):0];
   reg [HAMMING_SIZE:0]            rhamreg [(MAX_DISPARITY-1):0];

   wire [HAMMING_SIZE:0]           hamdistance [(MAX_DISPARITY-1):0];
   wire [(MAX_DISPARITY-1):0]      distance [(MAX_DISPARITY-1):0];

   // Three dimensional register array to hold the minimizer tree
   reg [HAMMING_SIZE:0]            tree [TREE_HEIGHT:0] [MAX_DISPARITY:0];

   // Assign dout to the top of the tree
   assign dout = tree[TREE_HEIGHT][MAX_DISPARITY];

   // Generate XORS and Counters
   genvar  i;
   generate
      for(i=0; i<MAX_DISPARITY; i=i+1) begin :PROCESS
	 xor x [HAMMING_SIZE:0] (hamdistance[i],rhamreg[i],lhamreg[MAX_DISPARITY-1]);
	 if(HAMMING_SIZE<=63) begin
	    hackmem169_63 hm (clk,hamdistance[i],distance[i]);
	 end
	 // NEED ELSE CASE HERE!
      end
   endgenerate

   // connect count output to tree
   genvar m;
   generate
      for(m=0; m<MAX_DISPARITY; m=m+1) begin :CONNECT
	 always @(posedge clk or posedge reset) begin
	    if(reset) begin
	       tree[0][m] <= 0;
	    end else begin
	       tree[0][m] <= distance[m];
	    end
	 end
      end
   endgenerate

   // shift registers
   genvar n;
   generate
      for(n=0; n<MAX_DISPARITY; n=n+1) begin
	 always @(posedge clk or posedge reset) begin
	    if(reset) begin
	       lhamreg[n] <= 0;
	       rhamreg[n] <= 0;
	    end else begin
	       if(n == 0) begin
		  lhamreg[0] <= lham;
		  rhamreg[n] <= rhamreg[n+1];
	       end else begin 
		  if(n == MAX_DISPARITY-1) begin
		     lhamreg[MAX_DISPARITY-1] <= lhamreg[n-1];
		     rhamreg[MAX_DISPARITY-1] <= rham;
		  end else begin
		     lhamreg[n] <= lhamreg[n-1];
		     rhamreg[n] <= rhamreg[n+1];
		  end
	       end
	    end
	 end
      end
   endgenerate

   // generate tree minimizer code
   genvar j,k;
   generate
      for(j=1; j<=TREE_HEIGHT; j=j+1) begin :OUTERTREE
	 for(k=0; k<(MAX_DISPARITY>>j+((MAX_DISPARITY>>(j-1))%2));k=k+1) begin :INNERTREE
	    always @(posedge clk or posedge reset) begin
	       if(reset) begin
		  tree[j][k] <= 0;
		  tree[j][MAX_DISPARITY-k] <= 0; //Index value of [i,j]
	       end else begin
		  if((k<<1)>(MAX_DISPARITY>>(j-1)+((MAX_DISPARITY>>(j-2))%2))) begin
		     //If we're at the end of the
		     //current row, and the current
		     //value is odd
		     tree[j][k] <= tree[j-1][(k<<1)+1]; // Value
		     if(j!=1) begin
			tree[j][MAX_DISPARITY-k] <= tree[j-1][MAX_DISPARITY-((k<<1)+1)]; // Index
		     end else begin
			tree[j][MAX_DISPARITY-k] <= (k<<1)+1;
		     end
		  end else begin
		     // Normal case
		     if(tree[j-1][k<<1] <= tree[j-1][(k<<1)+1]) begin
			tree[j][k] <= tree[j-1][k<<1];
			if(j!=1) begin
			   tree[j][MAX_DISPARITY-k] <= tree[j-1][MAX_DISPARITY-(k<<1)];
			end else begin
			   tree[j][MAX_DISPARITY-k] <= k<<1;
			end
		     end else begin
			tree[j][k] <= tree[j-1][(k<<1)+1];
			if(j!=1) begin
			   tree[j][MAX_DISPARITY-k] <= tree[j-1][MAX_DISPARITY-((k<<1)+1)];
			end else begin
			   tree[j][MAX_DISPARITY-k] <= (k<<1)+1;
			end
		     end
		  end
	       end
	    end
	 end
      end
   endgenerate

endmodule

module t_mindistance2;
   parameter NUM_LINES = 3; // see stereo2.v
   parameter HAMMING_SIZE = 7; // Hamming size (minus 1). See stereo2.v
   parameter MAX_DISPARITY = 4; // see stereo.v
   parameter DISPARITY_DEPTH = 1; // see stereo2.v
   parameter TREE_HEIGHT = 2; // Height minus 1

   // inputs
   reg clk;
   reg reset;
   reg [HAMMING_SIZE:0] lham, rham;

   // outputs
   wire [DISPARITY_DEPTH:0] dout;

   // instances
   mindistance2 DUT(.clk(clk),
                    .reset(reset),
                    .lham(lham),
                    .rham(rham),
                    .dout(dout)
                    );

   // clock
   initial clk <= 0;
   always #10 clk = ~clk;

   // simulation
   initial
   begin
      lham <= 8'b11111111;
      rham <= 8'b11111111;
      reset <= 1;
      #500; // long reset
      reset <= 0;

      #500;
      lham <= 8'b11111111;
      rham <= 8'b00000000;
   end

endmodule