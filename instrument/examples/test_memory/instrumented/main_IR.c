/***********************************************************
 Intermediate representation of
    test_memory/app_dir/main.c

 Converted by ir2c v0.1

 ***********************************************************/
#include <limits.h>
#include <stdint.h>
#include "ir2c.h"
#include "cacheSim.h"
#include "branchPred.h"
unsigned long SP = 0x1234;
unsigned long long memAccessCycles = 0;
unsigned long long pipelineCycles = 0;

#include "test_memory.h"


int main() {
mainbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
cacheSimInit();
branchPred_init();
SP = SP + 0x8;
// Simulating I Cache for obj block 0
memAccessCycles += simICache(0x3cc, 28);
pipelineCycles += 12 - (enterBlock(0x111, 0x117) ? 7 : 0);
  fill_L1_DCache ();
//  fill_L2_Cache ();
//  fill_L1_read_again ();
  printf("memAccessCycles = \%llu\n", memAccessCycles);
  printf("pipelineCycles = \%llu\n", pipelineCycles);
  cacheSimFini();
  return 0;
//  # SUCC: EXIT [100.0%] 

}


