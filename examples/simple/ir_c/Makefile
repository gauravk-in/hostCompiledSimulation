# Makefile to compile the C Example code
# make all - generates the debug information, and binary code for all the
#			examples in the folder.
include ../../Makefile.macros

TREEDUMP = -fdump-tree-all-blocks-details
OPT = -O2 #is O3 in original MiBench download. Use O3 for final testing
DEBUG = -g
#IRDUMP = 1 #defined - dump IR files, undefined - don't.
#PRINT = 1 #if defined and PHASE defined, include soft-float lib. fprintf uses floating point

ifdef PHASE
  CC = $(CROSS_GCC)
  OBJDUMP = $(CROSS_OBJDUMP)
  OEXT = elf
  
  ifdef IRDUMP
    COPTS = -static ${OPT} ${TREEDUMP} -T generic-hosted.ld
  else
    COPTS = -static ${OPT} -T generic-hosted.ld
  endif
 
  ifdef PRINT
    COPTS += -msoft-float
  endif
else
  CC = $(GCC)
  OBJDUMP = $(HOST_OBJDUMP)
  OEXT = out
  
  ifdef IRDUMP
    COPTS = -static ${OPT} 
  else
    COPTS = -static ${OPT}
  endif
endif

APP1 = simple_IR

all: simple_IR.$(OEXT) simple_IR.objdump

simple_IR.$(OEXT): simple_IR.c
	$(CC) $(COPTS) -o $@ $^
        
simple_IR.objdump: simple_IR.$(OEXT)
	${OBJDUMP} -D $^ >& ${APP1}.objdump


test:
		
clean:
	rm -rf *.o *.c.* simple_IR.elf simple_IR.out simple_IR.objdump
