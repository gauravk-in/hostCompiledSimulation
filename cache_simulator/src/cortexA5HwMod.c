#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

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
	unsigned int subIndexLenBits;

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

unsigned int memWriteLatency = 0;
unsigned int memReadLatency = 55;
unsigned int memReadPrefetchLatency = 0;

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
unsigned long L2I_Miss = 0;
unsigned long L2D_Miss = 0;

#define PREFETCH_TABLE_MAX_ENTRIES 3

unsigned int prefetch_table_entries;

struct prevAccess
{
	unsigned long address;
	unsigned long sequentialAccess;
	struct prevAccess *next;
	struct prevAccess *prev;
};
typedef struct prevAccess prevAccess_t;

prevAccess_t *prevAccessList_head;
prevAccess_t *prevAccessList_tail;

// Round Robin L2 Cache Replacement
unsigned int *L2_RR_evictSetIndex;

/**** LOCAL FUNCTIONS *********************************************************/

void insertAccess(prevAccess_t **head, prevAccess_t **tail, unsigned long address, unsigned long seqAccess)
{
	prevAccess_t *new_entry;

	if (*head == NULL && *tail == NULL)
	{
		// Empty
		new_entry = malloc(sizeof(prevAccess_t));
		new_entry->address = address;
		new_entry->sequentialAccess = seqAccess;
		*head = new_entry;
		*tail = new_entry;
		new_entry->next = new_entry;
		new_entry->prev = new_entry;
		prefetch_table_entries++;
	}
	else{
		if(prefetch_table_entries < PREFETCH_TABLE_MAX_ENTRIES)
		{
			new_entry = malloc(sizeof(prevAccess_t));
			new_entry->address = address;
			new_entry->sequentialAccess = seqAccess;
			(*tail)->next = new_entry;
			new_entry->prev = *tail;
			new_entry->next = *head;
			(*head)->prev = new_entry;
			(*tail) = new_entry;
			prefetch_table_entries++;
		}
		else
		{
			(*head)->address = address;
			(*head)->sequentialAccess = seqAccess;
			(*head) = (*head)->next;
			(*tail) = (*tail)->next;
		}
	}

	return;
}

int log_base2(int val)
{
	int ret = 0;
	val >>= 1;
	while (val)
	{
		++ret;
		val >>= 1;
	}
	return ret;
}

