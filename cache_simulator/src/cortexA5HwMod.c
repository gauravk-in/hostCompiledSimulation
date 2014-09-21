#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "cacheSimHwMod.h"

#define CACHELINE_VALID_BIT (1 << 0)
#define IS_CACHELINE_VALID(flags) (flags & CACHELINE_VALID_BIT)
#define SET_CACHELINE_VALID(flags) (flags |= CACHELINE_VALID_BIT)
#define SET_CACHELINE_INVALID(flags) (flags &= ~CACHELINE_VALID_BIT)

#define CACHELINE_DIRTY_BIT (1 << 1)
#define IS_CACHELINE_DIRTY(flags) (flags & CACHELINE_DIRTY_BIT)
#define SET_CACHELINE_DIRTY(flags) (flags |= CACHELINE_DIRTY_BIT)
#define SET_CACHELINE_CLEAN(flags) (flags &= ~CACHELINE_DIRTY_BIT)

#define ADDRESS_LEN_BITS 32

/**** DATA STRUCTURES *********************************************************/

struct cacheConfig
{
	// Size
	unsigned int lineLenBytes;
	unsigned int cacheSizeBytes;
	unsigned int numSets;

	// Derived
	unsigned int numLines;
	unsigned long tagMask;
	unsigned int tagLenBits;
	unsigned long indexMask;
	unsigned int indexLenBits;

	// Features
	unsigned int isWriteThrough;

	// Latencies
//	unsigned int hitLat;
//	unsigned int missLat;
	unsigned int hitLatency;
	unsigned int missLatency;

};
typedef struct cacheConfig cacheConfig_t;

/**
 * Stores all data related to a cache line.
 */
struct cacheLine
{
	unsigned int flags;
	unsigned long tag;
};
typedef struct cacheLine cacheLine_t;

/**** GLOBAL VARIABLES ********************************************************/

cacheConfig_t L1DCacheConf;
cacheConfig_t L1ICacheConf;
cacheConfig_t L2CacheConf;

cacheLine_t **L1DCache;
cacheLine_t **L1ICache;
cacheLine_t **L2Cache;

unsigned int memWriteLatency = 100;
unsigned int memReadLatency = 100;

unsigned long L1D_Hit_Read = 0;
unsigned long L1D_Hit_Writeback = 0;
unsigned long L1D_Hit_Writethrough = 0;
unsigned long L1D_Miss = 0;
unsigned long L1I_Hit_Read = 0;
unsigned long L1I_Hit_Writeback = 0;
unsigned long L1I_Hit_Writethrough = 0;
unsigned long L1I_Miss = 0;
unsigned long L2_Hit_Read = 0;
unsigned long L2_Hit_Writeback = 0;
unsigned long L2_Hit_Writethrough = 0;
unsigned long L2_Miss = 0;

/**** LOCAL FUNCTIONS *********************************************************/

int log_base2(int val)
{
	int ret = 0;
	while (val >>= 1) ++ret;
	return ret;
}

