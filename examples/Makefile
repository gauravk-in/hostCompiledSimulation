include ../Makefile.macros
include Makefile.macros

#EXAMPLES = sieve crc32 adpcm sha basicmath
EXAMPLES = sha sieve
#EXAMPLES = simple
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

run: run_ir2c hc_dev

run_test: ir2c back_annotate

run_test_all: 
	set -e; for e in $(EXAMPLES); do	\
	  $(MAKE) APPBASEDIR=$$e run_test;		\
	done

ir2c: run_ir2c compile_ir2c test_ir2c

ir2c_all:
	set -e; for e in $(EXAMPLES); do	\
	  $(MAKE) APPBASEDIR=$$e ir2c;		\
	done

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
	-rm $(APPBASEDIR)/$(IRDIR)/*IR.c


back_annotate: hc_dev compile_hc test_hc

back_annotate_all:
	set -e; for e in $(EXAMPLES); do	\
	  $(MAKE) APPBASEDIR=$$e back_annotate;	\
	done

hc_dev: 
	$(BA) -i $(APPBASEDIR)/$(IRDIR)$(IRFILE) -I $(APPBASEDIR)/$(OBJDIR)
	set -e; $(foreach h,$(HDR), $(LN) -f ../$(APPDIR)/$(basename $(notdir $(h))).h $(APPBASEDIR)/$(HC_DIR)/$(basename $(notdir $(h))).h ;)

mapping: 
	$(MAP) -i $(APPBASEDIR)/$(IRDIR)$(IRFILE) -I $(APPBASEDIR)/$(OBJDIR)

compile_hc:
	$(MAKE) -C $(APPBASEDIR)/$(HC_DIR)

test_hc:
	$(MAKE) -C $(APPBASEDIR)/$(HC_DIR) test

#adding - to rm so that errors are ignored	
clean_ba:
	@echo Cleaning up back annotation test
	-rm $(ENV_IN_DAT_DIR)/*.dat $(ENV_OUT_DAT_DIR)/*.dat $(ENV_IN_PWR_TOOL_DIR)/*.xml $(ENV_OUT_PWR_TOOL_DIR)/* $(ENV_HC_DIR)/*.c  $(ENV_HC_DIR)/*.out


clean: 
	for e in $(EXAMPLES); do	\
	  $(MAKE) -C $$e/$(APPDIR) clean;		\
	  $(MAKE) APPBASEDIR=$$e clean_plat_app clean_plat_hc;	\
	  $(MAKE) APPBASEDIR=$$e clean_ir2c clean_ba ;	\
	done





