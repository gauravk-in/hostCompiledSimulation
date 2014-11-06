#include <stdio.h>
#include <stdlib.h>

#define BPRED_TABLE_MAX_ENTRIES 125

enum predictionValues {
	UNKNOWN = -1,
	STRONGLY_TAKEN = 0,
	WEAKLY_TAKEN,
	WEAKLY_NOT_TAKEN,
	STRONGLY_NOT_TAKEN
};
typedef enum predictionValues prediction_t;

struct bPredTableEntry
{
	unsigned long branchInstAdd;
	prediction_t prediction;
	struct bPredTableEntry *next;
	struct bPredTableEntry *prev;
};
typedef struct bPredTableEntry bPredTableEntry_t;

bPredTableEntry_t *bPredTable_head;
bPredTableEntry_t *bPredTable_tail;
unsigned int bPredTableEntries;

unsigned int prevBlockValid;
unsigned long prevBlockEndAdd;

void insertEntryToTail(bPredTableEntry_t *entry)
{
//	printf("***************** Inserting Entry! 0x%lx\n\n", entry->branchInstAdd);

	if (bPredTableEntries == BPRED_TABLE_MAX_ENTRIES)
	{
		// Table Capacity full, must remove least recently used to make space
		bPredTableEntry_t *tmp;
		tmp = bPredTable_head;
		bPredTable_head = bPredTable_head->next;
		bPredTable_head->prev = NULL;
		bPredTableEntries--;
		free(tmp);
	}

	if (bPredTable_head == NULL &&
			bPredTable_tail == NULL)
	{
		entry->next = NULL;
		entry->prev = NULL;
		bPredTable_head = entry;
		bPredTable_tail = entry;
		bPredTableEntries++;
		return;
	}
	else
	{
		bPredTable_tail->next = entry;
		entry->prev = bPredTable_tail;
		entry->next = NULL;
		bPredTable_tail = entry;
		bPredTableEntries++;
		return;
	}
}

void moveEntryToTail(bPredTableEntry_t *entry)
{
	if (entry->next == NULL)
		return; // already at tail
	else if (entry->prev == NULL) {
		// Entry is head
		bPredTable_head = entry->next;
		bPredTable_head->prev = NULL;
		bPredTable_tail->next = entry;
		entry->prev = bPredTable_tail;
		entry->next = NULL;
		bPredTable_tail = entry;
		return;
	}
	else
	{
		entry->prev->next = entry->next;
		entry->next->prev = entry->prev;
		bPredTable_tail->next = entry;
		entry->prev = bPredTable_tail;
		entry->next = NULL;
		bPredTable_tail = entry;
		return;
	}
}

/**
 * Called when a new branch is entered.
 *
 * name: string containing name of the basic block.
 * blockObjStartAdd : Starting address of basic block from objdump
 * blockObjEndAdd : End address of basic block from objdump
 *
 * returns whether branch was predicted or not
 */
unsigned int enterBlock (unsigned long blockObjStartAdd,
		unsigned long blockObjEndAdd)
{
	int isBranchTaken;
	int predicted = -1;

	if (!prevBlockValid)
	{
		// No Previous block, so branch not predicted!
		// Set current block as previous
		prevBlockValid = 1;
		prevBlockEndAdd = blockObjEndAdd;
		predicted =  0;
	}

#define ADDRESS_IS_LINE_NUMBER
#ifdef ADDRESS_IS_LINE_NUMBER
	if (blockObjStartAdd == prevBlockEndAdd + 1)
#else
	if (blockObjStartAdd == prevBlockEndAdd + 4)
#endif
	{
		// Branch was not taken!
		isBranchTaken = 0;
	}
	else
	{
		// Branch was taken!
		isBranchTaken = 1;
	}

	bPredTableEntry_t *entry = bPredTable_tail;
	while(entry != NULL)
	{
		if (entry->branchInstAdd == prevBlockEndAdd)
		{
//			printf ("Entry Found!\n");
			// Entry Found!
			if (entry->prediction == STRONGLY_NOT_TAKEN)
			{
				if (isBranchTaken)
				{
					entry->prediction = WEAKLY_NOT_TAKEN;
					predicted =  0; // not predicted
					break;
				}
				else
				{
					predicted =  1; // predicted
					break;
				}
			}
			if (entry->prediction == WEAKLY_NOT_TAKEN)
			{
				if (isBranchTaken)
				{
					entry->prediction = WEAKLY_TAKEN;
					predicted =  0; // not predicted
					break;
				}
				else
				{
					entry->prediction = STRONGLY_NOT_TAKEN;
					predicted =  1; // predicted
					break;
				}
			}
			if (entry->prediction == WEAKLY_TAKEN)
			{
				if (isBranchTaken)
				{
					entry->prediction = STRONGLY_TAKEN;
					predicted =  1; // predicted
					break;
				}
				else
				{
					entry->prediction = WEAKLY_NOT_TAKEN;
					predicted =  0; // not predicted
					break;
				}
			}
			if (entry->prediction == STRONGLY_TAKEN)
			{
				if (isBranchTaken)
				{
					predicted =  1; // predicted
					break;
				}
				else
				{
					entry->prediction = WEAKLY_TAKEN;
					predicted =  0; // not predicted
					break;
				}
			}
		}
		entry = entry->prev;
	}

	if (entry != NULL)
	{
		// Entry was found!
		moveEntryToTail(entry);
	}
	else
	{
//		printf ("Entry NOT Found! 0x%lx\n", prevBlockEndAdd);
		// Entry was not found!
		entry = malloc(sizeof(bPredTableEntry_t));
		entry->branchInstAdd = prevBlockEndAdd;
		if (isBranchTaken)
		{
			entry->prediction = WEAKLY_NOT_TAKEN;
			predicted = 0;
		}
		else
		{
			entry->prediction = STRONGLY_NOT_TAKEN;
			predicted = 1;
		}
		insertEntryToTail(entry);
	}

	prevBlockEndAdd = blockObjEndAdd;

	if (!predicted)
	{
		printf("Branch NOT Predicted. Start 0x%lx; End 0x%lx\n\n", blockObjStartAdd, blockObjEndAdd);
	}
	else
	{
//		printf(" ****** Predicted. Start 0x%lx; End 0x%lx\n\n", blockObjStartAdd, blockObjEndAdd);
	}

	return predicted;
}

void branchPred_init() {
	bPredTable_head = NULL;
	bPredTable_tail = NULL;
	bPredTableEntries = 0;
	prevBlockValid = 0;
}
