# Makefile to compile the C Example code
# make all - generates the debug information, and binary code for all the
#			examples in the folder.

TREEDUMP = -fdump-tree-all-blocks-details
OPT = -O2 #is O3 in original MiBench download. Use O3 for final testing
DEBUG = -g
IRDUMP = 1 #defined - dump IR files, undefined - don't.
#PRINT = 1 #if defined and PHASE defined, include soft-float lib. fprintf uses floating point

ifdef PHASE
  CC = arm-none-linux-gnueabi-gcc
  OBJDUMP = arm-none-linux-gnueabi-objdump
  OEXT = elf
  
  ifdef IRDUMP
    COPTS = -static ${OPT} ${TREEDUMP}
  else
    COPTS = -static ${OPT}
  endif
 
  ifdef PRINT
    COPTS += -msoft-float
  endif
else
  CC = gcc
  OBJDUMP = objdump
  OEXT = out
  
  ifdef IRDUMP
    COPTS = -static ${OPT} 
  else
    COPTS = -static ${OPT}
  endif
endif

all: simple

simple: simple.c
	$(CC) $(COPTS) -o $@.$(OEXT) $^
	
test:
		
clean:
	rm -rf *.o *.c.* simple.elf simple.out