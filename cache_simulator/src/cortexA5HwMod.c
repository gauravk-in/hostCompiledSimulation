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

unsigned int memWriteLatency = 55;
unsigned int memReadLatency = 55;
unsigned int memReadPrefetchLatency = 10;

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
	while (val >>= 1) ++ret;
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
		L1DCacheConf.indexMask |= 0x00000001;
	}
	L1DCacheConf.indexMask = L1DCacheConf.indexMask << L1DCacheConf.subIndexLenBits;

	L1DCacheConf.tagLenBits = ADDRESS_LEN_BITS - L1DCacheConf.indexLenBits - L1DCacheConf.subIndexLenBits;
	L1DCacheConf.tagMask = 0;
	for (i = 0; i < L1DCacheConf.tagLenBits; i++)
	{
		L1DCacheConf.tagMask = L1DCacheConf.tagMask << 1;
		L1DCacheConf.tagMask |= 0x00000001;
	}
	L1DCacheConf.tagMask = L1DCacheConf.tagMask << (L1DCacheConf.indexLenBits + L1DCacheConf.subIndexLenBits);

	L1DCacheConf.isWriteThrough = 0;

	L1DCacheConf.hitLatency = 2;
	L1DCacheConf.missLatency = 2;


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

	L1ICacheConf.hitLatency = 2;
	L1ICacheConf.missLatency = 2;


	/*** L2 Cache *****************/

	L2CacheConf.lineLenBytes 		= 32;
	L2CacheConf.cacheSizeBytes 		= 512 * 1024; // 32 KB
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
	unsigned long _address;
	int setIndex = 0;
	int replaceIndex;

	for (_address = address; _address <= address + nBytes; _address += 4)
	{
		tag = getTagFromAddress(_address, L1ICacheConf.tagLenBits, L1ICacheConf.tagMask);
		index = getIndexFromAddress(_address, L1ICacheConf.subIndexLenBits, L1ICacheConf.indexMask);

		replaceIndex = -1;
		for (setIndex = 0; setIndex < L1ICacheConf.numSets; setIndex++)
		{
			if (IS_CACHELINE_VALID(L1ICache[setIndex][index].flags))
			{
				if (L1ICache[setIndex][index].tag == tag)
				{
					latency += L1ICacheConf.hitLatency;
					L1I_Hit_Read++;
					return latency;
				}
			}
			else
			{
				replaceIndex = setIndex;
			}
		}
		// L1 Miss has occured!
		L1I_Miss++;
		latency += L1ICacheConf.missLatency;

		// Data will be present for next access!
		if (replaceIndex == -1)
			replaceIndex = random() % L1ICacheConf.numSets;
		L1ICache[replaceIndex][index].tag = tag;
		SET_CACHELINE_VALID(L1ICache[replaceIndex][index].flags);

		tag = getTagFromAddress(_address, L2CacheConf.tagLenBits, L2CacheConf.tagMask);
		index = getIndexFromAddress(_address, L2CacheConf.subIndexLenBits, L2CacheConf.indexMask);

		replaceIndex = -1;
		for (setIndex = 0; setIndex < L2CacheConf.numSets; setIndex++)
		{
			if (IS_CACHELINE_VALID(L2Cache[setIndex][index].flags))
			{
				if (L2Cache[setIndex][index].tag == tag)
				{
					latency += L2CacheConf.hitLatency;
					L2_Hit_Read++;
					return latency;
				}
			}
			else
			{
				replaceIndex = setIndex;
			}
		}

		// L2 Miss has occured!
		L1I_Miss--;
		L2I_Miss++;
		latency += L2CacheConf.missLatency;

		// Data will be present for next access!
		if (replaceIndex == -1)
			replaceIndex = random() % L2CacheConf.numSets;
		L2Cache[replaceIndex][index].tag = tag;
		SET_CACHELINE_VALID(L2Cache[replaceIndex][index].flags);

		latency += memReadLatency;
	}

	return latency;
}


