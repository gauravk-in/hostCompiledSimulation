include ../../../../cache_simulator/Makefile.macros
include ../../../../branch_predictor/Makefile.macros

CC = gcc
CFLAGS = -O2 -std=c99
INCLUDE = -I$(CACHESIM_HEADERS) -I$(BPRED_HEADERS)
LIB = -L$(CACHESIM_LIB) -L$(BPRED_LIB)

APP_SOURCES = my_mem_IR.c sha_driver_IR.c sha_IR.c

all: sha.out

sha.out: $(APP_SOURCES)
	$(CC) $(CFLAGS) $(INCLUDE) $(LIB) -o $@ $^ -lcacheSim -lbranchPred

clean: 
	rm -rf *.o sha.out
	for f in $(SOURCES); do \
		rm -rf $$f; \
	done