void initCacheParams ()
{
	int i;

	/*** L1 DCache *****************/

	L1DCacheConf.lineLenBytes 		= 32;
	L1DCacheConf.cacheSizeBytes 	= 32 * 1024; // 4 KB
	L1DCacheConf.numSets 			= 4;

	L1DCacheConf.numLines  			= L1DCacheConf.cacheSizeBytes /
			(L1DCacheConf.lineLenBytes * L1DCacheConf.numSets);

	L1DCacheConf.subIndexLenBits = log_base2(L1DCacheConf.lineLenBytes);
	L1DCacheConf.indexLenBits = log_base2(L1DCacheConf.numLines);
	L1DCacheConf.indexMask = 0;
	for (i = 0; i < L1DCacheConf.indexLenBits; i++)
	{
		L1DCacheConf.indexMask = L1DCacheConf.indexMask << 1;
		L1DCacheConf.indexMask |= 1;
	}
	L1DCacheConf.indexMask = L1DCacheConf.indexMask << L1DCacheConf.subIndexLenBits;

	L1DCacheConf.tagLenBits = ADDRESS_LEN_BITS - L1DCacheConf.indexLenBits - L1DCacheConf.subIndexLenBits;
	L1DCacheConf.tagMask = 0;
	for (i = 0; i < L1DCacheConf.tagLenBits; i++)
	{
		L1DCacheConf.tagMask = L1DCacheConf.tagMask << 1;
		L1DCacheConf.tagMask |= 1;
	}
	L1DCacheConf.tagMask = L1DCacheConf.tagMask << (L1DCacheConf.indexLenBits + L1DCacheConf.subIndexLenBits);

	L1DCacheConf.isWriteThrough = 0;

	L1DCacheConf.hitLatency = 0;
	L1DCacheConf.missLatency = 0;


	/*** L1 ICache *****************/

	L1ICacheConf.lineLenBytes 		= 32;
	L1ICacheConf.cacheSizeBytes 	= 32 * 1024; // 4 KB
	L1ICacheConf.numSets 			= 2;

	L1ICacheConf.numLines  			= L1ICacheConf.cacheSizeBytes /
			(L1ICacheConf.lineLenBytes * L1ICacheConf.numSets);

	L1ICacheConf.subIndexLenBits = log_base2(L1ICacheConf.lineLenBytes);
	L1ICacheConf.indexLenBits = log_base2(L1ICacheConf.numLines);
	L1ICacheConf.indexMask = 0;
	for (i = 0; i < L1ICacheConf.indexLenBits; i++)
	{
		L1ICacheConf.indexMask = L1ICacheConf.indexMask << 1;
		L1ICacheConf.indexMask |= 0x00000001;
	}
	L1ICacheConf.indexMask = L1ICacheConf.indexMask << L1ICacheConf.subIndexLenBits;

	L1ICacheConf.tagLenBits = ADDRESS_LEN_BITS - L1ICacheConf.indexLenBits - L1ICacheConf.subIndexLenBits;
	L1ICacheConf.tagMask = 0;
	for (i = 0; i < L1ICacheConf.tagLenBits; i++)
	{
		L1ICacheConf.tagMask = L1ICacheConf.tagMask << 1;
		L1ICacheConf.tagMask |= 0x00000001;
	}
	L1ICacheConf.tagMask = L1ICacheConf.tagMask << (L1ICacheConf.indexLenBits + L1ICacheConf.subIndexLenBits);

	L1ICacheConf.isWriteThrough = 0;

	L1ICacheConf.hitLatency = 0;
	L1ICacheConf.missLatency = 0;


	/*** L2 Cache *****************/

	L2CacheConf.lineLenBytes 		= 32;
	L2CacheConf.cacheSizeBytes 		= 512 * 1024; // 256 KB
	L2CacheConf.numSets 			= 16;

	L2CacheConf.numLines  			= L2CacheConf.cacheSizeBytes /
			(L2CacheConf.lineLenBytes * L2CacheConf.numSets);

	L2CacheConf.subIndexLenBits = log_base2(L2CacheConf.lineLenBytes);
//	assert(5 == subIndexLen);
	L2CacheConf.indexLenBits = log_base2(L2CacheConf.numLines);
	L2CacheConf.indexMask = 0;
	for (i = 0; i < L2CacheConf.indexLenBits; i++)
	{
		L2CacheConf.indexMask = L2CacheConf.indexMask << 1;
		L2CacheConf.indexMask |= 0x00000001;
	}
	L2CacheConf.indexMask = L2CacheConf.indexMask << L2CacheConf.subIndexLenBits;

	L2CacheConf.tagLenBits = ADDRESS_LEN_BITS - L2CacheConf.indexLenBits - L2CacheConf.subIndexLenBits;
	L2CacheConf.tagMask = 0;
	for (i = 0; i < L2CacheConf.tagLenBits; i++)
	{
		L2CacheConf.tagMask = L2CacheConf.tagMask << 1;
		L2CacheConf.tagMask |= 0x00000001;
	}
	L2CacheConf.tagMask = L2CacheConf.tagMask << (L2CacheConf.indexLenBits + L2CacheConf.subIndexLenBits);

	L2CacheConf.isWriteThrough = 0;

	L2CacheConf.hitLatency = 16;
	L2CacheConf.missLatency = 16;
}


