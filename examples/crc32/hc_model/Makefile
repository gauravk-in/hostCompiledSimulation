APP1 = crc_top_IR_hc

#PHASE = final #when not defined, CC = gcc. otherwise cc = ppc-gcc

TREEDUMP = #-fdump-tree-all-blocks-details
OPT = -O2 #is O3 in original MiBench download. Use O3 for final testing
DEBUG = -g
#IRDUMP = 1 #1 - dump IR files, 0 - don't.

ifdef PHASE
  CC = /home/unga/suhas/powerpc-elf/bin/powerpc-elf-gcc
  OBJDUMP = /home/unga/suhas/powerpc-elf/bin/powerpc-elf-objdump
  OEXT = elf
  #ifeq (${IRDUMP},1)
  ifdef IRDUMP
    COPTS = -static -msim ${OPT} ${TREEDUMP} -I.
  else
    COPTS = -static -msim ${OPT} -I.
  endif
else
  CC = gcc
  OBJDUMP = objdump
  OEXT = out
  #ifeq (${IRDUMP}, 1)
  ifdef IRDUMP
    COPTS = -static ${OPT} -I../../../ir2c/include
  else
    COPTS = -static ${OPT} -I../../../ir2c/include
  endif
endif

FILE1 = crc_32_IR_hc.c ${APP1}.c 
FILE2 = crc_32_IR_hc.c ${APP1}_print.c
OFILE1 = ${APP1}.${OEXT}
OFILE2 = ${APP1}_print.${OEXT}

OBJDIR = .

SED=sed

all: crc crc_print

test:
	./${OFILE1}
	./${OFILE2}

crc: ${FILE1}
	${CC} ${COPTS} $^ -o ${OFILE1}
objdump_crc: ${OFILE1}
	${OBJDUMP} -D $^ >& ${OBJDIR}/${APP1}.objdump
crc_print: ${FILE2}
	${CC} ${COPTS} $^ -o ${OFILE2}
objdump_crc_print: ${OFILE2}
	${OBJDUMP} -D $^ >& ${OBJDIR}/${APP1}_print.objdump

crc_top_IR_hc_print.c: crc_top_IR_hc.c
	$(SED) -e 's|return \(.*\) != 0;|printf ("\\nMetrics: Total Cycles %ld, Total Energy %f J\\n", Cycle_count, Energy_count);\n  return \1 != 0;|' < $< > $@

clean:
	rm -rf *.${OEXT} ${OBJDIR}/*.objdump *.c.* output*
