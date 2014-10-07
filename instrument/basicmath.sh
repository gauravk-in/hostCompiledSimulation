#!/bin/sh

python instrument.py -i examples/basicmath/basicmath_small_truncated3_IR.c -i examples/basicmath/cubic_IR.c -i examples/basicmath/debug.h -i examples/basicmath/ir2c.h -i examples/basicmath/isqrt_IR.c -i examples/basicmath/my_math_IR.c -i examples/basicmath/pi.h -i examples/basicmath/rad2deg_IR.c -i examples/basicmath/round.h -i examples/basicmath/snipmath.h -i examples/basicmath/sniptype.h -o examples/basicmath/basicmath_small_truncated3_IR_my_math.objdump -b examples/basicmath/basicmath_small_truncated3_IR_my_math.elf -p examples/basicmath/instrumented/
