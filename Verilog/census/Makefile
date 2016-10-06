SHELL = /bin/bash

TESTS = census_test

check: $(TESTS)

# Arguments to pass to Verilator
VARGS = -Wall -I../lib
OBJ_DIR = obj_dir

census_test: census_test.v census_test.cpp
	verilator $(VARGS) -cc census_test.v --exe census_test.cpp
	make -j -f Vcensus_test.mk  -C $(OBJ_DIR)
	$(OBJ_DIR)/Vcensus_test

clean:
	rm -rf $(OBJ_DIR)
