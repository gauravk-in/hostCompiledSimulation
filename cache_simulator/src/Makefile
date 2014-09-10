include ../Makefile.macros

GCC = gcc
CFLAGS = -O3

HEADERS = $(CACHESIM_HEADERS)

# Cache Simulation Source Code
SOURCES = cacheSim.c cacheSimStat.c cacheSimStat.h cacheSimHwMod.h $(HEADERS)/cacheSim.h
OBJECTS = cacheSim.o cacheSimStat.o

# Add the source file(s) for the cache simulator hardware models
ifeq ($(CACHESIM_HWMOD),generic)
    SOURCES += genericHwMod.c
    OBJECTS += genericHwMod.o
endif

all: cacheSim

cacheSim: $(SOURCES)
	$(GCC) $(CFLAGS) -c -Wall -Werror -fpic $^
	$(GCC) -shared -o lib$@.so $(OBJECTS)
	
clean:
	rm -rf *.o libcacheSim.so