/***********************************************************
 Intermediate representation of
    adpcm/app_dir/my_ctop.c

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

/*
** Timing - Test timing on adpcm coder and decoder.
**
** The program creates 10Kb garbage, and runs the compressor and
** the decompressor on it.
*/

/*sds*/

#include <stdio.h>
#include "adpcm.h"
#include "in_small.h"
//#include "in_large.h"
#include "my_variables.h"
#define DATASIZE 10*1024	/* Data block size */
//ARR_SIZE is the number of short type elements in 
//input data array. defined in in_data_small.h
//unsigned int ARR_SIZE = 13305601;
//unsigned int ARR_SIZE = 684433;
short int pcmdata[DATASIZE];
unsigned long pcmdata_addr = 0x14f208;
char adpcmdata[DATASIZE/2];
unsigned long adpcmdata_addr = 0x154208;

int a[123];

struct adpcm_state coder_1_state;
unsigned long coder_1_state_addr = 0x14f204;


int main() {
  long unsigned int end_46;
  int i_45;
  long unsigned int end_44;
  long unsigned int end_43;
  long unsigned int start_40;
  uintptr_t ivtmp_34;
  int D_2229;
  uintptr_t ivtmp_28;
  long unsigned int count;
  long unsigned int end;
  long unsigned int start;
  long unsigned int j;
  int i;
  unsigned int ARR_SIZE_0;
  unsigned long ARR_SIZE_0_addr = 0x0;

  unsigned long ivtmp_34_addr = 0; // MANUAL
  unsigned long ivtmp_28_addr = 0; //MANUAL

mainbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
cacheSimInit();
branchPred_init();
SP = SP + 0x30;
memAccessCycles += simDCache(0x354, 1);  // PC Relative Load
memAccessCycles += simDCache(0x358, 1);  // PC Relative Load
memAccessCycles += simDCache(ARR_SIZE_addr, 1);
memAccessCycles += simDCache((SP + ARR_SIZE_0_addr), 0);
// Simulating I Cache for obj block 0
memAccessCycles += simICache(0x200, 36);
pipelineCycles += 27 - (enterBlock(0x96, 0x9e) ? 7 : 0);
  ARR_SIZE_0 = ARR_SIZE;
  j = ARR_SIZE_0 / 10240;
  if (j != 0)
    goto mainbb_14;
  else
    goto mainbb_7;
//  # SUCC: 14 [91.0%]  (true,exec) 7 [9.0%]  (false,exec)

mainbb_14:
//  # PRED: 2 [91.0%]  (true,exec)
memAccessCycles += simDCache(0x35c, 1);  // PC Relative Load
memAccessCycles += simDCache((SP + 0x4), 1);  // Spilling Register
memAccessCycles += simDCache(0x360, 1);  // PC Relative Load
memAccessCycles += simDCache(0x364, 1);  // PC Relative Load
memAccessCycles += simDCache(0x368, 1);  // PC Relative Load
// Simulating I Cache for obj block 1
memAccessCycles += simICache(0x224, 40);
pipelineCycles += 21 - (enterBlock(0x9f, 0xa8) ? 7 : 0);
  end_43 = 0;
  count = 0;
//  # SUCC: 3 [100.0%]  (fallthru)

mainbb_3:
//  # PRED: 13 [100.0%]  (fallthru) 14 [100.0%]  (fallthru)
pipelineCycles += 9 - (enterBlock(0xa9, 0xab) ? 7 : 0);
  end_46 = end_43 + 10240;
  if (end_43 < end_46)
    goto mainbb_4;
  else
    goto mainbb_6;
//  # SUCC: 4 [99.0%]  (true,exec) 6 [1.0%]  (false,exec)

mainbb_4:
//  # PRED: 3 [99.0%]  (true,exec)
memAccessCycles += simDCache((SP + 0x4), 1);  // Reading Spilt Register
// Simulating I Cache for obj block 3
memAccessCycles += simICache(0x258, 20);
pipelineCycles += 13 - (enterBlock(0xac, 0xb0) ? 7 : 0);
  i_45 = (int) end_43;
  ivtmp_34 = (uintptr_t)&in_Data[i_45];
  ivtmp_34_addr = in_Data_addr + (2 * i_45);
  end_44 = end_43;
//  # SUCC: 5 [100.0%]  (fallthru,exec)

mainbb_5:
//  # PRED: 5 [99.0%]  (true,exec) 4 [100.0%]  (fallthru,exec)
memAccessCycles += simDCache(pcmdata_addr + (2 * (end_44-end_43)), 0);
// Simulating I Cache for obj block 4
memAccessCycles += simICache(0x26c, 36);
// TODO: UnmappedLS: Load GlobalVar in_Data at line 179
pipelineCycles += 16 - (enterBlock(0xb1, 0xb9) ? 7 : 0);
  pcmdata[end_44 - end_43] = *(short int*)((uintptr_t)ivtmp_34);
//Manual Annotation
  memAccessCycles += simDCache(ivtmp_34_addr, 1);
  i_45 = i_45 + 1;
  end_44 = (long unsigned int) i_45;
  ivtmp_34 = ivtmp_34 + 2;
  ivtmp_34_addr = ivtmp_34_addr + 2;
  if (end_44 < end_46)
    goto mainbb_5;
  else
    goto mainbb_6;
//  # SUCC: 5 [99.0%]  (true,exec) 6 [1.0%]  (false,exec)

mainbb_6:
//  # PRED: 5 [1.0%]  (false,exec) 3 [1.0%]  (false,exec)
// Simulating I Cache for obj block 5
memAccessCycles += simICache(0x290, 40);
pipelineCycles += 14 - (enterBlock(0xba, 0xc3) ? 7 : 0);
  adpcm_coder (&pcmdata, pcmdata_addr,  &adpcmdata, adpcmdata_addr,  10240,  &coder_1_state, coder_1_state_addr);
  count = count + 1;
  if (j > count)
    goto mainbb_13;
  else
    goto mainbb_7;
//  # SUCC: 13 [91.0%]  (true,exec) 7 [9.0%]  (false,exec)

mainbb_13:
//  # PRED: 6 [91.0%]  (true,exec)
// Simulating I Cache for obj block 2
memAccessCycles += simICache(0x24c, 12);
  end_43 = end_46;
  goto mainbb_3;
//  # SUCC: 3 [100.0%]  (fallthru)

mainbb_7:
//  # PRED: 6 [9.0%]  (false,exec) 2 [9.0%]  (false,exec)
memAccessCycles += simDCache(0x358, 1);  // PC Relative Load
memAccessCycles += simDCache((SP + ARR_SIZE_0_addr), 1);
// Simulating I Cache for obj block 6
memAccessCycles += simICache(0x2b8, 32);
pipelineCycles += 19 - (enterBlock(0xc4, 0xcb) ? 7 : 0);
  if (ARR_SIZE_0 % 10240 != 0)
    goto mainbb_8;
  else
    goto mainbb_12;
//  # SUCC: 8 [61.0%]  (true,exec) 12 [39.0%]  (false,exec)

mainbb_8:
//  # PRED: 7 [61.0%]  (true,exec)
memAccessCycles += simDCache(0x354, 1);  // PC Relative Load
// Simulating I Cache for obj block 7
memAccessCycles += simICache(0x2d8, 24);
pipelineCycles += 14 - (enterBlock(0xcc, 0xd1) ? 7 : 0);
  start_40 = j * 10240;
  memAccessCycles += simDCache(ARR_SIZE_addr, 1);
  end = ARR_SIZE;
  if (start_40 < end)
    goto mainbb_9;
  else
    goto mainbb_11;
//  # SUCC: 9 [99.0%]  (true,exec) 11 [1.0%]  (false,exec)

mainbb_9:
//  # PRED: 8 [99.0%]  (true,exec)
memAccessCycles += simDCache(0x35c, 1);  // PC Relative Load
memAccessCycles += simDCache(0x360, 1);  // PC Relative Load
// Simulating I Cache for obj block 8
memAccessCycles += simICache(0x2f0, 28);
pipelineCycles += 13 - (enterBlock(0xd2, 0xd8) ? 7 : 0);
  i = (int) start_40;
  ivtmp_28 = (uintptr_t)&in_Data[i];
  ivtmp_28_addr = in_Data_addr + (2 * i);
  D_2229 = (int) end;
  start = start_40;
//  # SUCC: 10 [100.0%]  (fallthru,exec)

mainbb_10:
//  # PRED: 10 [99.0%]  (true,exec) 9 [100.0%]  (fallthru,exec)
memAccessCycles += simDCache(pcmdata_addr + (2 * (start-start_40)), 0);
// Simulating I Cache for obj block 9
memAccessCycles += simICache(0x30c, 36);
// TODO: UnmappedLS: Inaccurately Matched Load at line 219
pipelineCycles += 16 - (enterBlock(0xd9, 0xe1) ? 7 : 0);
  pcmdata[start - start_40] = *(short int*)((uintptr_t)ivtmp_28);
  memAccessCycles += simDCache(ivtmp_28_addr, 1);
  i = i + 1;
  start = (long unsigned int) i;
  ivtmp_28 = ivtmp_28 + 2;
  ivtmp_28_addr = ivtmp_28_addr + 2;
  if (i != D_2229)
    goto mainbb_10;
  else
    goto mainbb_11;
//  # SUCC: 10 [99.0%]  (true,exec) 11 [1.0%]  (false,exec)

mainbb_11:
//  # PRED: 10 [1.0%]  (false,exec) 8 [1.0%]  (false,exec)
memAccessCycles += simDCache(0x360, 1);  // PC Relative Load
memAccessCycles += simDCache(0x364, 1);  // PC Relative Load
memAccessCycles += simDCache(0x368, 1);  // PC Relative Load
// Simulating I Cache for obj block 10
memAccessCycles += simICache(0x330, 20);
pipelineCycles += 11 - (enterBlock(0xe2, 0xe6) ? 7 : 0);
  adpcm_coder (&pcmdata, pcmdata_addr,  &adpcmdata, adpcmdata_addr,  (int) (end - start_40),  &coder_1_state, coder_1_state_addr);
//  # SUCC: 12 [100.0%]  (fallthru,exec)

mainbb_12:
//  # PRED: 7 [39.0%]  (false,exec) 11 [100.0%]  (fallthru,exec)
// Simulating I Cache for obj block 11
memAccessCycles += simICache(0x344, 16);
printf("memAccessCycles = \%llu\n", memAccessCycles);
printf("pipelineCycles = \%llu\n", pipelineCycles);
cacheSimFini();
pipelineCycles += 18 - (enterBlock(0xe7, 0xea) ? 7 : 0);
  return 0;
//  # SUCC: EXIT [100.0%] 

}


