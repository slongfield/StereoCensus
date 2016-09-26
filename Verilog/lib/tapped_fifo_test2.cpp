/*  Wide test for the tapped FIFO.
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

// TODO(slongfield): Use GoogleTest or some other testing framework to clean
//  this up.


#include <iostream>

#include "Vtapped_fifo_test2.h"
#include "verilated.h"

int main(int argc, char **argv, char **env) {
  Verilated::commandArgs(argc, argv);
  Vtapped_fifo_test2* fifo_dut = new Vtapped_fifo_test2;
  int tick = 0;
  int cycle = 0;

  std::cout << "Testing wide tapped FIFO..... ";
  while(!Verilated::gotFinish() && cycle < 20) {
    fifo_dut->clk = tick%2 == 0;
    if (tick%2) cycle++;
    tick++;

    /* DEBUG. Cleanup.
    if (tick%2) {
      std::cout << "Cycle: " << cycle << " Taps: ";
      for (int i = 0; i < 10; i++)
        std::cout << fifo_dut->taps[i];
      std::cout << "\n";
    }
    */

    if ( cycle <= 1 ) {
      fifo_dut->rst = 1;
      continue;
    } else {
      fifo_dut->rst = 0;
    }

    if ( cycle <= 3 ) {
      fifo_dut->inp = 0;
      assert(fifo_dut->outp == 0);
      continue;
    }
    
    // On the 4th cycle, put in 1. Next few cycles, should see this shifting
    // over on the tap output.
    fifo_dut->inp = 0;
    if (cycle == 4) {
      fifo_dut->inp = 1;
    } else if (cycle > 4 && cycle < 14) {
      assert(fifo_dut->taps[10-(cycle-4)] == 1);
    } else if (cycle == 14) {
      assert(fifo_dut->outp == 1);
    } else {
      assert(fifo_dut->outp == 0);
    }
  
    fifo_dut->eval();
  }
  std::cout << "Test PASSED!\n";
  exit(0);
}
