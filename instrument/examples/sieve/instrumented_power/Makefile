include ../../../../cache_simulator/Makefile.macros
include ../../../../branch_predictor/Makefile.macros
include ../../../../power_estimator/Makefile.macros

CC = gcc
CFLAGS = -O2 -std=c99
INCLUDE = -I$(CACHESIM_HEADERS) -I$(BPRED_HEADERS) -I$(POWEREST_HEADERS)
LIB = -L$(CACHESIM_LIB) -L$(BPRED_LIB) -L$(POWEREST_LIB)

APP_SOURCES = erat_sieve_no_print_IR.c

all: sieve.out

sieve.out: $(APP_SOURCES)
	$(CC) $(CFLAGS) $(INCLUDE) $(LIB) -o $@ $^ -lcacheSim -lbranchPred -lpowerEst

clean: 
	rm -rf *.o cacheSimTest 
	for f in $(SOURCES); do \
		rm -rf $$f; \
	done
