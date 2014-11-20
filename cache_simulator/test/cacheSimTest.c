/**
 * This program tests the cache simulation software. It basically generates a
 * number of memory accesses, and checks the statistics generated from cache
 * simulation.
 */

#include "cacheSim.h"
#include "cacheSimResult.h"

#define HERE printf("%s: %s: %d\n", __FILE__, __func__, __LINE__)

#define MAX_REPEATS 2 
#define MAX_ACCESSES 64 * 1024 

#define START_ADD 0x0

struct csim_result_t csim_result;

int main(int argc, char **argv)
{
	unsigned long address = START_ADD;

	cacheSimInit(&csim_result);

	for(unsigned long j = 0; j < MAX_REPEATS; j++)
		for(unsigned long i = 0; i < MAX_ACCESSES; i+=4)
		{
			simDCache(address + i, 1, &csim_result);
		}

	cacheSimFini(&csim_result);

	return 0;
}
