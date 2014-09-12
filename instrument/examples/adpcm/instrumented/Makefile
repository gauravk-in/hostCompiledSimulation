include ../../../../cache_simulator/Makefile.macros

CC = gcc
CFLAGS = -O2 -std=c99
INCLUDE = -I$(CACHESIM_HEADERS)
LIB = -L$(CACHESIM_LIB)

APP_SOURCES = my_ctop_IR.c adpcm_IR.c

all: my_ctop_IR.out

my_ctop_IR.out: $(APP_SOURCES)
	$(CC) $(CFLAGS) $(INCLUDE) $(LIB) -o $@ $^ -lcacheSim

check: my_ctop_IR.out
	export LD_LIBRARY_PATH=$(CACHESIM_LIB)
	./my_ctop_IR.out

clean: 
	rm -rf *.o my_ctop_IR.out 
