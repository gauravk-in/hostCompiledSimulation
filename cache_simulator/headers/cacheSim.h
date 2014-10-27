/**
 * cache_sim.h
 * Purpose: Interface to the cache simulator. Defines functions that will be
 * called from the benchmark.
 *
 * @author: Gaurav Kukreja
 */

#ifndef CACHE_SIM_H
#define CACHE_SIM_H

#include "cacheSimResult.h"

/**
 * Simulates Instruction Cache access by benchmark
 *
 * @param address Starting address of instructions in the basic block
 * @param nBytes Number of bytes of instructions accessed in the basic block
 * @param
 *
 * @return number of clock cycles spent
 */
extern unsigned long long simICache(unsigned long address,
		unsigned int nBytes,
		struct csim_result_t *result);

/**
 * Simulates Data Cache access by benchmark
 *
 * @param address Address of data accessed
 * @param isReadAccess Tells cache simulator if it was read access.
 *
 * @return number of clock cycles spent
 */
extern unsigned long long simDCache(unsigned long address,
		unsigned int isReadAccess,
		struct csim_result_t *result);

/**
 * Initialize the cache data structures
 */
extern void cacheSimInit(struct csim_result_t *result);

/**
 * Frees data structures and cleans up
 *
 */
extern void cacheSimFini(struct csim_result_t *result);

#endif // CACHE_SIM_H
