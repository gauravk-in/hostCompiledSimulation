include ../Makefile.macros
include Makefile.macros

#EXAMPLES = sieve crc32 adpcm sha basicmath
EXAMPLES = crc32 basicmath
#EXAMPLES = sha sieve
#EXAMPLES = sha 
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

# IR2C Targets

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

help:
	@printf "\nHelp information for running project\n"
	@printf "\n\ttarget: Operation Performed\n"
	@printf "\nGeneral Targets\n"
	@printf "\thelp: Display this message\n"
	@printf "\tall: Compile all the benchmarks\n"
	@printf "\nIR2C Targets\n"
	@printf "\tir2c: For all benchmarks run_ir2c, compile_ir2c and test_ir2c\n"
	@printf "\trun_ir2c: Needs variable APPBASEDIR. Runs ir2c code, and generates Intermediate Source Code\n"
	@printf "\tcompile_ir2c: Needs variable APPBASEDIR. Compile ISC.\n"
	@printf "\ttest: Calls test target declared in ir_c/Makefile in each benchmark\n"
	@printf "\nmap_cfg Targets\n"
	@printf "\thelp: Display this message\n"
	
	@printf "\n\n"

