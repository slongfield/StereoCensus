# pop_count_gen.py
#
# Takes in a single argument, the number of inputs, and generates an
# unpipelined population count adder tree.
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
import math

# Header format string is parameterized by the number of stages needed
_HEADER = """
`ifndef CENSUS_POP_COUNT_{0}_V_
`define CENSUS_POP_COUNT_{0}_V_

`timescale 1ns/1ps

`include "dff.v"

// pop_count computes the population count of the input.
module pop_count_{0}#(
  parameter WIDTH=1
  ) (
    input wire clk,
    input wire rst,

    input wire  [WIDTH-1:0] inp,
    output wire [$clog2(WIDTH)-1:0] outp
  );
"""

_FOOTER = """
endmodule

`endif // CENSUS_POP_COUNT_{0}_V_
"""

parser = argparse.ArgumentParser()
parser.add_argument(
    "--width",
    help="Width of the population counter to generate",
    type=int,
    required=True)


def get_args():
    """get_args parses the args with argparse.

    Returns:
      width (int): Width that was passed on the commmand line.
    """
    args = parser.parse_args()
    return args.width


def clog2(x):
    """clog2 returns the ceiling of log_2(x).

    Args:
        x (int/float): Number to get the clog2 of

    Returns:
        clog2(x)
    """
    return int(math.ceil(math.log(x, 2)))


def generate_masks(width):
    """Generate masks generates a series of bitmasks for a tree adder.

    Args:
        width (int): width of the bitmasks, must be a power of two

    Returns:
        bitmasks (list[string]): A series of hex bitmasks selecting
           sequences of bits of increasing bits (in power of two increments)
    """

    assert (width & (width - 1)) == 0, "Width must be a power of two"

    bitmasks = []

    for stage in range(clog2(width)):
        mask = []
        stage_width = 1 << stage
        for _ in range(0, width, stage_width * 2):
            mask.append('0' * stage_width)
            mask.append('1' * stage_width)
        # Python adds an 'L' at the end if the width is greater than 64, but
        # Verilog doesn't want that, so strip it off. Also remove the leading
        # 0x, since verilog wants {width}'h.
        bitmasks.append(hex(int("".join(mask), 2)).strip('L')[2:])

    return bitmasks


def generate_adders(width):
    """Generates an adder tree.

    Assumes that masks exist, where mask m{n} represents a bitmask that
    exposes substrings of width 2^n.

    Args:
        width (int): width of the adder. Doesn't need to be a power of two.

    Returns:
        adders (list[string]): stages of an adder tree
    """

    # Format string to generate an adder.
    #  0: index into the storage array
    #  1: index+1
    #  2: index+2
    #  3: 1 << (index+1)
    # Start ignoring LineLengthBear
    _ADDER_FORMAT = """  if ($clog2(WIDTH) >= {2}) begin
    assign x[{1}] = (x[{0}] & m{1}[WIDTH-1:0]) + ((x[{0}] >> {3}) & m{1}[WIDTH-1:0]);
  end"""
    # Stop ignoring

    adders = []

    for idx in range(clog2(width) - 1):
        adders.append(_ADDER_FORMAT.format(
            idx, idx + 1, idx + 2, 1 << (idx + 1)))

    return adders


def generate_pop_count(width):
    """Generates an adder tree to compute the number of '1'.

    Args:
        width (int): The maximum width of the adder tree.

    Returns:
        pop_counter (string): Verilog representation of an adder tree.
    """

    clog_width = clog2(width)

    # Width, rounded up to the nearest power of two
    width_power2 = 1 << clog_width

    pop_count = [_HEADER.format(clog_width)]

    # Add local parameters for the bitmasks
    for i, param in enumerate(generate_masks(width_power2)):
        pop_count.append("  localparam m{} = {}'h{};".format(i, width_power2,
                                                             param))

    pop_count.append("""
  // Need to turn off of this lint check due to long-standing Verilator bug#63.
  /* verilator lint_off UNOPTFLAT */""")

    # Array for intermediate values
    pop_count.append("  wire [WIDTH-1:0] x[$clog2(WIDTH)];")

    # Output flop
    pop_count.append(
        "  dff#(.WIDTH($clog2(WIDTH))) ")
    pop_count.append(
        "    out_ff(clk, rst, x[$clog2(WIDTH)-1][$clog2(WIDTH)-1:0], outp);")

    # Initial adder
    pop_count.append(
        "  assign x[0] = (inp & m0[WIDTH-1:0]) + ((inp >> 1) & m0[WIDTH-1:0]);")

    # Generate the adder tree.
    pop_count.append("  generate")
    pop_count.extend(generate_adders(width))

    # Add an assertion for the maximum width
    pop_count.append("""  if ($clog2(WIDTH) > {}) begin
    initial begin
      assert(0); // Cannot handle widths larger than {}.
    end
  end""".format(clog_width, width_power2))

    pop_count.append("  endgenerate")
    pop_count.append("  /* verilator lint_on UNOPTFLAT */")

    pop_count.append(_FOOTER.format(clog_width))

    return "\n".join(pop_count)


def run():
    width = get_args()
    print(generate_pop_count(width))

if __name__ == '__main__':
    run()
