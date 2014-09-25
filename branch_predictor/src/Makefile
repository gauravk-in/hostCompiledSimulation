include ../Makefile.macros

GCC = gcc
CFLAGS = -O3

HEADERS = $(BPRED_HEADERS)

# Cache Simulation Source Code
SOURCES = branchPred.c $(HEADERS)/branchPred.h
OBJECTS = branchPred.o

all: branchPred

branchPred: $(SOURCES)
	$(GCC) $(CFLAGS) -c -Wall -Werror -fpic $^
	$(GCC) -shared -o lib$@.so $(OBJECTS)
	
clean:
	rm -rf *.o libbranchPred.so