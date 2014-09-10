include ../Makefile.macros

CC = gcc
CFLAGS = -O2 -std=c99
INCLUDE = -I$(CACHESIM_HEADERS)
LIB = -L$(CACHESIM_LIB)

TEST_SOURCES = cacheSimTest.c

all: cacheSimTest

cacheSimTest: $(TEST_SOURCES)
	$(CC) $(CFLAGS) $(INCLUDE) $(LIB) -o $@ $^ -lcacheSim	

clean: 
	rm -rf *.o cacheSimTest 