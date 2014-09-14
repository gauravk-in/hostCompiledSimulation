/**
 * genericHwMod.c
 * Purpose: Implements a generic cache simulation hardware model
 *
 * The Generic Cache Model has the following features
 *
 * Levels
 *   It has two levels of Cache.
 *   L1 Cache has separate data and instruction caches. Set Associative Cache.
 *   L2 Cache is used for data as well as instruction.
 *
 * Size
 *   The cache size, cache line size and number of sets are initialized in
 *   readConfigFile() function.
 *
 * Features
 *   Write Through Cache
 *   No pre-fetching for data.
 *   No pre-fetching for instruction. (??)
 *   Round Robin Replacement Policy for L1
 *   No Special DMA effects have been taken into account
 *
 */

#include <stdlib.h>
#include <string.h>

#include "cacheSimHwMod.h"
#include "cacheSimStat.h"

#define HERE printf("%s: %s: %d\n", __FILE__, __func__, __LINE__)

#define ADDRESS_LEN_BITS 32
#define CACHE_HIT 0
#define CACHE_HIT_WRITEBACK 1
#define CACHE_HIT_WRITETHROUGH 2
#define CACHE_MISS 3
#define CACHE_MISS_FLUSH 4

/******************************************************************************
 * DATA STRUCTURES
 ******************************************************************************/


/**
 * Stores cache parameters for each type/level of cache
 */
struct cacheParam_t
{
	// Size Params
	unsigned int cacheSets;
	unsigned int cacheSizeBytes;
	unsigned int lineSizeBytes;
	unsigned int cacheLength;
	unsigned int tagLengthBits;
	unsigned int indexLengthBits;
	unsigned int offsetLengthBits;

	// Derived
	unsigned long tagMask;
	unsigned long indexMask;

	// Features
	unsigned int isWriteThrough;

	// Latencies
	unsigned int cyclesHitRead;
	unsigned int cyclesHitWriteThrough;
	unsigned int cyclesHitWriteBack;
	unsigned int cyclesMiss;
	unsigned int cyclesMissFlush;
};

#define CACHELINE_VALID_BIT (1 << 0)
#define IS_CACHELINE_VALID(flags) (flags & CACHELINE_VALID_BIT)
#define SET_CACHELINE_VALID(flags) (flags |= CACHELINE_VALID_BIT)
#define SET_CACHELINE_INVALID(flags) (flags &= ~CACHELINE_VALID_BIT)

#define CACHELINE_DIRTY_BIT (1 << 1)
#define IS_CACHELINE_DIRTY(flags) (flags & CACHELINE_DIRTY_BIT)
#define SET_CACHELINE_DIRTY(flags) (flags |= CACHELINE_DIRTY_BIT)
#define SET_CACHELINE_CLEAN(flags) (flags &= ~CACHELINE_DIRTY_BIT)

/**
 * Stores all data related to a cache line.
 */
struct cacheLine_t
{
	unsigned int flags;
	unsigned long tag;
};

/******************************************************************************
 * GLOBAL VARIABLES
 ******************************************************************************/

struct cacheParam_t L1Params;
struct cacheParam_t L2Params;
unsigned long cyclesMemAccess;

struct cacheLine_t **L1DCache;
struct cacheLine_t **L1ICache;
struct cacheLine_t **L2DCache;
struct cacheLine_t **L2ICache;

/**
 * Array to keep a track of which cache line to remove in a round robin fashion
 */
unsigned int *L1DCacheReplace;
unsigned int *L1ICacheReplace;
unsigned int *L2DCacheReplace;
unsigned int *L2ICacheReplace;

/******************************************************************************
 * LOCAL FUNCTION DECLARATIONS
 ******************************************************************************/

void readConfigFile();

void** alloc2D(unsigned int rows, unsigned int cols, size_t size);


/******************************************************************************
 * LOCAL FUNCTIONS
 ******************************************************************************/

int log_base2(int val)
{
	int ret = 0;
	while (val >>= 1) ++ret;
	return ret;
}

/**
 * Reads config file and initializes data structures
 *
 * @param configFile Path to the config file.
 */
