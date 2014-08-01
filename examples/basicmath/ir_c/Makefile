include ../../Makefile.macros

APP1 = basicmath_small_IR
APP1PRINT = basicmath_small_print
APP2 = basicmath_large
DEBUGAPP = basicmath_small_debug
TRUNCAPP1 = basicmath_small_truncated3_IR

#PHASE = final #when not defined, CC = gcc. otherwise cc = ppc
MATH = my_math #when libsource, COPTS is as per lib source compilation. Uncomment paths, VPATH in that case

TREEDUMP = -fdump-tree-all-blocks-details
OPT = -O1 #is O3 in original MiBench download. Use O3 for final testing
DEBUG = -g

ifdef PHASE
  CC = $(CROSS_GCC)
  OBJDUMP = $(CROSS_OBJDUMP)
  OEXT = elf
  ifeq (${MATH}, libsource)
    COPTS = -D_IEEE_LIBM -D__IEEE_BIG_ENDIAN -I${MY_MPATH2} -I${MY_MPATH3} -static -msoft-float ${OPT} ${TREEDUMP} -I. -T generic-hosted.ld
  else
    COPTS = -static -msoft-float ${OPT} ${TREEDUMP} -I. -T generic-hosted.ld
  endif
else
  CC = $(GCC)
  OBJDUMP = $(HOST_OBJDUMP)
  OEXT = out
  ifeq (${MATH}, libsource)
    COPTS = -D_IEEE_LIBM -D__IEEE_LITTLE_ENDIAN -I${MY_MPATH2} -I${MY_MPATH3} -static ${OPT} -I../../../include -I../../../ir2c/include
  else
    COPTS = -static ${OPT} -I../../../include -I../../../ir2c/include
  endif
endif

FILE1 = ${APP1}.c   rad2deg.c  cubic.c   isqrt.c
FILE1MYMATH = ${APP1}.c   rad2deg.c  cubic.c   isqrt.c my_math.c
TRUNCFILE1MYMATH = ${TRUNCAPP1}.c   rad2deg_IR.c  cubic_IR.c   isqrt_IR.c my_math_IR.c
FILE1PRINT = ${APP1PRINT}.c rad2deg.c  cubic.c   isqrt.c my_math.c
FILE2 = ${APP2}.c   rad2deg.c  cubic.c   isqrt.c
OFILE1 = ${APP1}_w_math_sources.${OEXT}
OFILE1WSOURCES = ${APP1}_w_math_sources.${OEXT}
OFILE1MYMATH = ${APP1}_my_math.${OEXT}
TRUNCOFILE1MYMATH = ${TRUNCAPP1}_my_math.${OEXT}
OFILE1PRINT = ${APP1PRINT}.${OEXT}
OFILE2 = ${APP2}.${OEXT}

DEBUGFILE1 = ${DEBUGAPP}.c rad2deg.c  cubic_debug.c   isqrt.c
DEBUGOFILE1 = ${DEBUGAPP}.${OEXT}

OBJDIR = .

#### mathlib source paths and names
#MY_MPATH1=/home/local/grimlock/suhas/libm_some_sources/math
#MY_MPATH2=/home/local/grimlock/suhas/libm_some_sources/common
#MY_MPATH3=/home/local/grimlock/suhas/libm_some_sources/libc/include

#search path for math source files - 7 Oct12, no longer needed as
#source files are in current directory
#VPATH=${MY_MPATH1}:${MY_MPATH2}

MATHFILES1 = w_acos.c s_cos.c w_pow.c w_sqrt.c
MATHFILES2 = e_acos.c e_pow.c e_sqrt.c k_cos.c k_sin.c e_rem_pio2.c k_rem_pio2.c
MATHFILES3 = s_scalbn.c s_floor.c s_copysign.c s_fabs.c s_nan.c

all: basicmath_small_my_math_trunc objdump_small_my_math_trunc

test:
	./$(TRUNCOFILE1MYMATH)

full: basicmath_small basicmath_small_my_math basicmath_small_my_math_trunc basicmath_small_print basicmath_small_w_math_sources basicmath_large objdump_small objdump_small_my_math objdump_small_my_math_trunc objdump_small_w_math_sources objdump_large

#the _w_math_sources target uses source files of the newlib math library( libm)
basicmath_small: ${FILE1}
	${CC} ${COPTS} $^ -o ${OFILE1} -lm
basicmath_small_my_math: ${FILE1MYMATH}
	${CC} ${COPTS} $^ -o ${OFILE1MYMATH}
basicmath_small_my_math_trunc: ${TRUNCFILE1MYMATH}
	${CC} ${COPTS} $^ -o ${TRUNCOFILE1MYMATH}
basicmath_small_w_math_sources: ${FILE1} ${MATHFILES1} ${MATHFILES2} ${MATHFILES3}
	${CC} ${COPTS} $^ -o ${OFILE1WSOURCES}
basicmath_small_print: ${FILE1PRINT}
	${CC} ${COPTS} $^ -o ${OFILE1PRINT} 
basicmath_large: ${FILE2} Makefile
	${CC} ${COPTS} ${FILE2} -o ${OFILE2} -lm
objdump_small: ${OFILE1}
	${OBJDUMP} -D ${OFILE1} >& ${OBJDIR}/${APP1}./objdump
objdump_small_my_math: ${OFILE1MYMATH}
	${OBJDUMP} -D ${OFILE1MYMATH} >& ${OBJDIR}/${APP1}_my_math.objdump
objdump_small_my_math_trunc: ${TRUNCOFILE1MYMATH}
	${OBJDUMP} -D ${TRUNCOFILE1MYMATH} >& ${OBJDIR}/${TRUNCAPP1}_my_math.objdump
objdump_small_w_math_sources: ${OFILE1} Makefile
	${OBJDUMP} -D ${OFILE1} >& ${OBJDIR}/${APP1}_w_math_sources.objdump
objdump_small_print: ${OFILE1PRINT}
	${OBJDUMP} -D ${OFILE1PRINT}  >& ${OBJDIR}/${APP1PRINT}.objdump
objdump_large: ${OFILE2} Makefile
	${OBJDUMP} -D ${OFILE2} >& ${OBJDIR}/${APP2}.objdump

#the debug target prints out lookup tables for sqrt, acos, cos and pow
debug: basicmath_small_debug

basicmath_small_debug: ${DEBUGFILE1}
	${CC} ${COPTS} $^ -o ${DEBUGOFILE1} -lm


clean:
	rm -rf *.${OEXT} ${OBJDIR}/*objdump *.c.* 
