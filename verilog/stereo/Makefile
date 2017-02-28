SHELL = /bin/bash

TESTS = basic_test gen_test

check: $(TESTS)

# Arguments to pass to Verilator
OBJ_DIR = obj_dir
GEN_DIR = generated
VARGS = -Wall -I../lib -I../census -I$(GEN_DIR)

argmin_40.v: ../census/argmin_helper.v ../census/argmin_stage.v ../census/argmin_gen.py
	mkdir -p $(GEN_DIR)
	python3 ../census/argmin_gen.py --num_inputs=40 > $(GEN_DIR)/argmin_40.v

argmin_100.v: ../census/argmin_helper.v ../census/argmin_stage.v ../census/argmin_gen.py
	mkdir -p $(GEN_DIR)
	python3 ../census/argmin_gen.py --num_inputs=100 > $(GEN_DIR)/argmin_100.v

pop_count_9.v: ../census/pop_count_gen.py
	mkdir -p $(GEN_DIR)
	python3 ../census/pop_count_gen.py --width=400 > $(GEN_DIR)/pop_count_9.v

pop_count_7.v: ../census/pop_count_gen.py
	mkdir -p $(GEN_DIR)
	python3 ../census/pop_count_gen.py --width=100 > $(GEN_DIR)/pop_count_7.v

test_data:
	./to_dat.py ../data/cones/im2.png > $(GEN_DIR)/right
	./to_dat.py ../data/cones/im6.png > $(GEN_DIR)/left

basic_test: census_basic.v argmin_40.v pop_count_9.v basic_test.cpp test_data
	verilator $(VARGS) -cc census_basic.v --exe basic_test.cpp
	make -j -f Vcensus_basic.mk -C $(OBJ_DIR)
	$(OBJ_DIR)/Vcensus_basic $(GEN_DIR)/left $(GEN_DIR)/right	> $(GEN_DIR)/out.dat
	./from_dat.py -w 450 -i $(GEN_DIR)/out.dat --scale=4 --offset=410 -o $(GEN_DIR)/basic.png

stereo.v: census_gen.py 
	./census_gen.py -b 8 -d 100 -h 20 -w 20 -l 450 > $(GEN_DIR)/stereo.v

gen_test: stereo.v argmin_100.v pop_count_9.v gen_test.cpp test_data
	verilator $(VARGS) -cc $(GEN_DIR)/stereo.v --exe gen_test.cpp
	make -j -f Vstereo.mk -C $(OBJ_DIR)
	$(OBJ_DIR)/Vstereo $(GEN_DIR)/left $(GEN_DIR)/right	> $(GEN_DIR)/gen_out.dat
	./from_dat.py -w 450 -i $(GEN_DIR)/gen_out.dat --scale=4 --offset=410 -o $(GEN_DIR)/gen.png

gen_test_100: argmin_100.v pop_count_7.v gen_test.cpp test_data
	./census_gen.py -b 8 -d 100 -h 10 -w 10 -l 450 > $(GEN_DIR)/stereo.v
	verilator $(VARGS) -cc $(GEN_DIR)/stereo.v --exe gen_test.cpp
	make -j -f Vstereo.mk -C $(OBJ_DIR)
	$(OBJ_DIR)/Vstereo $(GEN_DIR)/left $(GEN_DIR)/right	> $(GEN_DIR)/gen_out.dat
	./from_dat.py -w 450 -i $(GEN_DIR)/gen_out.dat --scale=4 --offset=410 -o $(GEN_DIR)/gen_100.png


clean: 
	rm -rf $(OBJ_DIR)
	rm -rf $(GEN_DIR)