void readConfigFile()
{
	//	TODO: Read from config file, and remove the following workaround

	int i;

	// L1 Cache Parameters - same for separate Instruction and Data Cache
	// L1 Size Params
	L1Params.cacheSets 			= 4;
	L1Params.cacheSizeBytes 	= 16 * 1024;
	L1Params.lineSizeBytes 		= 16;
	L1Params.indexLengthBits 	= log_base2(L1Params.cacheSizeBytes / (L1Params.cacheSets * L1Params.lineSizeBytes));
	L1Params.offsetLengthBits 	= log_base2(L1Params.lineSizeBytes);
	L1Params.tagLengthBits 		= 32 - L1Params.indexLengthBits - L1Params.offsetLengthBits;


	// L1 Latencies
	L1Params.cyclesHitRead 			= 2;
	L1Params.cyclesHitWriteThrough 	= 100;
	L1Params.cyclesHitWriteBack		= 4;
	L1Params.cyclesMiss 			= 2;
	L1Params.cyclesMissFlush		= 105;

	// L1 Features
	L1Params.isWriteThrough 	= 0;

	// L1 Derived
	L1Params.cacheLength		= L1Params.cacheSizeBytes
									/ L1Params.cacheSets
									/ L1Params.lineSizeBytes; //256

	L1Params.tagMask = 0;
	for(i=0; i < L1Params.tagLengthBits; i++)
	{
		L1Params.tagMask = L1Params.tagMask << 1;
		L1Params.tagMask = L1Params.tagMask | 0x00000001;
	}
	L1Params.tagMask = L1Params.tagMask << (32 - L1Params.tagLengthBits);

	L1Params.indexMask = 0;
	for(i=0; i < L1Params.indexLengthBits; i++)
	{
		L1Params.indexMask = L1Params.indexMask << 1;
		L1Params.indexMask = L1Params.indexMask | 0x00000001;
	}

	L1Params.indexMask = L1Params.indexMask << L1Params.offsetLengthBits;

	///////////////////////////////////////////////

	// L2 Cache Parameters - unified cache for data and instruction
	// L2 Size Params
	L2Params.cacheSets 			= 8;
	L2Params.cacheSizeBytes 	= 128 * 1024;
	L2Params.lineSizeBytes 		= 64;
	L2Params.indexLengthBits 	= log_base2(L2Params.cacheSizeBytes / (L2Params.cacheSets * L2Params.lineSizeBytes));
	L2Params.offsetLengthBits 	= log_base2(L2Params.lineSizeBytes);
	L2Params.tagLengthBits 		= 32 - L2Params.indexLengthBits - L2Params.offsetLengthBits;

	// L2 Latencies
	L2Params.cyclesHitRead 			= 20;
	L2Params.cyclesHitWriteThrough 	= 100;
	L2Params.cyclesHitWriteBack		= 25;
	L2Params.cyclesMiss 			= 20;
	L2Params.cyclesMissFlush		= 120;

	// L2 Features
	L2Params.isWriteThrough 	= 1;

	// L2 Derived
	L2Params.cacheLength 		= L2Params.cacheSizeBytes
									/ L2Params.cacheSets
									/ L2Params.lineSizeBytes; // 512

	L2Params.tagMask = 0;
	for(i=0; i < L2Params.tagLengthBits; i++)
	{
		L2Params.tagMask = L2Params.tagMask << 1;
		L2Params.tagMask = L2Params.tagMask | 0x00000001;
	}
	L2Params.tagMask = L2Params.tagMask << (32 - L2Params.tagLengthBits);

	L2Params.indexMask = 0;
	for(i=0; i < L2Params.indexLengthBits; i++)
	{
		L2Params.indexMask = L2Params.indexMask << 1;
		L2Params.indexMask = L2Params.indexMask | 0x00000001;
	}
	L2Params.indexMask = L2Params.indexMask << L2Params.offsetLengthBits;

	//////////////////////////////////////////////////
}

