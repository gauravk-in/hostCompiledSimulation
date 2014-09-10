include ../../../../cache_simulator/Makefile.macros

CC = gcc
CFLAGS = -O2 -std=c99
INCLUDE = -I$(CACHESIM_HEADERS)
LIB = -L$(CACHESIM_LIB)

APP_SOURCES = erat_sieve_no_print_IR.c

all: sieve.out

sieve.out: $(APP_SOURCES)
	$(CC) $(CFLAGS) $(INCLUDE) $(LIB) -o $@ $^ -lcacheSim

clean: 
	rm -rf *.o cacheSimTest 
	for f in $(SOURCES); do \
		rm -rf $$f; \
	done