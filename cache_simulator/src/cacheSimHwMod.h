/**
 * cacheSimHwMod.h
 * Purpose: Contains the Hardware Model Descriptor Data Structure
 *
 * @author: Gaurav Kukreja
 */

#ifndef CACHE_SIM_HW_MOD_H
#define CACHE_SIM_HW_MOD_H

#include "cacheSimStat.h"

/**
 * Cache Simulation Hardware Model Descriptor
 */
struct cacheSimHwMod_t
{
	/**
	 * Simulates Instruction Cache access by benchmark
	 *
	 * @param address Starting address of instructions in the basic block
	 * @param nBytes Number of bytes of instructions accessed in the basic block
	 *
	 * @return number of clock cycles spent
	 */
	unsigned int (*simICache) (unsigned long address, unsigned int nBytes);

	/**
	 * Simulates Data Cache access by benchmark
	 *
	 * @param address Address of data accessed
	 * @param isReadAccess Tells cache simulator if it was read access.
	 *
	 * @return number of clock cycles spent
	 */
	unsigned int (*simDCache) (unsigned long address, unsigned int isReadAccess);

	/**
	 * Initialize the cache data structures
	 *
	 * @param configFile Path to the json config file which describes cache
	 *        organization
	 */
	void (*cacheSimInit) ();

	/**
	 * Frees data structures and cleans up
	 */
	void (*cacheSimFini) ();
};


/**
 * The hwMod data structure is a global data structure which will be defined in
 * the hardware model implementations. It will be accessed from cacheSim.c by
 * including this file, and be linked to the specific hardware model at compile
 * time.
 */
extern struct cacheSimHwMod_t hwMod;

#endif // CACHE_SIM_HW_MOD_H