/**
 * Allocates a 2 dimensional array. To be used to allocate space for cache lines
 *
 * @param rows number of rows
 * @param cols number of cols
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

unsigned int generic_simL2ICache(unsigned long address,
		 unsigned int nBytes,
		 unsigned long long *nCycles)
{
	unsigned long index;
	unsigned long tag;
	int set;
	int replaceSet = -1;
	int _address;

	for (_address = address; _address < address + nBytes; _address += 4)
	{
		tag = getTagFromAddress(_address, L2Params.tagLengthBits,
				L2Params.tagMask);
		index = getIndexFromAddress(_address, L2Params.offsetLengthBits,
				L2Params.indexMask);

		for(set = 0; set < L2Params.cacheSets; set++)
		{
			if(L2ICache[set][index].tag == tag &&
					(IS_CACHELINE_VALID(L2ICache[set][index].flags))) // L2 HIT
			{
				// Nothing to do, no cycles spent

				cacheSimStat.access_type = L2_HIT_READ;
				cacheSimStat.nCycles += L2Params.cyclesHitRead;
				*nCycles += L2Params.cyclesHitRead;
				return CACHE_HIT;
			}
			if (replaceSet == -1 && !(IS_CACHELINE_VALID (L2ICache[set][index].flags)))
				replaceSet = set;
		}

		// Cache Miss Occurred

		if (replaceSet == -1)
		{
			replaceSet = L2ICacheReplace[index];
			L2ICacheReplace[index] = (L2ICacheReplace[index] == 7) ? 0 : L2ICacheReplace[index]+1;
		}

		// Evict cache line - nothing to do. No cycles wasted.

		// Already, load new data assuming it will be fetched from L2 or Mem
		L2ICache[replaceSet][index].tag = tag;
		SET_CACHELINE_VALID (L2ICache[replaceSet][index].flags);
		SET_CACHELINE_CLEAN (L2ICache[replaceSet][index].flags);

		cacheSimStat.access_type = L2_MISS;
		cacheSimStat.nCycles += L2Params.cyclesMiss;
		*nCycles += L2Params.cyclesMiss;
	}
	return CACHE_MISS;
}


unsigned int generic_simL1ICache(unsigned long address,
		unsigned int nBytes,
		unsigned long long *nCycles)
{
	unsigned long index;
	unsigned long tag;
	int set;
	int replaceSet = -1;
	int _address;

	for (_address = address; _address < address + nBytes; _address += 4)
	{
		tag = getTagFromAddress(_address, L1Params.tagLengthBits,
				L1Params.tagMask);
		index = getIndexFromAddress(_address, L1Params.offsetLengthBits,
				L1Params.indexMask);

		for(set = 0; set < L1Params.cacheSets; set++)
		{
			if(L1ICache[set][index].tag == tag &&
					(IS_CACHELINE_VALID(L1ICache[set][index].flags))) // L1 HIT
			{
					// Nothing to do, no cycles spent

					cacheSimStat.access_type = L1_HIT_READ;
					cacheSimStat.nCycles += L1Params.cyclesHitRead;
					*nCycles += L1Params.cyclesHitRead;
					return CACHE_HIT;
			}
			if (replaceSet == -1 && !(IS_CACHELINE_VALID (L1ICache[set][index].flags)))
				replaceSet = set;
		}

		// Cache Miss Occurred

		if (replaceSet == -1)
		{
			replaceSet = L1ICacheReplace[index];
			L1ICacheReplace[index] = (L1ICacheReplace[index] == 3) ? 0 : L1ICacheReplace[index]+1;
		}

		// Evict cache line - nothing to do. No cycles wasted.

		// Already, load new data assuming it will be fetched from L2 or Mem
		L1ICache[replaceSet][index].tag = tag;
		SET_CACHELINE_VALID (L1ICache[replaceSet][index].flags);
		SET_CACHELINE_CLEAN (L1ICache[replaceSet][index].flags);

		cacheSimStat.access_type = L1_MISS;
		cacheSimStat.nCycles += L1Params.cyclesMiss;
		*nCycles += L1Params.cyclesMiss;
	}
	return CACHE_MISS;
}

unsigned int generic_simL2DCache(unsigned long address,
		 unsigned int isReadAcccess,
		 unsigned long long *nCycles)
{
	unsigned long index;
	unsigned long tag;
	int set;
	int replaceSet = -1;

	tag = getTagFromAddress(address, L2Params.tagLengthBits,
			L2Params.tagMask);
	index = getIndexFromAddress(address, L2Params.offsetLengthBits,
			L2Params.indexMask);

	for(set = 0; set < L2Params.cacheSets; set++)
	{
		if(L2DCache[set][index].tag == tag &&
				(IS_CACHELINE_VALID(L2DCache[set][index].flags))) // L2 HIT
		{
			if(!isReadAcccess) // Write Access
			{
				if(L2Params.isWriteThrough) // Write Through
				{
					// Data in L2 will be updated, and will remain VALID -
					//    nothing to do

					// Some cycles wasted for data flush
					cacheSimStat.access_type = L2_HIT_WRITETHROUGH;
					cacheSimStat.nCycles += L2Params.cyclesHitWriteThrough;
					*nCycles += L2Params.cyclesHitWriteThrough;
					return CACHE_HIT_WRITETHROUGH;
				}
				else // Write Back
				{
					// Data in L2 will be updated, and will remain VALID. Line
					//   will be marked for flush - nothing to do

					// No extra cycles wasted now for flush
					cacheSimStat.access_type = L2_HIT_WRITEBACK;
					cacheSimStat.nCycles += L2Params.cyclesHitWriteBack;
					*nCycles += L2Params.cyclesHitWriteBack;
					return CACHE_HIT_WRITEBACK;
				}
			}
			else // Read Access
			{
				// Nothing to do, no cycles spent

				cacheSimStat.access_type = L2_HIT_READ;
				cacheSimStat.nCycles += L2Params.cyclesHitRead;
				*nCycles += L2Params.cyclesHitRead;
				return CACHE_HIT;
			}
		}
		if (replaceSet == -1 && !(IS_CACHELINE_VALID (L2DCache[set][index].flags)))
			replaceSet = set;
	}

	// Cache Miss Occurred

	if (replaceSet == -1)
	{
		replaceSet = L2DCacheReplace[index];
		L2DCacheReplace[index] = (L2DCacheReplace[index] == 7) ? 0 : L2DCacheReplace[index]+1;
	}

	if(IS_CACHELINE_DIRTY (L2DCache[replaceSet][index].flags))
	{
		// !! Should never occur, since we are using Write Through Cache.

		// Flush the cache line - nothing to do specifically, just add the
		//   extra nCycles wasted in this case.

		// Already, load new data assuming it will be fetched from L2 or Mem
		L2DCache[replaceSet][index].tag = tag;
		SET_CACHELINE_VALID (L2DCache[replaceSet][index].flags);
		SET_CACHELINE_CLEAN (L2DCache[replaceSet][index].flags);

		cacheSimStat.access_type = L2_MISS_FLUSH;
		cacheSimStat.nCycles += L2Params.cyclesMissFlush;
		*nCycles += L2Params.cyclesMissFlush;
		return CACHE_MISS_FLUSH;
	}
	else
	{
		// Evict cache line - nothing to do. No cycles wasted.

		// Already, load new data assuming it will be fetched from L2 or Mem
		L2DCache[replaceSet][index].tag = tag;
		SET_CACHELINE_VALID (L2DCache[replaceSet][index].flags);
		SET_CACHELINE_CLEAN (L2DCache[replaceSet][index].flags);

		cacheSimStat.access_type = L2_MISS;
		cacheSimStat.nCycles += L2Params.cyclesMiss;
		*nCycles += L2Params.cyclesMiss;
		return CACHE_MISS;
	}
}


unsigned int generic_simL1DCache(unsigned long address,
		 unsigned int isReadAcccess,
		 unsigned long long *nCycles)
{
	unsigned long index;
	unsigned long tag;
	int set;
	int replaceSet = -1;

	tag = getTagFromAddress(address, L1Params.tagLengthBits,
			L1Params.tagMask);
	index = getIndexFromAddress(address, L1Params.offsetLengthBits,
			L1Params.indexMask);

	for(set = 0; set < L1Params.cacheSets; set++)
	{
		if(L1DCache[set][index].tag == tag &&
				(IS_CACHELINE_VALID(L1DCache[set][index].flags))) // L1 HIT
		{
			if(!isReadAcccess) // Write Access
			{
				if(L1Params.isWriteThrough) // Write Through
				{
					// Data in L1 will be updated, and will remain VALID -
					//    nothing to do

					// Some cycles wasted for data flush
					cacheSimStat.access_type = L1_HIT_WRITETHROUGH;
					cacheSimStat.nCycles += L1Params.cyclesHitWriteThrough;
					*nCycles += L1Params.cyclesHitWriteThrough;
					return CACHE_HIT_WRITETHROUGH;
				}
				else // Write Back
				{
					// Data in L1 will be updated, and will remain VALID. Line
					//   will be marked for flush - nothing to do

					// No extra cycles wasted now for flush
					cacheSimStat.access_type = L1_HIT_WRITEBACK;
					cacheSimStat.nCycles += L1Params.cyclesHitWriteBack;
					*nCycles += L1Params.cyclesHitWriteBack;
					return CACHE_HIT_WRITEBACK;
				}
			}
			else // Read Access
			{
				// Nothing to do, no cycles spent

				cacheSimStat.access_type = L1_HIT_READ;
				cacheSimStat.nCycles += L1Params.cyclesHitRead;
				*nCycles += L1Params.cyclesHitRead;
				return CACHE_HIT;
			}
		}
		if (replaceSet == -1 && !(IS_CACHELINE_VALID (L1DCache[set][index].flags)))
			replaceSet = set;
	}

	// Cache Miss Occurred

	if (replaceSet == -1)
	{
		replaceSet = L1DCacheReplace[index];
		L1DCacheReplace[index] = (L1DCacheReplace[index] == 3) ? 0 : L1DCacheReplace[index]+1;
	}

	if(IS_CACHELINE_DIRTY (L1DCache[replaceSet][index].flags))
	{
		// !! Should never occur, since we are using Write Through Cache.

		// Flush the cache line - nothing to do specifically, just add the
		//   extra nCycles wasted in this case.

		// Already, load new data assuming it will be fetched from L2 or Mem
		L1DCache[replaceSet][index].tag = tag;
		SET_CACHELINE_VALID (L1DCache[replaceSet][index].flags);
		SET_CACHELINE_CLEAN (L1DCache[replaceSet][index].flags);

		cacheSimStat.access_type = L1_MISS_FLUSH;
		cacheSimStat.nCycles += L1Params.cyclesMissFlush;
		*nCycles += L1Params.cyclesMissFlush;
		return CACHE_MISS_FLUSH;
	}
	else
	{
		// Evict cache line - nothing to do. No cycles wasted.

		// Already, load new data assuming it will be fetched from L2 or Mem
		L1DCache[replaceSet][index].tag = tag;
		SET_CACHELINE_VALID (L1DCache[replaceSet][index].flags);
		SET_CACHELINE_CLEAN (L1DCache[replaceSet][index].flags);

		cacheSimStat.access_type = L1_MISS;
		cacheSimStat.nCycles += L1Params.cyclesMiss;
		*nCycles += L1Params.cyclesMiss;
		return CACHE_MISS;
	}
}

/**
 * Simulates Instruction Cache access by benchmark
 *
 * @param address Starting address of instructions in the basic block
 * @param nBytes Number of bytes of instructions accessed in the basic block
 *
 * @return number of clock cycles spent
 */
