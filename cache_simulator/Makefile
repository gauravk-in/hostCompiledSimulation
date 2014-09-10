# Makefile for cache simulator
include Makefile.macros

SRC = src
LIB = $(CACHESIM_LIB)

INSTALL = cp

all: cacheSim

cacheSim: 
	$(MAKE) -C $(SRC)
	$(INSTALL) $(SRC)/libcacheSim.so $(LIB)
	
clean:
	rm -rf *.o
	rm -rf $(LIB)/cacheSim.so