/**
 * Allocates a 2 dimensional array. To be used to allocate space for cache lines
 *
 * @param rows number of cache lines
 * @param cols number of sets
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
		unsigned int nBytes,
		struct csim_result_t *result)
{
	unsigned int latency = 0;
	unsigned long tag;
	unsigned long index;
	unsigned long _address;
	int setIndex = 0;
	int invalidSetIndex;
	int hit = 0;
	unsigned long address_32;

	address_32 = address & (~(L1ICacheConf.lineLenBytes-1));
	for (_address = address_32; _address <= address + nBytes; _address += L1ICacheConf.lineLenBytes)
	{
		tag = getTagFromAddress(_address, L1ICacheConf.tagLenBits, L1ICacheConf.tagMask);
		index = getIndexFromAddress(_address, L1ICacheConf.subIndexLenBits, L1ICacheConf.indexMask);

		hit = 0;
		invalidSetIndex = -1;
		for (setIndex = 0; setIndex < L1ICacheConf.numSets; setIndex++)
		{
			if (IS_CACHELINE_VALID(L1ICache[setIndex][index].flags))
			{
				if (L1ICache[setIndex][index].tag == tag)
				{
					latency += L1ICacheConf.hitLatency;
					L1I_Hit_Read++;
					result->L1Hits++;
					result->latency += L1ICacheConf.hitLatency;
					hit = 1;
					break;
				}
			}
			else
			{
				invalidSetIndex = setIndex;
			}
		}

		if (hit)
			continue;

		// L1 Miss has occured!
		L1I_Miss++;
		latency += L1ICacheConf.missLatency;
		result->latency += L1ICacheConf.missLatency;

		// Data will be present for next access!
		if (invalidSetIndex == -1)
		{
			invalidSetIndex = random() % L1ICacheConf.numSets;

#define EXCLUSIVE_L2_CACHE
#ifdef EXCLUSIVE_L2_CACHE
			{
				unsigned long L1ReplaceAdd;
				/**
				 * Any address is contained in either L1 or L2 Cache. Evicted
				 * data from L1 Cache, is stored to L2 Cache.
				 */

				// Extract the replaced address
				L1ReplaceAdd = L1ICache[index][invalidSetIndex].tag <<
						(ADDRESS_LEN_BITS - L1ICacheConf.tagLenBits);
				L1ReplaceAdd += index << L1ICacheConf.subIndexLenBits;

				// Store replaced address in L2.
				{
					unsigned long l2Tag;
					unsigned long l2Index;
					unsigned int l2InvalidSetIndex;

					l2Tag = getTagFromAddress(L1ReplaceAdd, L2CacheConf.tagLenBits,
							L2CacheConf.tagMask);
					l2Index = getIndexFromAddress(L1ReplaceAdd, L2CacheConf.subIndexLenBits,
							L2CacheConf.indexMask);

					l2InvalidSetIndex = -1;
					for(setIndex = 0; setIndex < L2CacheConf.numSets; setIndex++)
					{
						if(!IS_CACHELINE_VALID(L2Cache[l2Index][setIndex].flags))
						{
							l2InvalidSetIndex = setIndex;
						}
					}

					if(l2InvalidSetIndex == -1)
					{
//						l2InvalidSetIndex = random() % L2CacheConf.numSets;
						l2InvalidSetIndex = L2_RR_evictSetIndex[l2Index]++;
						if (L2_RR_evictSetIndex[l2Index] == L2CacheConf.numSets)
							L2_RR_evictSetIndex[l2Index] = 0;

						if(IS_CACHELINE_DIRTY(L2Cache[l2Index][l2InvalidSetIndex].flags))
						{
							// Write Back to memory!
//							latency += memWriteLatency;
							L2_Hit_Writeback++;
						}
					}
					L2Cache[l2Index][l2InvalidSetIndex].tag = l2Tag;

					// Add Latency to write to L2
					// TODO: May not be needed, due to Store Buffering !!!!
//					latency += L2CacheConf.hitLatency;
//					result->latency += L2CacheConf.hitLatency;
				}
			}
#endif
		}
		L1ICache[invalidSetIndex][index].tag = tag;
		SET_CACHELINE_VALID(L1ICache[invalidSetIndex][index].flags);

		tag = getTagFromAddress(_address, L2CacheConf.tagLenBits, L2CacheConf.tagMask);
		index = getIndexFromAddress(_address, L2CacheConf.subIndexLenBits, L2CacheConf.indexMask);

		hit = 0;
		for (setIndex = 0; setIndex < L2CacheConf.numSets; setIndex++)
		{
			if (IS_CACHELINE_VALID(L2Cache[setIndex][index].flags))
			{
				if (L2Cache[setIndex][index].tag == tag)
				{
					latency += L2CacheConf.hitLatency;
					L2_Hit_Read++;
					result->L2Hits++;
					result->latency += L2CacheConf.hitLatency;
					hit = 1;
					break;
				}
			}
		}

		if(hit)
			continue;

		// L2 Miss has occured!
//		L1I_Miss--;
		L2I_Miss++;
		result->L2Misses++;
		latency += L2CacheConf.missLatency;
		result->latency += L2CacheConf.missLatency;
		latency += memReadLatency;
		result->latency += memReadLatency;
	}
	return latency;
}

unsigned long long cortexA5_simDCache(unsigned long address,
		unsigned int isReadAccess,
		struct csim_result_t *result)
{
	unsigned int latency = 0;
	unsigned long tag;
	unsigned long index;
	int setIndex = 0;
	int invalidSetIndex;
	unsigned long L1ReplaceAdd = 0;
	unsigned int L1ReplaceAddFlags = 0;

	// TODO : Implement the mechanism for Write Through Cache.
	/**
	 * For write through, the latency will be memWriteLatency. Allocate the data
	 * in L1 Cache.
	 *
	 * For write back cache, we need to check if data is already in cache. We do
	 * that later.
	 */

