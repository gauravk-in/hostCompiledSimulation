/**
 * cache_sim.c
 * Purpose: This is a cache simulation software. The benchmark code is
 * instrumented, and the modified code is compiled with the simulator. The
 * cache organization can be configured from human-readable config files.
 *
 * @author Gaurav Kukreja
 */

#include <stdio.h>
#include "cacheSimHwMod.h"
#include "cacheSimStat.h"

#define COLLECT_STAT

#define HERE printf("%s: %s: %d\n", __FILE__, __func__, __LINE__)

/******************************************************************************
 * GLOBAL VARIABLES
 ******************************************************************************/


/******************************************************************************
 * DATA STRUCTURES
 ******************************************************************************/


/******************************************************************************
 * LOCAL FUNCTION DECLARATIONS
 ******************************************************************************/


/******************************************************************************
 * LOCAL FUNCTIONS
 ******************************************************************************/


/******************************************************************************
 * GLOBAL FUNCTIONS
 ******************************************************************************/

/**
 * Simulates Instruction Cache access by benchmark
 *
 * @param address Starting address of instructions in the basic block
 * @param nBytes Number of bytes of instructions accessed in the basic block
 *
 * @return number of clock cycles spent
 */
unsigned long long simICache(unsigned long address, unsigned int nBytes)
{
	unsigned long long nCycles;
	cacheSimStat.access_type = ACCESS_TYPE_INVALID;
	cacheSimStat.nCycles = 0;
	cacheSimStat.powerMicroJ = 0;

	nCycles = hwMod.simICache(address, nBytes);

#ifdef COLLECT_STAT
	cacheSimStatCollect();
#endif

	return nCycles;
}

/**
 * Simulates Data Cache access by benchmark
 *
 * @param address Address of data accessed
 *
 * @return number of clock cycles spent
 */
unsigned long long simDCache(unsigned long address, unsigned int isReadAccess)
{
	unsigned long long nCycles;
	cacheSimStat.access_type = ACCESS_TYPE_INVALID;
	cacheSimStat.nCycles = 0;
	cacheSimStat.powerMicroJ = 0;

	nCycles = hwMod.simDCache(address, isReadAccess);

#ifdef COLLECT_STAT
	cacheSimStatCollect();
#endif

	return nCycles;
}

/**
 * Initialize the cache data structures
 */
void cacheSimInit()
{
	hwMod.cacheSimInit();
}

/**
 * Frees data structures and cleans up
 */
void cacheSimFini()
{
	hwMod.cacheSimFini();

#ifdef COLLECT_STAT
	cacheSimStatPrint();
#endif
}
