/**
 * This program tests the cache simulation software. It basically generates a
 * number of memory accesses, and checks the statistics generated from cache
 * simulation.
 */

#include "cacheSim.h"

#define HERE printf("%s: %s: %d\n", __FILE__, __func__, __LINE__)

#define MAX_REPEATS 2
#define MAX_ACCESSES 524288

#define START_ADD 0x12345678

int main(int argc, char **argv)
{
	unsigned long address = START_ADD;

	cacheSimInit();

	for(unsigned long j = 0; j < MAX_REPEATS; j++)
		for(unsigned long i = 0; i < MAX_ACCESSES; i++)
		{
			simDCache(address + i, 1);
		}
	cacheSimFini();

	return 0;
}
