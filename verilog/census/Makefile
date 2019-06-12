SHELL = /bin/bash

TESTS = census_test pop_count_test argmin_test

check: $(TESTS)

# Arguments to pass to Verilator
OBJ_DIR = obj_dir
GEN_DIR = generated
VARGS = -Wall -I../lib -I$(GEN_DIR)

census_test: census_test.v census_test.cpp
	verilator $(VARGS) -cc census_test.v --exe census_test.cpp
	make -j -f Vcensus_test.mk  -C $(OBJ_DIR)
	$(OBJ_DIR)/Vcensus_test

pop_count_7.v: pop_count_gen.py
	mkdir -p $(GEN_DIR)
	../venv/bin/python3 pop_count_gen.py --width=128 > $(GEN_DIR)/pop_count_7.v

pop_count_test: pop_count_test.v pop_count_test.cpp pop_count_7.v
	verilator $(VARGS) -cc pop_count_test.v --exe pop_count_test.cpp
	make -j -f Vpop_count_test.mk  -C $(OBJ_DIR)
	$(OBJ_DIR)/Vpop_count_test

argmin_10.v: argmin_helper.v argmin_stage.v argmin_gen.py
	mkdir -p $(GEN_DIR)
	../venv/bin/python3 argmin_gen.py --num_inputs=10 > $(GEN_DIR)/argmin_10.v

argmin_test: argmin_10.v argmin_test.v argmin_test.cpp
	verilator $(VARGS) -cc argmin_test.v --exe argmin_test.cpp
	make -j -f Vargmin_test.mk -C $(OBJ_DIR)
	$(OBJ_DIR)/Vargmin_test

clean:
	rm -rf $(OBJ_DIR)
	rm -rf $(GEN_DIR)
