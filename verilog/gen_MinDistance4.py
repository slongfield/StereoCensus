# Creates a minDistance 4 file with the specified settings
import datetime
import sys

def gen_MinDistance4(hamming_total_size, hamming_depth, max_disparity, disparity_depth, outFile):

	# Cannot do bitcounts of greater than 4095 bits...
	#if(hamming_total_size > 4095):
	#	print("Too large of a neighborhood.\n")
	#	sys.exit()
	# can with treesum!

	out = open(outFile, 'w');

	# Write the header information and stuff that doesn't need generation

	out.write("// Combinatorial MinDistance \n")
	out.write("// \n")
	out.write("// Generater written by: \n")
	out.write("// Stephen Longfield, Dec 15, 2008 \n")
	out.write("// Generated fresh on " + str(datetime.date.today()) + "\n\n")
	
	# Module name:

	out.write("module mindistance4(clk, reset, lham, rham, dout); \n")

	# Parameters!  This makes writing the rest a bit easier
	out.write("""
  parameter HAMMING_TOTAL_SIZE =""" + str(hamming_total_size-1) + """;
  parameter HAMMING_DEPTH = """ + str(hamming_depth-1) + """;
  parameter MAX_DISPARITY = """ + str(max_disparity-1) + """;
  parameter DISPARITY_DEPTH = """ + str(disparity_depth-1) + """;
		\n""")
	# Don't need masks for treesum!
	# Generated Parameters! -- Masks dependent on the value of hamming_total_size.
	#hamming_hex_size = hamming_total_size/4
	#hamming_hex_overflow = hamming_total_size%4
	#if(hamming_hex_overflow>0):
	#	hamming_overflow = 1 
	#else:
	#	hamming_overflow = 0

	# Make calculations for the output mask -> repeated 00F00F
	#mask_out_size = hamming_total_size/12
	# If there are bits that don't fit well into the three hex land well..
	#	Figure out how to compensate:
	#mask_out_overflow = hamming_total_size%12
	#if(mask_out_overflow > 8):
	#	overflow = "00F"
	#elif(mask_out_overflow > 4):
	#	overflow = "0F"
	#elif(mask_out_overflow > 0):
	#	overflow = "F"
	#else:
	#	overflow = ""
		

	#out.write("""
  #parameter MASK_1 = """ + str(hamming_total_size) +  """'h""" + "1"*hamming_hex_size + "1"*hamming_overflow + """;
  #parameter MASK_2 = """ + str(hamming_total_size) +  """'h""" + "3"*hamming_hex_size + "3"*hamming_overflow + """;
  #parameter MASK_3 = """ + str(hamming_total_size) +  """'h""" + "7"*hamming_hex_size + "7"*hamming_overflow + """;
  #parameter MASK_OUT = """ + str(hamming_total_size) +  """'h""" + overflow + "00F"*mask_out_size + """;
#\n""")

	# Add in the I/O and variables.  Controlled by parameter sizes already.
	out.write("""	
  input clk;
  input reset;
  input [HAMMING_TOTAL_SIZE:0] lham;
  input [HAMMING_TOTAL_SIZE:0] rham;
  output reg [DISPARITY_DEPTH:0] dout;

  reg [HAMMING_TOTAL_SIZE:0] rham_shift [MAX_DISPARITY:0];
  wire [HAMMING_DEPTH:0] distances [MAX_DISPARITY:0];
\n""")

	# Now we need to instantiate max_disparity number of treesum modules
	# Note: Assuming these are the treesum modules generated, so don't need masks... 
	# Don't really need to pass in any parameters, then...
	
	for i in range(max_disparity):
		out.write("""
  treesum #(.HAMMING_TOTAL_SIZE(HAMMING_TOTAL_SIZE), .HAMMING_DEPTH(HAMMING_DEPTH))
                    ts""" + str(i) + """ (clk,reset,lham^rham_shift[""" + str(i) + """],distances[""" + str(i) + """]);
""")

	# Begin generation of sequential logic.

	out.write("""
  always @(posedge clk or posedge reset) begin
    if(reset) begin
      dout <= 0;
""")

	# Reset shift registers
	for i in range(max_disparity):
		out.write("""
      rham_shift[""" + str(i) + """] <= 0;""")

	# Start sequential data processing
	out.write("""
    end else begin""")

	# Shift shift registers
	for i in range(max_disparity):
		if(i == 0):
			out.write("""
      rham_shift[0] <= rham;""")
		else:
			out.write("""
      rham_shift[""" + str(i) + """] <= rham_shift[""" + str(i-1) + """];""")

	# Now we need to generate the code to find the minimum distances... This is ugly in many ways
	
	for i in range(max_disparity):
		if(i == 0):
			out.write("""

      if (""")
		else:
			out.write("""
      end else if(""")

		for j in range(max_disparity):
			if(j > i):
				out.write("(distances[" + str(i) + "] < distances[" + str(j) + "])")
				if(j != max_disparity-1):
					if(i==max_disparity-1 and j==max_disparity-2):
						pass
					else:
						out.write(" && ")


		if(i == max_disparity-1):
			out.write("(distances[" + str(i) + "] !=  distances[" + str(i-1) + "])")
		
		out.write(""") begin
        dout <= """ + str(i) + """;""")

	out.write("""
      end else begin
        dout <= """ + str(max_disparity) + """;
      end
    end
  end
endmodule""")

	out.close()




if __name__=="__main__":
	gen_MinDistance4(16, 4, 10, 4, "test.v")
