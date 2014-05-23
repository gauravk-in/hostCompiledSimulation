include ../../Makefile.macros

APP1 = crc_top

#PHASE = final #when not defined, CC = gcc. otherwise cc = ppc-gcc

TREEDUMP = -fdump-tree-all-blocks-details
OPT = -O2 #is O3 in original MiBench download. Use O3 for final testing
DEBUG = -g
IRDUMP = 1 #1 - dump IR files, 0 - don't.
#PRINT = 1 #if defined and PHASE defined, include soft-float lib. fprintf uses floating point

ifdef PHASE
  CC = $(CROSS_GCC)
  OBJDUMP = $(CROSS_OBJDUMP)
  OEXT = elf
  #ifeq (${IRDUMP},1)
  ifdef IRDUMP
    COPTS = -static ${OPT} ${TREEDUMP}
  else
    COPTS = -static ${OPT}
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

FILE1 = crc_32.c ${APP1}.c
OFILE1 = ${APP1}.${OEXT}
OFILE1PRINT = ${APP1}_print.${OEXT}

OBJDIR = .

all: crc_print crc objdump_crc_print objdump_crc

test:
	./${OFILE1}
	./$(OFILE1PRINT)

crc: ${FILE1}
	${CC} ${COPTS} $^ -o ${OFILE1}
objdump_crc: ${OFILE1}
	${OBJDUMP} -D $^ >& ${APP1}.objdump
crc_print: ${FILE1}
	${CC} ${COPTS} -DPRINT_RESULTS $^ -o ${OFILE1PRINT}
objdump_crc_print: ${OFILE1PRINT}
	${OBJDUMP} -D $^ >& ${APP1}_print.objdump

clean:
	rm -rf *.${OEXT} *.objdump *.c.* output*
