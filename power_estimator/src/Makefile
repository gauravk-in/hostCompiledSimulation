include ../Makefile.macros

GCC = gcc
CFLAGS = -O3

HEADERS = $(POWEREST_HEADERS)

CFLAGS += -I$(HEADERS)

# Cache Simulation Source Code
SOURCES = power_estimator.c $(HEADERS)/power_estimator.h
OBJECTS = power_estimator.o

all: powerEst

powerEst: $(SOURCES)
	$(GCC) $(CFLAGS) -c -Wall -Werror -fpic $^
	$(GCC) -shared -o lib$@.so $(OBJECTS)
	
clean:
	rm -rf *.o libpowerEst.so
