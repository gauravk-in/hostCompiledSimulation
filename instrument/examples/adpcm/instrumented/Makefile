include ../../../../cache_simulator/Makefile.macros

CC=gcc
CFLAGS=-O2 -std=c99
INCLUDE=-I$(CSIM_DIR)/src

APP_SOURCES = my_ctop_IR.c adpcm_IR.c

all: my_ctop_IR.out

my_ctop_IR.out: $(SOURCES) $(APP_SOURCES)
	$(CC) $(CFLAGS) $(INCLUDE) -o $@ $^

clean: 
	rm -rf *.o cacheSimTest 
	for f in $(SOURCES); do \
		rm -rf $$f; \
	done