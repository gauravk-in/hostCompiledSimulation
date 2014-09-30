#
# Makefile for adpcm and test programs
# -------------------

include ../../Makefile.macros

APP1 = test_memory

TREEDUMP = -fdump-tree-all-blocks-details
OPT = -O1 -g #is O3 in original MiBench download. Use O3 for final testing
DEBUG = -g
IRDUMP = 1 #defined - dump IR files, undefined - don't.
#PRINT = 1 #if defined and PHASE defined, include soft-float lib. fprintf uses floating point

ifdef PHASE
  CC = $(CROSS_GCC)
  OBJDUMP = $(CROSS_OBJDUMP)
  OEXT = elf
  #ifeq (${IRDUMP},1)
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
  #ifeq (${IRDUMP}, 1)
  ifdef IRDUMP
    COPTS = -static ${OPT} 
  else
    COPTS = -static ${OPT}
  endif
endif

FILE1 = ${APP1}.c main.c
OFILE1 = ${APP1}

OBJDIR = .

all: test_memory objdump_test_memory

test:
	./$(OFILE1).${OEXT}

test_memory: ${FILE1}
	$(CC) $(COPTS) $^ -o ${OFILE1}.${OEXT}

objdump_test_memory: ${OFILE1}
	${OBJDUMP} -D $^.${OEXT} >& ${OBJDIR}/${APP1}.objdump

clean:
	-rm -rf *.${OEXT} ${OBJDIR}/*.objdump *.c.* test_memory
