# argmin_gen.py
#
# Takes in a single argument, the number of inputs, and generates a verilog
# armin tree, using the argmin_helper.
#
# Copyright (c) 2016, Stephen Longfield, stephenlongfield.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse

# Header is a format string, expecting number of inputs as an argument.
_HEADER = """
`ifndef CENSUS_ARGMIN_{0}_V_
`define CENSUS_ARGMIN_{0}_V_

module argmin_{0}#(
    parameter WIDTH=1
  ) (
    input wire clk,
    input wire rst,

    input wire [WIDTH*{0}-1:0] inp,

    output wire [WIDTH-1:0] outp,
    output wire [$clog2({0})-1:0] outp_addr
  );

  localparam ADDR_WIDTH = $clog2({0});
"""

_FOOTER = """
endmodule

`endif // CENSUS_ARGMIN_V_
"""

_STAGE = """
  argmin_helper#(.WIDTH(WIDTH), .ADDR_WIDTH(ADDR_WIDTH), .NUM_INP({num_inp}),
                 .NUM_OUTP({num_outp}), .STAGE({stage}))
                ah_{stage}(clk, rst, {inp}, {inp_addr}, {outp}, {outp_addr});
"""

parser = argparse.ArgumentParser()
parser.add_argument(
    "--num_inputs",
    help="number of inputs in the generated argmin",
    type=int,
    required=True)


def get_args():
    """get_args parses the args with argparse.

    Returns:
      num_inputs (int): Number of inputs that was passed on the commmand line.
    """
    args = parser.parse_args()
    return args.num_inputs


def generate_argmin(num_inputs):
    """generate_argmin generates an argmin function

    Args:

    Returns:
      argmin (string): verilog that computes the argmin function
    """
    lines = []
    lines.append(_HEADER.format(num_inputs))

    # Pretend the inputs were the outputs from some imaginary previous stage.
    prev_output = "inp"
    prev_output_addr = "0"
    stage = 0
    input_size = num_inputs

    while (input_size > 1):
        output_size = input_size // 2 + input_size % 2

        outp_name = "data_{}".format(stage)
        outp_addr = "addr_{}".format(stage)

        # Create some new output ports
        lines.append("  wire [WIDTH*{}-1:0]      {};".format(output_size,
                                                             outp_name))
        lines.append("  wire [ADDR_WIDTH*{}-1:0] {};".format(output_size,
                                                             outp_addr))
        lines.append(_STAGE.format(num_inp=input_size, num_outp=output_size,
                                   stage=stage, inp=prev_output, inp_addr=prev_output_addr,
                                   outp=outp_name, outp_addr=outp_addr))

        stage += 1
        input_size = output_size
        prev_output = outp_name
        prev_output_addr = outp_addr

    # Set up the outputs
    lines.append("  assign outp      = {};".format(prev_output))
    lines.append("  assign outp_addr = {};".format(prev_output_addr))

    lines.append(_FOOTER)
    return "\n".join(lines)


def run():
    num_inputs = get_args()
    print(generate_argmin(num_inputs))

if __name__ == '__main__':
    run()