unsigned long long cortexA5_simDCache(unsigned long address,
										   unsigned int isReadAccess)
{
	unsigned int latency = 0;
	unsigned long tag;
	unsigned long index;
	int setIndex = 0;
	int replaceIndex;
	int i;

	if (isReadAccess == 0 && L1DCacheConf.isWriteThrough == 1) // Write Access
	{
		// Simply increment latency by time to write to memory
		latency += memWriteLatency;
		L1D_Hit_Writethrough++;
		return latency;
	}
	// For writeback, there is no latency. We can safely take this assumption,
	//   as we are only using a Single Core System.

	tag = getTagFromAddress(address, L1DCacheConf.tagLenBits, L1DCacheConf.tagMask);
	index = getIndexFromAddress(address, L1DCacheConf.subIndexLenBits, L1DCacheConf.indexMask);

	replaceIndex = -1;
	for (setIndex = 0; setIndex < L1DCacheConf.numSets; setIndex++)
	{
		if (IS_CACHELINE_VALID(L1DCache[setIndex][index].flags))
		{
			if (L1DCache[setIndex][index].tag == tag)
			{
				latency += L1DCacheConf.hitLatency;
				if (isReadAccess)
					L1D_Hit_Read++;
				else
					L1D_Hit_Writeback++;
				return latency;
			}
		}
		else
		{
			replaceIndex = setIndex;
		}
	}
	// L1 Miss has occured!
	L1D_Miss++;
	latency += L1DCacheConf.missLatency;

	// Data will be present for next access!
	if (replaceIndex == -1)
		replaceIndex = random() % L1DCacheConf.numSets;
	L1DCache[replaceIndex][index].tag = tag;
	SET_CACHELINE_VALID(L1DCache[replaceIndex][index].flags);

	tag = getTagFromAddress(address, L2CacheConf.tagLenBits, L2CacheConf.tagMask);
	index = getIndexFromAddress(address, L2CacheConf.subIndexLenBits, L2CacheConf.indexMask);

	replaceIndex = -1;
	for (setIndex = 0; setIndex < L2CacheConf.numSets; setIndex++)
	{
		if (IS_CACHELINE_VALID(L2Cache[setIndex][index].flags))
		{
			if (L2Cache[setIndex][index].tag == tag)
			{
				latency += L2CacheConf.hitLatency;
				if (isReadAccess)
					L2_Hit_Read++;
				else
					L2_Hit_Writeback++;
				return latency;
			}
		}
		else
		{
			replaceIndex = setIndex;
		}
	}

	// L2 Miss has occured!
	L1D_Miss--;
	L2D_Miss++;
	latency += L2CacheConf.missLatency;

	// Data will be present for next access!
	if (replaceIndex == -1)
		replaceIndex = random() % L2CacheConf.numSets;
	L2Cache[replaceIndex][index].tag = tag;
	SET_CACHELINE_VALID(L2Cache[replaceIndex][index].flags);

	prevAccess_t *access = prevAccessList_tail;
	for (i = 0; i < prefetch_table_entries && access != NULL; i++)
	{

		if (address == access->address + L2CacheConf.lineLenBytes)
		{
			//printf("0x%lx - 0x%lx\n", access->address, address);
			if (access->sequentialAccess > 5)
			{
				latency += memReadPrefetchLatency;
			}
			insertAccess(&prevAccessList_head, &prevAccessList_tail, address, access->sequentialAccess+1);
			return latency;
		}
		access = access->prev;
	}

	latency += memReadLatency;
	insertAccess(&prevAccessList_head, &prevAccessList_tail, address, 0);
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

	prevAccessList_head = NULL;
	prevAccessList_tail = NULL;
	prefetch_table_entries = 0;

	return;
}

void cortexA5_cacheSimFini()
{
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
	printf("\t Inst. Miss = %ld\n", L2I_Miss);
	printf("\t Data Miss = %ld\n", L2D_Miss);

	free(L1DCache);
	free(L1ICache);
	free(L2Cache);

	return;
}

struct cacheSimHwMod_t hwMod = {
		.simDCache = &cortexA5_simDCache,
		.simICache = &cortexA5_simICache,
		.cacheSimInit = &cortexA5_cacheSimInit,
		.cacheSimFini = &cortexA5_cacheSimFini
};
