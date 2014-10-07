/***********************************************************
 Intermediate representation of
    test_memory/app_dir/test_memory.c

 Converted by ir2c v0.1

 ***********************************************************/
#include <limits.h>
#include <stdint.h>
#include "ir2c.h"
#include "cacheSim.h"
#include "branchPred.h"
extern unsigned long SP;
extern unsigned long long memAccessCycles;
extern unsigned long long pipelineCycles;



#include <stdio.h>
#include "test_data_8192_32k.h"
#include "test_data_131072_512k.h"


void fill_L1_read_again() {
  long long unsigned int sum_47;
  uintptr_t ivtmp_43;
  uintptr_t ivtmp_34;
  long long unsigned int sum;

fill_L1_read_againbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
SP = SP + 0x8;
memAccessCycles += simDCache(0x34c, 1);  // PC Relative Load
// Simulating I Cache for obj block 0
memAccessCycles += simICache(0x2d0, 24);
pipelineCycles += 14 - (enterBlock(0xd0, 0xd5) ? 7 : 0);
  ivtmp_43 = 0;
  sum = 0;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

fill_L1_read_againbb_3:
//  # PRED: 3 [99.0%]  (true,exec) 2 [100.0%]  (fallthru,exec)
memAccessCycles += simDCache(data_8192_addr + (+ivtmp_43), 1);
// Simulating I Cache for obj block 1
memAccessCycles += simICache(0x2e8, 24);
pipelineCycles += 12 - (enterBlock(0xd6, 0xdb) ? 7 : 0);
  sum = sum + (long long unsigned int) *(unsigned int*)((uintptr_t)&data_8192 + (uintptr_t)ivtmp_43);
  ivtmp_43 = ivtmp_43 + 4;
  if (ivtmp_43 != 32768)
    goto fill_L1_read_againbb_3;
  else
    goto fill_L1_read_againbb_4;
//  # SUCC: 3 [99.0%]  (true,exec) 4 [1.0%]  (false,exec)

fill_L1_read_againbb_4:
//  # PRED: 3 [1.0%]  (false,exec)
memAccessCycles += simDCache(0x350, 1);  // PC Relative Load
memAccessCycles += simDCache(0x34c, 1);  // PC Relative Load
// Simulating I Cache for obj block 2
memAccessCycles += simICache(0x300, 36);
pipelineCycles += 15 - (enterBlock(0xdc, 0xe4) ? 7 : 0);
  printf (&"fill_L1_DCache : Sum (8192) = %llu\n"[0], sum);
  ivtmp_34 = 0;
  sum_47 = 0;
//  # SUCC: 5 [100.0%]  (fallthru,exec)

fill_L1_read_againbb_5:
//  # PRED: 5 [99.0%]  (true,exec) 4 [100.0%]  (fallthru,exec)
memAccessCycles += simDCache(data_8192_addr + (+ivtmp_34), 1);
// Simulating I Cache for obj block 3
memAccessCycles += simICache(0x324, 24);
pipelineCycles += 13 - (enterBlock(0xe5, 0xea) ? 7 : 0);
  sum_47 = sum_47 + (long long unsigned int) *(unsigned int*)((uintptr_t)&data_8192 + (uintptr_t)ivtmp_34);
  ivtmp_34 = ivtmp_34 + 4;
  if (ivtmp_34 != 32772)
    goto fill_L1_read_againbb_5;
  else
    goto fill_L1_read_againbb_6;
//  # SUCC: 5 [99.0%]  (true,exec) 6 [1.0%]  (false,exec)

fill_L1_read_againbb_6:
//  # PRED: 5 [1.0%]  (false,exec)
memAccessCycles += simDCache(0x350, 1);  // PC Relative Load
// Simulating I Cache for obj block 4
memAccessCycles += simICache(0x33c, 16);
pipelineCycles += 10 - (enterBlock(0xeb, 0xee) ? 7 : 0);
  printf (&"fill_L1_DCache : Sum (8192) = %llu\n"[0], sum_47);
  return;
//  # SUCC: EXIT [100.0%] 

}



