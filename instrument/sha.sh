#!/bin/sh

python instrument.py -i examples/sha/in_small.h -i examples/sha/ir2c.h -i examples/sha/my_defines.h -i examples/sha/my_mem.h -i examples/sha/my_mem_IR.c -i examples/sha/my_variable.h -i examples/sha/sha_driver_IR.c -i examples/sha/sha.h -i examples/sha/sha_IR.c -o examples/sha/sha_driver_IR.objdump -b examples/sha/sha_driver_IR.elf -p examples/sha/instrumented_power/
