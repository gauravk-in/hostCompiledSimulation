#
# Makefile for adpcm and test programs
# -------------------

######################################################################
#CFLAGS = -static -O3

APP1 = my_ctop_IR_hc

#PHASE = final #when not defined, CC = gcc. otherwise cc = ppc-gcc

TREEDUMP = -fdump-tree-all-blocks-details
OPT = -g -O2 #is O3 in original MiBench download. Use O3 for final testing
DEBUG = -g
#OPT = ${DEBUG} - turn this on when need to debug
#IRDUMP = 1 #defined - dump IR files, undefined - don't.
#PRINT = 1 #if defined and PHASE defined, include soft-float lib. fprintf uses floating point

ifdef PHASE
  CC = /home/unga/suhas/powerpc-elf/bin/powerpc-elf-gcc
  OBJDUMP = /home/unga/suhas/powerpc-elf/bin/powerpc-elf-objdump
  OEXT = elf
  #ifeq (${IRDUMP},1)
  ifdef IRDUMP
    COPTS = -static -msim ${OPT} ${TREEDUMP}
  else
    COPTS = -static -msim ${OPT}
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
    COPTS = -static ${OPT} ${TREEDUMP} -I../../../ir2c/include
  else
    COPTS = -static ${OPT} -I../../../ir2c/include
  endif
endif

FILE1 = ${APP1}.c adpcm_IR_hc.c
FILE1PRINT = ${APP1}_print.c adpcm_IR_hc.c
#FILE1 = ${APP1}.c adpcm_IR_hc_bb6_correction_debug_prints.c
OFILE1 = ${APP1}.${OEXT}
OFILE1PRINT = ${APP1}_print.${OEXT}

OBJDIR = .

SED=sed

all: my_ctest my_ctest_print

test:
	./$(OFILE1)
	./$(OFILE1PRINT)

my_ctest: ${FILE1}
	$(CC) $(COPTS) $^ -o ${OFILE1}

my_ctest_print: ${FILE1PRINT}
	$(CC) $(COPTS) $^ -o ${OFILE1PRINT}

objdump_my_ctest: ${OFILE1}
	${OBJDUMP} -D $^ >& ${OBJDIR}/${APP1}.objdump

my_ctop_IR_hc_print.c: my_ctop_IR_hc.c
	$(SED) -e 's|return 0;|printf ("\\nMetrics: Total Cycles %ld, Total Energy %f J\\n", Cycle_count, Energy_count);\n  return 0;|' < $< > $@

clean:
	-rm -rf *.${OEXT} ${OBJDIR}/*.objdump *.c.*