void initCacheParams ()
{
	int subIndexLen = 0;
	int i;

	/*** L1 DCache *****************/

	L1DCacheConf.lineLenBytes 		= 32;
	L1DCacheConf.cacheSizeBytes 	= 4 * 1024; // 4 KB
	L1DCacheConf.numSets 			= 4;

	L1DCacheConf.numLines  			= L1DCacheConf.cacheSizeBytes /
			(L1DCacheConf.lineLenBytes * L1DCacheConf.numSets);

	subIndexLen = log_base2(L1DCacheConf.lineLenBytes);
	L1DCacheConf.indexLenBits = log_base2(L1DCacheConf.numLines);
	L1DCacheConf.indexMask = 0;
	for (i = 0; i < L1DCacheConf.indexLenBits; i++)
	{
		L1DCacheConf.indexMask = L1DCacheConf.indexMask << 1;
		L1DCacheConf.indexMask |= 0x00000001;
	}
	L1DCacheConf.indexMask = L1DCacheConf.indexMask << subIndexLen;

	L1DCacheConf.tagLenBits = ADDRESS_LEN_BITS - L1DCacheConf.indexMask - subIndexLen;
	L1DCacheConf.tagMask = 0;
	for (i = 0; i < L1DCacheConf.tagLenBits; i++)
	{
		L1DCacheConf.tagMask = L1DCacheConf.tagMask << 1;
		L1DCacheConf.tagMask |= 0x00000001;
	}
	L1DCacheConf.tagMask = L1DCacheConf.tagMask << (L1DCacheConf.indexLenBits + subIndexLen);

	L1DCacheConf.isWriteThrough = 0;

	L1DCacheConf.hitLatency = 2;
	L1DCacheConf.missLatency = 2;


	/*** L1 ICache *****************/

	L1ICacheConf.lineLenBytes 		= 32;
	L1ICacheConf.cacheSizeBytes 	= 4 * 1024; // 4 KB
	L1ICacheConf.numSets 			= 2;

	L1ICacheConf.numLines  			= L1ICacheConf.cacheSizeBytes /
			(L1ICacheConf.lineLenBytes * L1ICacheConf.numSets);

	subIndexLen = log_base2(L1ICacheConf.lineLenBytes);
	L1ICacheConf.indexLenBits = log_base2(L1ICacheConf.numLines);
	L1ICacheConf.indexMask = 0;
	for (i = 0; i < L1ICacheConf.indexLenBits; i++)
	{
		L1ICacheConf.indexMask = L1ICacheConf.indexMask << 1;
		L1ICacheConf.indexMask |= 0x00000001;
	}
	L1ICacheConf.indexMask = L1ICacheConf.indexMask << subIndexLen;

	L1ICacheConf.tagLenBits = ADDRESS_LEN_BITS - L1ICacheConf.indexMask - subIndexLen;
	L1ICacheConf.tagMask = 0;
	for (i = 0; i < L1ICacheConf.tagLenBits; i++)
	{
		L1ICacheConf.tagMask = L1ICacheConf.tagMask << 1;
		L1ICacheConf.tagMask |= 0x00000001;
	}
	L1ICacheConf.tagMask = L1ICacheConf.tagMask << (L1ICacheConf.indexLenBits + subIndexLen);

	L1ICacheConf.isWriteThrough = 0;

	L1ICacheConf.hitLatency = 2;
	L1ICacheConf.missLatency = 2;


	/*** L2 Cache *****************/

	L2CacheConf.lineLenBytes 		= 32;
	L2CacheConf.cacheSizeBytes 		= 32 * 1024; // 32 KB
	L2CacheConf.numSets 			= 2;

	L2CacheConf.numLines  			= L2CacheConf.cacheSizeBytes /
			(L2CacheConf.lineLenBytes * L2CacheConf.numSets);

	subIndexLen = log_base2(L2CacheConf.lineLenBytes);
	L2CacheConf.indexLenBits = log_base2(L2CacheConf.numLines);
	L2CacheConf.indexMask = 0;
	for (i = 0; i < L2CacheConf.indexLenBits; i++)
	{
		L2CacheConf.indexMask = L2CacheConf.indexMask << 1;
		L2CacheConf.indexMask |= 0x00000001;
	}
	L2CacheConf.indexMask = L2CacheConf.indexMask << subIndexLen;

	L2CacheConf.tagLenBits = ADDRESS_LEN_BITS - L2CacheConf.indexMask - subIndexLen;
	L2CacheConf.tagMask = 0;
	for (i = 0; i < L2CacheConf.tagLenBits; i++)
	{
		L2CacheConf.tagMask = L2CacheConf.tagMask << 1;
		L2CacheConf.tagMask |= 0x00000001;
	}
	L2CacheConf.tagMask = L2CacheConf.tagMask << (L2CacheConf.indexLenBits + subIndexLen);

	L2CacheConf.isWriteThrough = 0;

	L2CacheConf.hitLatency = 14;
	L2CacheConf.missLatency = 14;
}


/**
 * Allocates a 2 dimensional array. To be used to allocate space for cache lines
 *
 * @param rows number of sets
 * @param cols number of cache lines
 * @param size size of the data structure to be stored
 *
 * @return pointer to array of pointers pointing to rows of data.
 */
void** alloc2D(unsigned int rows, unsigned int cols, size_t size)
{
	void** ret;
	void *data;
	int i;
	size_t arrSize = (rows * sizeof(void*)) + (rows * cols * size);

	ret = malloc(arrSize);
	memset(ret, 0, arrSize);
	data = (void*) (ret + rows);

	for(i=0; i<rows; i++)
	{
		ret[i] = data + i * cols * size;
	}

	return ret;
}

inline unsigned long getTagFromAddress(unsigned long address,
		unsigned int tagLengthBits, unsigned long tagMask)
{
	return (address & tagMask) >> (ADDRESS_LEN_BITS - tagLengthBits);
}

inline unsigned long getIndexFromAddress(unsigned long address,
		unsigned int offsetLengthBits, unsigned long indexMask)
{

	return (address & indexMask) >> offsetLengthBits;
}


/**** HWMOD FUNCTIONS *********************************************************/

