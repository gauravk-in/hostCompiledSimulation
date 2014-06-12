/**
 * cacheSimStat.h
 * Purpose: Data structures and function declarations for collecting statistics
 * returned from Cache Simulation.
 */

#ifndef CACHE_SIM_STAT_H
#define CACHE_SIM_STAT_H

/**
 * Enum to specify the kind of memory access.
 */
enum cacheSimStatAccess_t
{
	ACCESS_TYPE_INVALID = 0,
	L1_HIT_READ,
	L1_HIT_WRITEBACK,
	L1_HIT_WRITETHROUGH,
	L1_MISS_FLUSH,
	L1_MISS,
	L2_HIT_READ,
	L2_HIT_WRITEBACK,
	L2_HIT_WRITETHROUGH,
	L2_MISS_FLUSH,
	L2_MISS
};


/**
 * Statistics will be returned by Hardware Model Implementation of the cache.
 */
struct cacheSimStat_t
{
	enum cacheSimStatAccess_t access_type;
	unsigned int nCycles;
	unsigned int powerMicroJ;
};

/**
 * cacheSimStat is globally declared in cacheSim.c. The Hardware Model
 * implementation will use this data structure to return the cache simulation
 * statistics.
 */
extern struct cacheSimStat_t cacheSimStat;

void cacheSimStatCollect();

void cacheSimStatPrint();

#endif // CACHE_SIM_STAT_H
