include ../../../../cache_simulator/Makefile.macros
include ../../../../branch_predictor/Makefile.macros

CC = gcc
CFLAGS = -O2 -std=c99
INCLUDE = -I$(CACHESIM_HEADERS) -I$(BPRED_HEADERS)
LIB = -L$(CACHESIM_LIB) -L$(BPRED_LIB)

APP_SOURCES = basicmath_small_truncated3_IR.c cubic_IR.c isqrt_IR.c my_math_IR.c rad2deg_IR.c 

all: basicmath.out

basicmath.out: $(APP_SOURCES)
	$(CC) $(CFLAGS) $(INCLUDE) $(LIB) -o $@ $^ -lcacheSim -lbranchPred

clean: 
	rm -rf *.o basicmath.out 