	tag = getTagFromAddress(address, L1DCacheConf.tagLenBits, L1DCacheConf.tagMask);
	index = getIndexFromAddress(address, L1DCacheConf.subIndexLenBits, L1DCacheConf.indexMask);

	invalidSetIndex = -1;
	for (setIndex = 0; setIndex < L1DCacheConf.numSets; setIndex++)
	{
		if (IS_CACHELINE_VALID(L1DCache[index][setIndex].flags))
		{
			if (L1DCache[index][setIndex].tag == tag)
			{
				// Add the latency
				latency += L1DCacheConf.hitLatency;

				if (isReadAccess)
				{
					L1D_Hit_Read++;
					result->L1Hits++;
				}
				else // Write Access
				{
					L1D_Hit_Writeback++;
					SET_CACHELINE_DIRTY(L1DCache[index][setIndex].flags);
				}

				// If data was found in L1 Cache, we return from here!!
				result->latency += latency;
				return latency;
			}
		}
		else
		{
			invalidSetIndex = setIndex;
		}
	}

	// L1 Miss has occured!
	L1D_Miss++;
	latency += L1DCacheConf.missLatency;

	// Allocate Space for Data which will be present next time!!
	if (invalidSetIndex == -1)
	{
		// Replace a random cache line
		invalidSetIndex = random() % L1DCacheConf.numSets;

#define EXCLUSIVE_L2_CACHE
#ifdef EXCLUSIVE_L2_CACHE
		/**
		 * Any address is contained in either L1 or L2 Cache. Eviceted data
		 * from L1 Cache, is stored to L2 Cache.
		 */

		// Extract the replaced address
		L1ReplaceAdd = L1DCache[index][invalidSetIndex].tag <<
				(ADDRESS_LEN_BITS - L1DCacheConf.tagLenBits);
		L1ReplaceAdd += index << L1DCacheConf.subIndexLenBits;
		L1ReplaceAddFlags = L1DCache[index][invalidSetIndex].flags;

		// Store replaced address in L2.
		{
			unsigned long l2Tag;
			unsigned long l2Index;
			unsigned int l2InvalidSetIndex;

			l2Tag = getTagFromAddress(L1ReplaceAdd, L2CacheConf.tagLenBits,
					L2CacheConf.tagMask);
			l2Index = getIndexFromAddress(L1ReplaceAdd, L2CacheConf.subIndexLenBits,
					L2CacheConf.indexMask);

			l2InvalidSetIndex = -1;
			for(setIndex = 0; setIndex < L2CacheConf.numSets; setIndex++)
			{
				if(!IS_CACHELINE_VALID(L2Cache[l2Index][setIndex].flags))
				{
					l2InvalidSetIndex = setIndex;
				}
			}

			if(l2InvalidSetIndex == -1)
			{
//				printf("l2_RR_evictSetIndex = %d\n", L2_RR_evictSetIndex);
//				l2InvalidSetIndex = random() % L2CacheConf.numSets;
				l2InvalidSetIndex = L2_RR_evictSetIndex[l2Index]++;
				if (L2_RR_evictSetIndex[l2Index] == L2CacheConf.numSets)
					L2_RR_evictSetIndex[l2Index] = 0;

				if(IS_CACHELINE_DIRTY(L2Cache[l2Index][l2InvalidSetIndex].flags))
				{
					// Write Back to memory!
					latency += memWriteLatency;
					L2_Hit_Writeback++;
				}
			}

			L2Cache[l2Index][l2InvalidSetIndex].tag = l2Tag;
			L2Cache[l2Index][l2InvalidSetIndex].flags = L1ReplaceAddFlags;

			// Add Latency to write to L2
			// TODO: May not be needed, due to Store Buffering !!!!
//			latency += L2CacheConf.hitLatency;
		}
#endif
	}
	// Make new data available
	L1DCache[index][invalidSetIndex].tag = tag;
	SET_CACHELINE_VALID(L1DCache[index][invalidSetIndex].flags);
	if(!isReadAccess)
		SET_CACHELINE_DIRTY(L1DCache[index][invalidSetIndex].flags);
	else
		SET_CACHELINE_CLEAN(L1DCache[index][invalidSetIndex].flags);

	// Lookup Data in L2 Cache
	tag = getTagFromAddress(address, L2CacheConf.tagLenBits, L2CacheConf.tagMask);
	index = getIndexFromAddress(address, L2CacheConf.subIndexLenBits, L2CacheConf.indexMask);

