TREEDUMP=-fdump-tree-all-blocks-details

ifdef PHASE

OEXT=.elf
DUMPEXT=objdump

DEBUG=-g
OPT=-O2

CFLAGS=-pedantic -Wcomment -fno-asm -fsigned-char -W -Wparentheses -Wreturn-type -Wswitch -Wunused -Wsign-compare -Wimplicit -Wreturn-type -Wshadow -Wpointer-arith -Wwrite-strings -Wsign-compare -Wstrict-prototypes -Wmissing-prototypes -Wmissing-declarations -msim -msoft-float $(OPT) $(TREEDUMP)

CC=powerpc-elf-gcc

OBJDUMP=powerpc-elf-objdump

else

OEXT=.out
DUMPEXT=objdump

DEBUG=-g
OPT=-O2

CFLAGS=$(OPT)

CC=gcc

OBJDUMP=objdump

endif


all: erat_sieve_no_print erat_sieve_print

test:
	./erat_sieve_print$(OEXT)

erat_sieve_no_print:: erat_sieve_no_print.c
	$(CC) $(CFLAGS) -o $@$(OEXT) $^
	$(OBJDUMP) -D  $@$(OEXT) >& $@.$(DUMPEXT)

erat_sieve_print:: erat_sieve_print.c
	$(CC) $(CFLAGS) -o $@$(OEXT) $^
	$(OBJDUMP) -D  $@$(OEXT) >& $@.$(DUMPEXT)

#adding - to rm so that errors are ignored	
clean::
	@echo Cleaning up massaged IR build
	-rm *$(OEXT) *.objdump erat_sieve_no_print.c.* erat_sieve_print.c.*
