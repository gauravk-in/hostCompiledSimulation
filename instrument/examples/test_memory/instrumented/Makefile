include ../../../../cache_simulator/Makefile.macros
include ../../../../branch_predictor/Makefile.macros

CC = gcc
CFLAGS = -O2 -std=c99
INCLUDE = -I$(CACHESIM_HEADERS) -I$(BPRED_HEADERS)
LIB = -L$(CACHESIM_LIB) -L$(BPRED_LIB)

APP_SOURCES = test_memory_IR.c main_IR.c

all: test_memory.out

test_memory.out: $(APP_SOURCES)
	$(CC) $(CFLAGS) $(INCLUDE) $(LIB) -o $@ $^ -lcacheSim -lbranchPred

clean: 
	rm -rf *.o test_memory.out 
	for f in $(SOURCES); do \
		rm -rf $$f; \
	done
