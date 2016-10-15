SHELL = /bin/bash

TESTS = fifo_test tapped_fifo_test1 tapped_fifo_test2 line_buffer_test

check: $(TESTS)

# Arguments to pass to Verilator
VARGS = -Wall 
OBJ_DIR = obj_dir

fifo_test: fifo_test.v fifo_test.cpp
	verilator $(VARGS) -cc fifo_test.v --exe fifo_test.cpp
	make -j -f Vfifo_test.mk  -C $(OBJ_DIR)
	$(OBJ_DIR)/Vfifo_test

tapped_fifo_test1: tapped_fifo_test1.v tapped_fifo_test1.cpp
	verilator $(VARGS) -cc tapped_fifo_test1.v --exe tapped_fifo_test1.cpp
	make -j -f Vtapped_fifo_test1.mk  -C $(OBJ_DIR)
	$(OBJ_DIR)/Vtapped_fifo_test1

tapped_fifo_test2: tapped_fifo_test2.v tapped_fifo_test2.cpp
	verilator $(VARGS) -cc tapped_fifo_test2.v --exe tapped_fifo_test2.cpp
	make -j -f Vtapped_fifo_test2.mk  -C $(OBJ_DIR)
	$(OBJ_DIR)/Vtapped_fifo_test2

line_buffer_test: line_buffer_test.v line_buffer_test.cpp
	verilator $(VARGS) -cc line_buffer_test.v --exe line_buffer_test.cpp
	make -j -f Vline_buffer_test.mk  -C $(OBJ_DIR)
	$(OBJ_DIR)/Vline_buffer_test

clean:
	rm -rf $(OBJ_DIR)