	for (setIndex = 0; setIndex < L2CacheConf.numSets; setIndex++)
	{
		if (IS_CACHELINE_VALID(L2Cache[index][setIndex].flags))
		{
			if (L2Cache[index][setIndex].tag == tag)
			{
				/**
				 * If data is found in L2, just mark the line as invalid,
				 * to mark that the data has been moved to L1. The data was
				 * already made available in L1.
				 *
				 * Add the latency.
				 */

				latency += L2CacheConf.hitLatency;
				SET_CACHELINE_INVALID(L2Cache[index][setIndex].flags);
				SET_CACHELINE_CLEAN(L2Cache[index][setIndex].flags);
				L2_Hit_Read++;
				result->L2Hits++;
				result->latency += latency;
				return latency;
			}
		}
	}

	// L2 Miss has occured!
	L1D_Miss--;
	L2D_Miss++;
	result->L2Misses++;
	latency += L2CacheConf.missLatency;

	/**
	 * Data will directly be loaded to L1 Cache. Nothing to do, if L2 Miss.
	 */

#define DATA_PREFETCH
#ifdef DATA_PREFETCH
	/**
	 * Checking for data prefetch at the end! Probably, need to do this in the
	 * beginning.
	 */

	if(isReadAccess)
	{
		int i;

		prevAccess_t *access = prevAccessList_tail;
		for (i = 0; i < prefetch_table_entries && access != NULL; i++)
		{
			if (address == access->address + L2CacheConf.lineLenBytes)
			{
				if (access->sequentialAccess > 25)
				{
					/**
					 * Data would have been prefetched !!
					 * Important:
					 * 1. Data has already been loaded into L1 earlier.
					 * 2. Latencies added if here, are L1 Miss and L2 Miss.
					 *    These latencies need not be added if prefetched!!
					 * 3. Incremement L1 Hit, and count for prefetches!
					 * 4. Decrement L2 Miss count.
					 */

					latency = memReadPrefetchLatency;
					result->prefetches++;
					result->L1Hits++;
					result->L2Misses--;
				}
				insertAccess(&prevAccessList_head, &prevAccessList_tail, address, access->sequentialAccess+1);
				result->latency += latency;
				return latency;
			}
			access = access->prev;
		}
		insertAccess(&prevAccessList_head, &prevAccessList_tail, address, 0);
	}
#endif

	/**
	 * Data must be fetched from the memory !!!
	 * Add the memReadLatency only!
	 */
	latency += memReadLatency;
	result->latency += latency;
	return latency;
}

void cortexA5_cacheSimInit(struct csim_result_t *result)
{
	// Allocate space for caches
	initCacheParams();

	result->L1Hits = 0;
	result->L2Hits = 0;
	result->L2Misses = 0;
	result->prefetches = 0;
	result->latency = 0;

	L1DCache = (cacheLine_t **) alloc2D(L1DCacheConf.numLines,
				L1DCacheConf.numSets, sizeof(cacheLine_t));
	L1ICache = (cacheLine_t **) alloc2D(L1ICacheConf.numLines,
				L1ICacheConf.numSets, sizeof(cacheLine_t));
	L2Cache = (cacheLine_t **) alloc2D(L2CacheConf.numLines,
				L2CacheConf.numSets, sizeof(cacheLine_t));

	prevAccessList_head = NULL;
	prevAccessList_tail = NULL;
	prefetch_table_entries = 0;

	L2_RR_evictSetIndex = (unsigned int*) malloc(L2CacheConf.numLines * sizeof(unsigned int));
	memset(L2_RR_evictSetIndex, 0, sizeof(unsigned int) * L2CacheConf.numLines);

	return;
}

void cortexA5_cacheSimFini(struct csim_result_t *result)
{
	printf("Statistics : \n");

	printf ("\nTotal L1 Hits = %llu\n", result->L1Hits);
	printf ("Total L2 Hits = %llu\n", result->L2Hits);
	printf ("Total L2 Misses = %llu\n", result->L2Misses);
	printf ("Total Prefetches = %llu\n", result->prefetches);
	printf ("Mem Access Cycles = %llu\n", result->latency);

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
	printf("\t Inst. Miss = %ld\n", L2I_Miss);
	printf("\t Data Miss = %ld\n", L2D_Miss);

	free(L1DCache);
	free(L1ICache);
	free(L2Cache);
	free(L2_RR_evictSetIndex);

	return;
}

struct cacheSimHwMod_t hwMod = {
		.simDCache = &cortexA5_simDCache,
		.simICache = &cortexA5_simICache,
		.cacheSimInit = &cortexA5_cacheSimInit,
		.cacheSimFini = &cortexA5_cacheSimFini
};
