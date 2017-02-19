SHELL = /bin/bash

TESTS = basic_test

check: $(TESTS)

# Arguments to pass to Verilator
OBJ_DIR = obj_dir
GEN_DIR = generated
VARGS = -Wall -I../lib -I../census -I$(GEN_DIR)

argmin_40.v: ../census/argmin_helper.v ../census/argmin_stage.v ../census/argmin_gen.py
	mkdir -p $(GEN_DIR)
	python3 ../census/argmin_gen.py --num_inputs=40 > $(GEN_DIR)/argmin_40.v

pop_count_400.v: ../census/pop_count_gen.py
	mkdir -p $(GEN_DIR)
	python3 ../census/pop_count_gen.py --width=400 > $(GEN_DIR)/pop_count_9.v

basic_test: census_basic.v argmin_40.v pop_count_400.v basic_test.cpp
	verilator $(VARGS) -cc census_basic.v --exe basic_test.cpp
	make -j -f Vcensus_basic.mk -C $(OBJ_DIR)
	$(OBJ_DIR)/Vcensus_basic left_img right_img > $(GEN_DIR)/out.dat


clean: 
	rm -rf $(OBJ_DIR)
	rm -rf $(GEN_DIR)
