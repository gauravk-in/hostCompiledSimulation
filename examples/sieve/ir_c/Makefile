include ../../Makefile.macros

#TREEDUMP = -fdump-tree-all-blocks-details
OPT = -g -O1 #is O3 in original MiBench download. Use O3 for final testing
DEBUG = -g
IRDUMP = 0 #defined - dump IR files, undefined - don't.
#PRINT = 1 #if defined and PHASE defined, include soft-float lib. fprintf uses floating point

DUMPEXT = objdump

ifdef PHASE
  CC = $(CROSS_GCC)
  OBJDUMP = $(CROSS_OBJDUMP)
  OEXT = elf
  #ifeq (${IRDUMP},1)
  ifdef IRDUMP
    COPTS = -pedantic -Wcomment -fno-asm -fsigned-char -W -Wparentheses -Wreturn-type -Wswitch -Wunused -Wsign-compare -Wimplicit -Wreturn-type -Wshadow -Wpointer-arith -Wwrite-strings -Wsign-compare -Wstrict-prototypes -Wmissing-prototypes -Wmissing-declarations -msoft-float $(OPT) -I. -T generic-hosted.ld
  else
    COPTS = -pedantic -Wcomment -fno-asm -fsigned-char -W -Wparentheses -Wreturn-type -Wswitch -Wunused -Wsign-compare -Wimplicit -Wreturn-type -Wshadow -Wpointer-arith -Wwrite-strings -Wsign-compare -Wstrict-prototypes -Wmissing-prototypes -Wmissing-declarations -msoft-float $(OPT) -I. -T generic-hosted.ld
  endif
 
  ifdef PRINT
    COPTS += -msoft-float
  endif
else
  CC = $(GCC)
  OBJDUMP = $(HOST_OBJDUMP)
  OEXT = out
  #ifeq (${IRDUMP}, 1)
  ifdef IRDUMP
    COPTS = -static ${OPT} -I../../../ir2c/include
  else
    COPTS = -static ${OPT} -I../../../ir2c/include
  endif
endif


all: erat_sieve_no_print_IR

test:
	./erat_sieve_no_print_IR.$(OEXT)

erat_sieve_no_print_IR:: erat_sieve_no_print_IR.c
	$(CC) $(COPTS) -o $@.$(OEXT) $^
	$(OBJDUMP) -D  $@.$(OEXT) >& $@.$(DUMPEXT)

erat_sieve_print_IR:: erat_sieve_print_IR.c
	$(CC) $(OPTS) -o $@.$(OEXT) $^
	$(OBJDUMP) -D  $@.$(OEXT) >& $@.$(DUMPEXT)

#adding - to rm so that errors are ignored	
clean::
	@echo Cleaning up massaged IR build
	rm -rf *.elf *.out *.objdump
	rm -rf *.c.*