void fill_L2_Cache() {
  uintptr_t ivtmp_77;
  long long unsigned int sum;

fill_L2_Cachebb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
SP = SP + 0x8;
memAccessCycles += simDCache(0x2c8, 1);  // PC Relative Load
// Simulating I Cache for obj block 0
memAccessCycles += simICache(0x28c, 20);
pipelineCycles += 13 - (enterBlock(0xbd, 0xc1) ? 7 : 0);
  ivtmp_77 = 0;
  sum = 0;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

fill_L2_Cachebb_3:
//  # PRED: 3 [99.0%]  (true,exec) 2 [100.0%]  (fallthru,exec)
memAccessCycles += simDCache(data_131072_addr + (+ivtmp_77), 1);
// Simulating I Cache for obj block 1
memAccessCycles += simICache(0x2a0, 24);
pipelineCycles += 12 - (enterBlock(0xc2, 0xc7) ? 7 : 0);
  sum = sum + (long long unsigned int) *(unsigned int*)((uintptr_t)&data_131072 + (uintptr_t)ivtmp_77);
  ivtmp_77 = ivtmp_77 + 4;
  if (ivtmp_77 != 524288)
    goto fill_L2_Cachebb_3;
  else
    goto fill_L2_Cachebb_4;
//  # SUCC: 3 [99.0%]  (true,exec) 4 [1.0%]  (false,exec)

fill_L2_Cachebb_4:
//  # PRED: 3 [1.0%]  (false,exec)
memAccessCycles += simDCache(0x2cc, 1);  // PC Relative Load
// Simulating I Cache for obj block 2
memAccessCycles += simICache(0x2b8, 16);
pipelineCycles += 10 - (enterBlock(0xc8, 0xcb) ? 7 : 0);
  printf (&"fill_L1_DCache : Sum (131072) = %llu\n"[0], sum);
  return;
//  # SUCC: EXIT [100.0%] 

}



void fill_L1_DCache() {
  uintptr_t ivtmp_108;
  long long unsigned int sum;

fill_L1_DCachebb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
SP = SP + 0x8;
memAccessCycles += simDCache(0x284, 1);  // PC Relative Load
// Simulating I Cache for obj block 0
memAccessCycles += simICache(0x244, 24);
pipelineCycles += 14 - (enterBlock(0xa9, 0xae) ? 7 : 0);
  ivtmp_108 = 0;
  sum = 0;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

fill_L1_DCachebb_3:
//  # PRED: 3 [99.0%]  (true,exec) 2 [100.0%]  (fallthru,exec)
memAccessCycles += simDCache(data_8192_addr + (+ivtmp_108), 1);
// Simulating I Cache for obj block 1
memAccessCycles += simICache(0x25c, 24);
pipelineCycles += 12 - (enterBlock(0xaf, 0xb4) ? 7 : 0);
  sum = sum + (long long unsigned int) *(unsigned int*)((uintptr_t)&data_8192 + (uintptr_t)ivtmp_108);
  ivtmp_108 = ivtmp_108 + 4;
  if (ivtmp_108 != 32768)
    goto fill_L1_DCachebb_3;
  else
    goto fill_L1_DCachebb_4;
//  # SUCC: 3 [99.0%]  (true,exec) 4 [1.0%]  (false,exec)

fill_L1_DCachebb_4:
//  # PRED: 3 [1.0%]  (false,exec)
memAccessCycles += simDCache(0x288, 1);  // PC Relative Load
// Simulating I Cache for obj block 2
memAccessCycles += simICache(0x274, 16);
pipelineCycles += 10 - (enterBlock(0xb5, 0xb8) ? 7 : 0);
  printf (&"fill_L1_DCache : Sum (8192) = %llu\n"[0], sum);
  return;
//  # SUCC: EXIT [100.0%] 

}



void half_fill_L1_DCache() {
  uintptr_t ivtmp_139;
  long long unsigned int sum;

half_fill_L1_DCachebb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
SP = SP + 0x8;
// Simulating I Cache for obj block 0
memAccessCycles += simICache(0x200, 20);
pipelineCycles += 13 - (enterBlock(0x96, 0x9a) ? 7 : 0);
  ivtmp_139 = 0;
  sum = 0;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

half_fill_L1_DCachebb_3:
//  # PRED: 3 [99.0%]  (true,exec) 2 [100.0%]  (fallthru,exec)
// Simulating I Cache for obj block 1
memAccessCycles += simICache(0x214, 24);
pipelineCycles += 12 - (enterBlock(0x9b, 0xa0) ? 7 : 0);
  sum = sum + (long long unsigned int) *(unsigned int*)((uintptr_t)&data_131072 + (uintptr_t)ivtmp_139);
  ivtmp_139 = ivtmp_139 + 4;
  if (ivtmp_139 != 16384)
    goto half_fill_L1_DCachebb_3;
  else
    goto half_fill_L1_DCachebb_4;
//  # SUCC: 3 [99.0%]  (true,exec) 4 [1.0%]  (false,exec)

half_fill_L1_DCachebb_4:
//  # PRED: 3 [1.0%]  (false,exec)
// Simulating I Cache for obj block 2
memAccessCycles += simICache(0x22c, 16);
pipelineCycles += 10 - (enterBlock(0xa1, 0xa4) ? 7 : 0);
  printf (&"fill_L1_DCache : Sum (8192) = %llu\n"[0], sum);
  return;
//  # SUCC: EXIT [100.0%] 

}


