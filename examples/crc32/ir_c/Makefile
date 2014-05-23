APP1 = crc_top_IR

#PHASE = final #when not defined, CC = gcc. otherwise cc = ppc-gcc

TREEDUMP = #-fdump-tree-all-blocks-details
OPT = -O2 #is O3 in original MiBench download. Use O3 for final testing
DEBUG = -g
IRDUMP = 1 #1 - dump IR files, 0 - don't.

ifdef PHASE
  CC = powerpc-elf-gcc
  OBJDUMP = powerpc-elf-objdump
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

FILE1 = crc_32_IR.c ${APP1}.c 
OFILE1 = ${APP1}.${OEXT}

OBJDIR = .

all: crc objdump_crc

test:
	./${OFILE1}

crc: ${FILE1}
	${CC} ${COPTS} $^ -o ${OFILE1}
objdump_crc: ${OFILE1}
	${OBJDUMP} -D $^ >& ${APP1}.objdump

clean:
	rm -rf *.${OEXT} *.objdump *.c.* output*
