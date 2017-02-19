/*  Test framework for the line buffer.
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

#include "Vline_buffer_test.h"
#include "verilated.h"

int kWindowWidth = 10;
int kLines = 10;
int kLineWidth = 20;
int kResetCycles = 3;

int main(int argc, char **argv, char **env) {
  Verilated::commandArgs(argc, argv);
  Vline_buffer_test* lb_dut = new Vline_buffer_test;
  int tick = 0;
  int cycle = 0;

  std::cout << "Testing line buffer..... ";

  while(!Verilated::gotFinish() && cycle <= kLineWidth*kLines+kResetCycles) {
    lb_dut->eval();
    lb_dut->clk = tick%2 == 0;
    if (tick%2) cycle++;
    tick++;

    if ( cycle <= 1 ) {
      lb_dut->rst = 1;
      continue;
    } else {
      lb_dut->rst = 0;
    }

    if ( cycle <= kResetCycles ) {
      lb_dut->inp = 0;
      assert(lb_dut->outp[0] == 0);
      continue;
    }

    if ( cycle > kResetCycles ) {
      lb_dut->inp = (cycle-kResetCycles);
    }

    int i = 0;
    if ( cycle == kLineWidth*kLines+kResetCycles && tick%2==0 ) {
      for (int line = 0; line < kLines; ++line) {
        for (int col = 0; col < kWindowWidth; ++col) {
          //std::cout << "l " << line << "c " << col << " " << lb_dut->outp[i] << "\n";
          assert(lb_dut->outp[i] == (kLineWidth-kWindowWidth) + kLineWidth*line + col);
          i++;
        }
      }
    }


  }
  std::cout << "Test PASSED!\n";
  exit(0);
}
