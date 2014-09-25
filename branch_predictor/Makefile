# Makefile for cache simulator
include Makefile.macros

SRC = $(BPRED_SRC)
LIB = $(BPRED_LIB)

INSTALL = cp

all: branchPred

branchPred: 
	$(MAKE) -C $(SRC)
	$(INSTALL) $(SRC)/lib$@.so $(LIB)
	
clean:
	rm -rf *.o
	rm -rf $(LIB)/libbranchPred.so
