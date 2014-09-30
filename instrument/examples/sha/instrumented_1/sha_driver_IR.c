/***********************************************************
 Intermediate representation of
    sha/app_dir/sha_driver.c

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

/* NIST Secure Hash Algorithm */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include "sha.h"
#include "in_small.h"
#include "my_variable.h"
struct SHA_INFO sha_info; //making global
unsigned long sha_info_addr = 0x56770;


int main() {
mainbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
cacheSimInit();
branchPred_init();
SP = SP + 0x8;
memAccessCycles += simDCache(0x224, 1);  // PC Relative Load
memAccessCycles += simDCache(0x228, 1);  // PC Relative Load
memAccessCycles += simDCache(0x22c, 1);  // PC Relative Load
// Simulating I Cache for obj block 0
memAccessCycles += simICache(0x200, 36);
// TODO: UnmappedLS: Load GlobalVar ARR_SIZE at line 154
pipelineCycles += 16 - (enterBlock(0x96, 0x9e) ? 7 : 0);
  sha_stream (&sha_info, sha_info_addr,  &in_Data, in_Data_addr,  ARR_SIZE);
  printf("memAccessCycles = \%llu\n", memAccessCycles);
  printf("pipelineCycles = \%llu\n", pipelineCycles);
  cacheSimFini();
  return 0;
//  # SUCC: EXIT [100.0%] 

}