unsigned long long generic_simICache(unsigned long address, unsigned int nBytes)
{
	unsigned long long nCycles = 0;
	unsigned int ret;

	ret = generic_simL1ICache(address, nBytes, &nCycles);

	if(CACHE_MISS == ret || CACHE_MISS_FLUSH == ret)
	{
		// L1 Data Cache Miss has occured, simulate L2 Access.
		ret = generic_simL2ICache(address, nBytes, &nCycles);
		if(CACHE_MISS == ret || CACHE_MISS_FLUSH == ret)
		{
			nCycles += cyclesMemAccess;
		}
	}

	return nCycles;
}

/**
 * Simulates Data Cache access by benchmark
 *
 * @param address Address of data accessed
 *
 * @return number of clock cycles spent
 */
unsigned long long generic_simDCache(unsigned long address, unsigned int isReadAccess)
{
	unsigned long long nCycles = 0;
	unsigned int ret;

	ret = generic_simL1DCache(address, isReadAccess, &nCycles);

	if(CACHE_MISS == ret || CACHE_MISS_FLUSH == ret)
	{
		// L1 Data Cache Miss has occured, simulate L2 Access.
		ret = generic_simL2DCache(address, isReadAccess, &nCycles);
		if(CACHE_MISS == ret || CACHE_MISS_FLUSH == ret)
		{
			nCycles += cyclesMemAccess;
		}
	}

	return nCycles;
}

