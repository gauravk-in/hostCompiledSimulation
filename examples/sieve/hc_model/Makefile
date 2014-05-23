OEXT=.out
DUMPEXT=objdump

DEBUG=-g
OPT=-O2

CFLAGS=$(OPT) -I../../../ir2c/include

CC=gcc
OBJDUMP=objdump
SED=sed


all: erat_sieve_no_print_IR_hc erat_sieve_print_IR_hc

test:
	./erat_sieve_print_IR_hc$(OEXT)

erat_sieve_no_print_IR_hc:: erat_sieve_no_print_IR_hc.c
	$(CC) $(CFLAGS) -o $@$(OEXT) $^

erat_sieve_print_IR_hc:: erat_sieve_print_IR_hc.c
	$(CC) $(CFLAGS) -o $@$(OEXT) $^

erat_sieve_print_IR_hc.c: erat_sieve_no_print_IR_hc.c
	$(SED) -e 's|return 0;|printf ("\\nMetrics: Total Cycles %ld, Total Energy %f J\\n", Cycle_count, Energy_count);\n  return 0;|' < $< > $@

#adding - to rm so that errors are ignored	
clean::
	@echo Cleaning up massaged IR_hc build
	-rm *$(OEXT) *.objdump
