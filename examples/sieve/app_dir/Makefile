include ../../Makefile.macros

TREEDUMP = -fdump-tree-all-blocks-details
OPT = -O2 #is O3 in original MiBench download. Use O3 for final testing
DEBUG = -g
IRDUMP = 1 #defined - dump IR files, undefined - don't.
#PRINT = 1 #if defined and PHASE defined, include soft-float lib. fprintf uses floating point
DUMPEXT = objdump

ifdef PHASE
  CC = $(CROSS_GCC)
  OBJDUMP = $(CROSS_OBJDUMP)
  OEXT = elf
  #ifeq (${IRDUMP},1)
  ifdef IRDUMP
    COPTS = -pedantic -Wcomment -fno-asm -fsigned-char -W -Wparentheses -Wreturn-type -Wswitch -Wunused -Wsign-compare -Wimplicit -Wreturn-type -Wshadow -Wpointer-arith -Wwrite-strings -Wsign-compare -Wstrict-prototypes -Wmissing-prototypes -Wmissing-declarations -msoft-float $(OPT) $(TREEDUMP) -T generic-hosted.ld
  else
    COPTS = -pedantic -Wcomment -fno-asm -fsigned-char -W -Wparentheses -Wreturn-type -Wswitch -Wunused -Wsign-compare -Wimplicit -Wreturn-type -Wshadow -Wpointer-arith -Wwrite-strings -Wsign-compare -Wstrict-prototypes -Wmissing-prototypes -Wmissing-declarations -msoft-float $(OPT) -T generic-hosted.ld
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
    COPTS = -static ${OPT} 
  else
    COPTS = -static ${OPT}
  endif
endif

all: erat_sieve_no_print erat_sieve_print

test:
	./erat_sieve_print.$(OEXT)

erat_sieve_no_print:: erat_sieve_no_print.c
	$(CC) $(COPTS) $(CFLAGS) -o $@.$(OEXT) $^
	$(OBJDUMP) -D  $@.$(OEXT) >& $@.$(DUMPEXT)

erat_sieve_print:: erat_sieve_print.c
	$(CC) $(COPTS) $(CFLAGS) -o $@.$(OEXT) $^
	$(OBJDUMP) -D  $@.$(OEXT) >& $@.$(DUMPEXT)

#adding - to rm so that errors are ignored	
clean::
	@echo Cleaning up massaged IR build
	-rm *.$(OEXT) *.objdump erat_sieve_no_print.c.* erat_sieve_print.c.*