/**
 * Initialize the cache data structures
 */
void generic_cacheSimInit()
{
	readConfigFile();

	// allocating space for storing the cache lines in a 2d array
	// L1 Data cache
	L1DCache = (struct cacheLine_t **) alloc2D (L1Params.cacheSets,
			L1Params.cacheLength, sizeof(struct cacheLine_t));
	L1DCacheReplace = (unsigned int *) malloc((size_t) L1Params.cacheLength *
			sizeof(unsigned int));

	// L1 Instruction Cache
	L1ICache = (struct cacheLine_t **) alloc2D (L1Params.cacheSets,
			L1Params.cacheLength, sizeof(struct cacheLine_t));
	L1ICacheReplace = (unsigned int *) malloc((size_t) L1Params.cacheLength *
				sizeof(unsigned int));

	// L2 Data Cache
	L2DCache = (struct cacheLine_t **) alloc2D (L2Params.cacheSets,
				L2Params.cacheLength, sizeof(struct cacheLine_t));
	L2DCacheReplace = (unsigned int *) malloc((size_t) L2Params.cacheLength *
				sizeof(unsigned int));

	// L2 Instruction Cache
	L2ICache = (struct cacheLine_t **) alloc2D (L2Params.cacheSets,
				L2Params.cacheLength, sizeof(struct cacheLine_t));
	L2ICacheReplace = (unsigned int *) malloc((size_t) L2Params.cacheLength *
				sizeof(unsigned int));

}

/**
 * Frees data structures and cleans up
 *
 */
void generic_cacheSimFini()
{
	free(L1DCache);
}

struct cacheSimHwMod_t hwMod = {
		.simDCache = &generic_simDCache,
		.simICache = &generic_simICache,
		.cacheSimInit = &generic_cacheSimInit,
		.cacheSimFini = &generic_cacheSimFini
};