unsigned long long cortexA5_simICache(unsigned long address,
										   unsigned int nBytes)
{
	unsigned int latency = 0;
	unsigned long tag;
	unsigned long index;
	int setIndex = 0;

	tag = getTagFromAddress(address, L1ICacheConf.tagLenBits, L1ICacheConf.tagMask);
	index = getIndexFromAddress(address, L1ICacheConf.indexLenBits, L1ICacheConf.indexMask);

	for (setIndex = 0; setIndex < L1ICacheConf.numSets; setIndex++)
	{
		if (L1ICache[setIndex][index].tag == tag &&
				IS_CACHELINE_VALID(L1ICache[setIndex][index].flags))
		{
			latency += L1ICacheConf.hitLatency;
			L1I_Hit_Read++;
			return latency;
		}
	}
	// L1 Miss has occured!
	L1I_Miss++;
	latency += L1ICacheConf.missLatency;

	tag = getTagFromAddress(address, L2CacheConf.tagLenBits, L2CacheConf.tagMask);
	index = getIndexFromAddress(address, L2CacheConf.indexLenBits, L2CacheConf.indexMask);

	for (setIndex = 0; setIndex < L2CacheConf.numSets; setIndex++)
	{
		if (L2Cache[setIndex][index].tag == tag &&
				IS_CACHELINE_VALID(L2Cache[setIndex][index].flags))
		{
			latency += L2CacheConf.hitLatency;
			L2_Hit_Read++;
			return latency;
		}
	}

	// L2 Miss has occured!
	L2_Miss++;
	latency += L2CacheConf.missLatency;
	latency += memReadLatency;

	return latency;
}


unsigned long long cortexA5_simDCache(unsigned long address,
										   unsigned int isReadAccess)
{
	unsigned int latency = 0;
	unsigned long tag;
	unsigned long index;
	int setIndex = 0;

	if (isReadAccess == 0 && L1DCacheConf.isWriteThrough == 1) // Write Access
	{
		// Simply increment latency by time to write to memory
		latency += memWriteLatency;
		L1D_Hit_Writethrough++;
	}
	// For writeback, there is no latency. We can safely take this assumption,
	//   as we are only using a Single Core System.

	tag = getTagFromAddress(address, L1DCacheConf.tagLenBits, L1DCacheConf.tagMask);
	index = getIndexFromAddress(address, L1DCacheConf.indexLenBits, L1DCacheConf.indexMask);

	for (setIndex = 0; setIndex < L1DCacheConf.numSets; setIndex++)
	{
		if (L1DCache[setIndex][index].tag == tag &&
				IS_CACHELINE_VALID(L1DCache[setIndex][index].flags))
		{
			latency += L1DCacheConf.hitLatency;
			if (isReadAccess)
				L1D_Hit_Read++;
			else
				L1D_Hit_Writeback++;
			return latency;
		}
	}
	// L1 Miss has occured!
	L1D_Miss++;
	latency += L1DCacheConf.missLatency;

	tag = getTagFromAddress(address, L2CacheConf.tagLenBits, L2CacheConf.tagMask);
	index = getIndexFromAddress(address, L2CacheConf.indexLenBits, L2CacheConf.indexMask);

	for (setIndex = 0; setIndex < L2CacheConf.numSets; setIndex++)
	{
		if (L2Cache[setIndex][index].tag == tag &&
				IS_CACHELINE_VALID(L2Cache[setIndex][index].flags))
		{
			latency += L2CacheConf.hitLatency;
			if (isReadAccess)
				L2_Hit_Read++;
			else
				L2_Hit_Writeback++;
			return latency;
		}
	}

	// L2 Miss has occured!
	L2_Miss++;
	latency += L2CacheConf.missLatency;
	latency += memReadLatency;
	return latency;
}

void cortexA5_cacheSimInit()
{
	// Allocate space for caches
	initCacheParams();

	L1DCache = (cacheLine_t **) alloc2D(L1DCacheConf.numSets,
				L1DCacheConf.numLines, sizeof(cacheLine_t));
	L1ICache = (cacheLine_t **) alloc2D(L1ICacheConf.numSets,
				L1ICacheConf.numLines, sizeof(cacheLine_t));
	L2Cache = (cacheLine_t **) alloc2D(L2CacheConf.numSets,
				L2CacheConf.numLines, sizeof(cacheLine_t));

	return;
}

void cortexA5_cacheSimFini()
{
	free(L1DCache);
	free(L1ICache);
	free(L2Cache);

	printf("Statistics : \n");

	printf("\nL1 Data Cache\n");
	printf("\t Hit Read = %ld\n", L1D_Hit_Read);
	printf("\t Hit Writeback = %ld\n", L1D_Hit_Writeback);
	printf("\t Miss = %ld\n", L1D_Miss);

	printf("\nL1 Instruction Cache\n");
	printf("\t Hit Read = %ld\n", L1I_Hit_Read);
	printf("\t Miss = %ld\n", L1I_Miss);

	printf("\nL2 Unified Cache\n");
	printf("\t Hit Read = %ld\n", L2_Hit_Read);
	printf("\t Hit Writeback = %ld\n", L2_Hit_Writeback);
	printf("\t Miss = %ld\n", L2_Miss);

	return;
}

struct cacheSimHwMod_t hwMod = {
		.simDCache = &cortexA5_simDCache,
		.simICache = &cortexA5_simICache,
		.cacheSimInit = &cortexA5_cacheSimInit,
		.cacheSimFini = &cortexA5_cacheSimFini
};
