/*  Test for the census transform.
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
 */

#include <iostream>

#include "Vcensus_test.h"
#include "verilated.h"

// Want Width*Height to be less than 32 for this test, so the output fits in a
// single 32-bit integer.
int kWidth = 5;
int kHeight = 5;
int kResetCycles = 3;

int main(int argc, char **argv, char **env) {
  Verilated::commandArgs(argc, argv);
  Vcensus_test* census_dut = new Vcensus_test;
  int tick = 0;
  int cycle = 0;

  std::cout << "Testing census transformer..... ";

  while(!Verilated::gotFinish() && cycle <= kResetCycles+2) {
    census_dut->eval();
    census_dut->clk = tick%2 == 0;
    if (tick%2) cycle++;
    tick++;
    if (!(tick%2 == 0)) continue;

    if ( cycle <= 1 ) {
      census_dut->rst = 1;
      continue;
    } else {
      census_dut->rst = 0;
    }

    if ( cycle <= kResetCycles ) {
      for(int i = 0; i < kWidth*kHeight; i++) {
        census_dut->inp[i] = 0;
        assert(census_dut->outp == 0);
      }
      continue;
    }

    if (cycle == kResetCycles + 1) {
      for(int i = 0; i < kWidth*kHeight; i++) {
        census_dut->inp[i] = i;
      }
    }

    if(cycle == kResetCycles + 2) {
      assert(census_dut->outp == (1<<(kWidth*kHeight/2))-1);
    }


  }
  std::cout << "Test PASSED!\n";
  exit(0);
}
