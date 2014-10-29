# Makefile for cache simulator
include Makefile.macros

SRC = $(POWEREST_SRC)
LIB = $(POWEREST_LIB)

INSTALL = cp

all: powerEst

powerEst: 
	$(MAKE) -C $(SRC)
	$(INSTALL) $(SRC)/libpowerEst.so $(LIB)
	
clean:
	rm -rf *.o
	rm -rf $(LIB)/libpowerEst.so
