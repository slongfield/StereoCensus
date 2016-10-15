/*  Simple sanity test for the FIFO.
 * 
 *  If this test doesn't pass, it means that something is wrong with your 
 *  installation of Verilog, Cpp, or Make.
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

#include "Vfifo_test.h"
#include "verilated.h"

int main(int argc, char **argv, char **env) {
  Verilated::commandArgs(argc, argv);
  Vfifo_test* fifo_dut = new Vfifo_test;
  int tick = 0;
  int cycle = 0;

  std::cout << "Testing basic FIFO..... ";
  while(!Verilated::gotFinish() && cycle < 20) {
    fifo_dut->clk = tick%2 == 0;
    if (tick%2) cycle++;
    tick++;

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
    
    // On the 4th cycle, put in 4. Since the FIFO is 10 elements long, it 
    // should be visible on the output on the 14th cycle.
    fifo_dut->inp = 0;
    if (cycle == 4) {
      fifo_dut->inp = 4;
    } else if (cycle == 14) {
      assert(fifo_dut->outp == 4);
    } else {
      assert(fifo_dut->outp == 0);
    }
  
    fifo_dut->eval();
  }
  std::cout << "Test PASSED!\n";
  exit(0);
}
