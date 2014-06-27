# By default, the code is compiled for a "big endian" machine.
# To compile on a "little endian" machine set the LITTLE_ENDIAN flag.
# To make smaller object code, but run a little slower, don't use UNROLL_LOOPS.
# To use NIST's modified SHA of 7/11/94, define USE_MODIFIED_SHA

#CC = gcc
#CFLAGS = -O2 -Wall -DLITTLE_ENDIAN

#sha:	sha_driver.o sha.o my_mem.o
#	$(CC) -o $@ sha_driver.o sha.o my_mem.o
#	strip $@

#clean:
#	rm -rf *.o sha output*

include ../../Makefile.macros

APP1 = sha_driver_IR
APP2 = sha_driver_create_input_array_IR

#PHASE = final #when not defined, CC = gcc. otherwise cc = ppc-gcc

TREEDUMP = -fdump-tree-all-blocks-details
OPT = -O2 #is O3 in original MiBench download. Use O3 for final testing
OPT += -fno-optimize-sibling-calls #don't optimise for tail calls, only turn on for ppc
DEBUG = -g
#IRDUMP = 1 #1 - dump IR files, 0 - don't.
#PRINT = 1 #if defined and PHASE defined, include soft-float lib. fprintf uses floating point

ifdef PHASE
  CC = $(CROSS_GCC)
  OBJDUMP = $(CROSS_OBJDUMP)
  OEXT = elf
  #ifeq (${IRDUMP},1)
  ifdef IRDUMP
    COPTS = -Wall ${OPT} ${TREEDUMP} -I. -T generic-hosted.ld
  else
    COPTS = -Wall ${OPT} -I. -T generic-hosted.ld
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
    COPTS = ${OPT} -I../../../ir2c/include
  else
    COPTS = ${OPT} -I../../../ir2c/include
  endif
endif

FILE1 = ${APP1}.c sha_IR.c my_mem_IR.c
FILE2 = ${APP2}.c sha_create_input_array_IR.c my_mem_IR.c
OFILE1 = ${APP1}.${OEXT}
OFILE2 = ${APP2}.${OEXT}

OBJDIR = .

all: sha objdump_sha

test:
	./$(OFILE1)

sha: ${FILE1}
	${CC} ${COPTS} $^ -o ${OFILE1}
sha_create_array: ${FILE2}
	${CC} ${COPTS} $^ -o ${OFILE2}
objdump_sha: ${OFILE1}
	${OBJDUMP} -D $^ >& ${OBJDIR}/${APP1}.objdump
objdump_sha_create_array: ${OFILE2}
	${OBJDUMP} -D $^ >& ${OBJDIR}/${APP2}.objdump

clean:
	rm -rf *.${OEXT} ${OBJDIR}/*.objdump *.c.* output*
