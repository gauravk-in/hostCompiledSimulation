#!/bin/sh

python instrument.py -i examples/test_memory/test_memory_IR.c -i examples/test_memory/main_IR.c -i examples/test_memory/ir2c.h -i examples/test_memory/test_data_131072_512k.h -i examples/test_memory/test_data_8192_32k.h -o examples/test_memory/test_memory_IR.objdump -b examples/test_memory/test_memory_IR.elf -p examples/test_memory/instrumented/
