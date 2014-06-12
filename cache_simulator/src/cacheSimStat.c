/**
 * cacheSimStat.c
 * Purpose: This code basically collects the results from cache simulation,
 * and records the statistics for reporting later.
 */

#include <stdio.h>
#include "cacheSimStat.h"

/**
 * Global Variable used to receive simulation statistics from HW Model
 * Implementation.
 */
struct cacheSimStat_t cacheSimStat;

static unsigned long nAccesses = 0;
static unsigned long nL1Miss = 0;
static unsigned long nL1Hit = 0;
static unsigned long nL2Hit = 0;
static unsigned long nL2Miss = 0;

void cacheSimStatCollect()
{
	nAccesses++;
	switch(cacheSimStat.access_type)
	{
		case L1_HIT_READ:
		case L1_HIT_WRITEBACK:
		case L1_HIT_WRITETHROUGH:
			nL1Hit++;
			break;
		case L1_MISS:
		case L1_MISS_FLUSH:
			nL1Miss++;
			break;
		case L2_HIT_READ:
		case L2_HIT_WRITEBACK:
		case L2_HIT_WRITETHROUGH:
			nL1Miss++;
			nL2Hit++;
			break;
		case L2_MISS:
		case L2_MISS_FLUSH:
			nL1Miss++;
			nL2Miss++;
			break;
		default:
			break;
	}
}

void cacheSimStatPrint()
{
	printf("Accesses = %lu \n"
			"L1 Hits = %lu \n"
			"L1 Miss = %lu (L1 Miss Rate = %lu) \n"
			"L2 Hits = %lu \n"
			"L2 Miss = %lu (L2 Miss Rate = %lu) \n",
			nAccesses, nL1Hit, nL1Miss, nL1Miss*100/nAccesses,
			nL2Hit, nL2Miss, nL2Miss*100/nAccesses);
}

