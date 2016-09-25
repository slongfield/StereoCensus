SHELL = /bin/bash

TESTS = fifo_test

check: $(TESTS)

# Arguments to pass to Verilator
VARGS = -Wall 
OBJ_DIR = obj_dir

fifo_test: fifo_test.v fifo_test.cpp
	verilator $(VARGS) -cc fifo_test.v --exe fifo_test.cpp
	make -j -f Vfifo_test.mk  -C $(OBJ_DIR)
	$(OBJ_DIR)/Vfifo_test

clean:
	rm -rf $(OBJ_DIR)
