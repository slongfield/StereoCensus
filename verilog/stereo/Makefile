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

pop_count_9.v: ../census/pop_count_gen.py
	mkdir -p $(GEN_DIR)
	python3 ../census/pop_count_gen.py --width=400 > $(GEN_DIR)/pop_count_9.v

basic_test: census_basic.v argmin_40.v pop_count_9.v basic_test.cpp
	verilator $(VARGS) -cc census_basic.v --exe basic_test.cpp
	make -j -f Vcensus_basic.mk -C $(OBJ_DIR)
	./to_dat.py ../data/cones/im2.png > $(GEN_DIR)/right
	./to_dat.py ../data/cones/im6.png > $(GEN_DIR)/left
	$(OBJ_DIR)/Vcensus_basic $(GEN_DIR)/left $(GEN_DIR)/right	> $(GEN_DIR)/out.data
	./from_dat.py -w 450 -i $(GEN_DIR)/out.dat --scale=4 --offset=40 -o $(GEN_DIR)/basic.png

census_gen.v: census_gen.py

# max_disparty: 100
# window size: 19x19
gen_test: census_gen.v 


clean: 
	rm -rf $(OBJ_DIR)
	rm -rf $(GEN_DIR)
