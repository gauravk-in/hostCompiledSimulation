include ../Makefile.macros

CC=gcc
CFLAGS=-O2 -std=c99

TEST_SOURCES = cacheSimTest.c

all: cacheSimTest

cacheSimTest: $(SOURCES) $(TEST_SOURCES)
	$(CC) $(CFLAGS) -o $@ $^

clean: 
	rm -rf *.o cacheSimTest 
	for f in $(SOURCES); do \
		rm -rf $$f; \
	done