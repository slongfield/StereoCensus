/*  Test for the basic stereo vision core.
 *
 *  Copyright (c) 2016, Stephen Longfield, stephenlongfield.com
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 *  Run the test with:
 *    Vcensus_basic [left file] [right file]
 *
 *  Where left file and right file are two equal length files containing the
 *  values from the left 'camera' and right 'camera'. The computed disparities
 *  will be written directly to stdout. Redirect as needed.
 *
 *  Recommend the "to_dat.py" and "from_dat.py" scripts in this directory to
 *  transform images to and from this format.
 *
 */

#include <iostream>
#include <fstream>
#include <cstdlib>

#include "Vcensus_basic.h"
#include "verilated.h"

void usage() {
  std::cout << "Usage: ";
  std::cout << "  Vcensus_basic [left file] [right file]";
}

int main(int argc, char **argv, char **env) {
  Verilated::commandArgs(argc, argv);
  Vcensus_basic* dut = new Vcensus_basic;
  int tick = 0;
  int cycle = 0;
  int lval = 0;
  int rval = 0;

  if (argc != 3) {
    usage();
    exit(1);
  }

  std::ifstream left(argv[1], std::ifstream::in);
  std::ifstream right(argv[2], std::ifstream::in);

  while(!Verilated::gotFinish() && left.good() && right.good()) {
    dut->eval();
    dut->clk = tick%2 == 0;
    if (tick%2) cycle++;
    tick++;
    if (!(tick%2 == 0)) continue;

    // Reset
    if ( cycle <= 1 ) {
      dut->rst = 1;
      continue;
    } else {
      dut->rst = 0;
    }

    left >> lval;
    dut->inp_left = lval;
    right >> rval;
    dut->inp_right = rval;

    std::cout << int(dut->outp) << endl;

  }
  left.close();
  right.close();
  exit(0);
}
