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

APP1 = sha_driver_IR_hc

#PHASE = final #when not defined, CC = gcc. otherwise cc = ppc-gcc

TREEDUMP = -fdump-tree-all-blocks-details
OPT = -O2 #is O3 in original MiBench download. Use O3 for final testing
#OPT += -fno-optimize-sibling-calls #don't optimise for tail calls
DEBUG = -g
##enabling debug
#OPT = -g
#IRDUMP = 1 #1 - dump IR files, 0 - don't.
#PRINT = 1 #if defined and PHASE defined, include soft-float lib. fprintf uses floating point

ifdef PHASE
  CC = /home/unga/suhas/powerpc-elf/bin/powerpc-elf-gcc
  OBJDUMP = /home/unga/suhas/powerpc-elf/bin/powerpc-elf-objdump
  OEXT = elf
  #ifeq (${IRDUMP},1)
  ifdef IRDUMP
    COPTS = -Wall -msim ${OPT} ${TREEDUMP}
  else
    COPTS = -Wall -msim ${OPT} 
  endif

  ifdef PRINT
    COPTS += -msoft-float
  endif

else
  CC = gcc
  OBJDUMP = objdump
  OEXT = out
  #ifeq (${IRDUMP}, 1)
  ifdef IRDUMP
    COPTS = ${OPT} ${TREEDUMP} -I../../../ir2c/include
  else
    COPTS = ${OPT} -I../../../ir2c/include
  endif
endif

FILE1 = ${APP1}.c sha_IR_hc.c my_mem_IR_hc.c
FILE2 = ${APP1}_print.c sha_IR_hc.c my_mem_IR_hc.c
OFILE1 = ${APP1}.${OEXT}
OFILE2 = ${APP1}_print.${OEXT}

OBJDIR = .

SED=sed

all: sha sha_print

test:
	./$(OFILE1)
	./$(OFILE2)

sha: ${FILE1}
	${CC} ${COPTS} $^ -o ${OFILE1}
sha_print: ${FILE2}
	${CC} ${COPTS} $^ -o ${OFILE2}
objdump_sha: ${OFILE1}
	${OBJDUMP} -D $^ >& ${OBJDIR}/${APP1}.objdump
objdump_sha_print: ${OFILE2}
	${OBJDUMP} -D $^ >& ${OBJDIR}/${APP2}.objdump

sha_driver_IR_hc_print.c: sha_driver_IR_hc.c
	$(SED) -e 's|return 0;|printf ("\\nMetrics: Total Cycles %ld, Total Energy %f J\\n", Cycle_count, Energy_count);\n  return 0;|' < $< > $@

clean:
	rm -rf *.${OEXT} ${OBJDIR}/*.objdump *.c.* output*
