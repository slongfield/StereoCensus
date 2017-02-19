# census_gen.py
#
# From some command-line options generates a stereo vision census verilog
# module.
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

# The header format string expects:
#   bit_width:     the number of bits in the input stream
#   max_disparity: maximum disparity searching for (used to determine output
#                  width)
_HEADER = """
`ifndef STEREO_CENSUS_V_
`define STEREO_CENSUS_V_

module stereo (
    input wire clk,
    input wire rst,

    input wire [{bit_width}-1:0] inp_left,
    input wire [{bit_width}-1:0] inp_right,

    output wire [$clog2({max_disparity}] outp
  );
"""

# Footer takes no parameters.
_FOOTER = """
endmodule 

`endif // STEREO_CENSUS_V_"""
