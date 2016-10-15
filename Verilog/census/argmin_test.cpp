/*  Test for the argmin unit.
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

#include "Vargmin_test.h"
#include "verilated.h"

int kResetCycles = 3;
int main(int argc, char **argv, char **env) {
  Verilated::commandArgs(argc, argv);
  Vargmin_test* argmin_dut = new Vargmin_test;
  int tick = 0;
  int cycle = 0;

  std::cout << "Testing argmin transformer..... ";

  while(!Verilated::gotFinish() && cycle <= kResetCycles+20) {
    argmin_dut->eval();
    argmin_dut->clk = tick%2 == 0;
    if (tick%2) cycle++;
    tick++;
    if (!(tick%2 == 0)) continue;

    if ( cycle <= 1 ) {
      argmin_dut->rst = 1;
      continue;
    } else {
      argmin_dut->rst = 0;
    }

    if (cycle > 3) {
      for (int i = 0; i < 10; i++) {
        argmin_dut->inp[i] = (cycle+i)%10;
      }
    }

    // After four cycles of information passing through, should see real data on
    // the output. 
    if (cycle > 7) {
      assert(argmin_dut->outp_addr == (cycle+5) % 10);
    }
  }
  std::cout << "Test PASSED!\n";
  exit(0);
}
