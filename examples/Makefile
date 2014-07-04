include ../Makefile.macros
include Makefile.macros

#EXAMPLES = sieve crc32 adpcm sha basicmath
#EXAMPLES = sha sieve
EXAMPLES = sieve
STARTADR = 0x10000214

# Space separated list of all C files in APPDIR
HDR=$(wildcard $(APPBASEDIR)/$(APPDIR)/*.h)
SRC=$(wildcard $(APPBASEDIR)/$(APPDIR)/*.c)

# File selection in case of multiple versions of app
IRFILE=
ifeq ($(APPBASEDIR),sieve)
	IRFILE=/erat_sieve_no_print_IR.c
endif

# Characterization environment variables
export ENV_OUT_DAT_DIR:=$(APPBASEDIR)/$(OUT_DAT_DIR)/
export ENV_IN_DAT_DIR:=$(APPBASEDIR)/$(IN_DAT_DIR)/
export ENV_HC_DIR:=$(APPBASEDIR)/$(HC_DIR)

all: app

app:
	set -e; for e in $(EXAMPLES); do	\
	  $(MAKE) -C $$e/$(APPDIR) all test;		\
	  $(MAKE) -C $$e/$(APPDIR) PHASE=final all;	\
	done

#run: run_ir2c

ir2c:
	set -e; for e in $(EXAMPLES); do	\
	  $(MAKE) APPBASEDIR=$$e ir2c_full;		\
	done

ir2c_full: run_ir2c compile_ir2c test_ir2c

run_ir2c:
	set -e; $(foreach s,$(SRC), $(IR2C) $(s) > $(APPBASEDIR)/$(IRDIR)/$(basename $(notdir $(s)))_IR.c ;)
	set -e; $(foreach h,$(HDR), $(LN) -f ../$(APPDIR)/$(basename $(notdir $(h))).h $(APPBASEDIR)/$(IRDIR)/$(basename $(notdir $(h))).h ;)
	$(TOUCH) $(APPBASEDIR)/$(IRDIR)/ir2c.h

compile_ir2c:
	$(MAKE) -C $(APPBASEDIR)/$(IRDIR)
	$(MAKE) -C $(APPBASEDIR)/$(IRDIR) PHASE=final

test_ir2c:
	$(MAKE) -C $(APPBASEDIR)/$(IRDIR) test
	
clean_ir2c:
	@echo Cleaning up IR 2 C test
	-rm -rf $(APPBASEDIR)/$(IRDIR)/*IR.c
	$(MAKE) -C $(APPBASEDIR)/$(IRDIR) clean

clean: 
	for e in $(EXAMPLES); do	\
	  $(MAKE) -C $$e/$(APPDIR) clean;		\
	  $(MAKE) APPBASEDIR=$$e clean_ir2c;		\
	done





