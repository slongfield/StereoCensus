/*  Test for the population counter.
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

#include "Vpop_count_test.h"
#include "verilated.h"

int kResetCycles = 3;
int main(int argc, char **argv, char **env) {
  Verilated::commandArgs(argc, argv);
  Vpop_count_test* pop_count_dut = new Vpop_count_test;
  int tick = 0;
  int cycle = 0;

  std::cout << "Testing pop_count transformer..... ";

  while(!Verilated::gotFinish() && cycle <= kResetCycles+6) {
    pop_count_dut->eval();
    pop_count_dut->clk = tick%2 == 0;
    if (tick%2) cycle++;
    tick++;
    if (!(tick%2 == 0)) continue;

    if ( cycle <= 1 ) {
      pop_count_dut->rst = 1;
      continue;
    } else {
      pop_count_dut->rst = 0;
    }

    if ( cycle <= kResetCycles ) {
      pop_count_dut->inp = 0;
      assert(pop_count_dut->outp == 0);
      continue;
    }

    // 7 = 0b111 = 3
    if (cycle == kResetCycles + 1) {
      pop_count_dut->inp = 7;
      assert(pop_count_dut->outp == 0);
    }

    // 111 = 0b1101111 = 6
    if (cycle == kResetCycles + 2) {
      pop_count_dut->inp = 111;
      assert(pop_count_dut->outp == 3);
    }

    // 42 = 0b101010 = 3
    if (cycle == kResetCycles + 3) {
      pop_count_dut->inp = 42;
      assert(pop_count_dut->outp == 6);
    }

    // 1234 = 0b10011010010 = 5
    if (cycle == kResetCycles + 4) {
      pop_count_dut->inp = 1234;
      assert(pop_count_dut->outp == 3);
    }

    if (cycle == kResetCycles + 5) {
      pop_count_dut->inp = 0;
      assert(pop_count_dut->outp == 5);
    }

  }
  std::cout << "Test PASSED!\n";
  exit(0);
}
