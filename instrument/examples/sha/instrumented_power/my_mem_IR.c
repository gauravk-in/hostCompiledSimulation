/***********************************************************
 Intermediate representation of
    sha/app_dir/my_mem.c

 Converted by ir2c v0.1

 ***********************************************************/
#include <limits.h>
#include <stdint.h>
#include "ir2c.h"
#include "cacheSim.h"
#include "branchPred.h"
#include "power_estimator.h"
extern unsigned long SP;
extern unsigned long long memAccessCycles;
extern unsigned long long pipelineCycles;
extern struct csim_result_t csim_result;

/*
Author - Suhas Chakravarty
memcpy implementation taken from 
www.danielvik.com/2010/02/fast-memcpy-in-c.html
Renamed to my_memcpy
Created - 17 Nov 2012
Last modified - 17 Nov 2012
*/

#include <stdlib.h>


void* my_memcpy (void*dest, unsigned long dest_addr, const void*src, unsigned long src_addr, size_t count) {
  uintptr_t ivtmp_23;

my_memcpybb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
pipelineCycles += 2;
enterBlock(0x748, 0x74c);
memAccessCycles += simICache(0x748, 8, &csim_result); // GK
SP = SP + 0x0;
  if (count != 0)
    goto my_memcpybb_5;
  else
    goto my_memcpybb_4;
//  # SUCC: 5 [91.0%]  (true,exec) 4 [9.0%]  (false,exec)

my_memcpybb_5:
//  # PRED: 2 [91.0%]  (true,exec)
  ivtmp_23 = 0;
//  # SUCC: 3 [100.0%]  (fallthru)

my_memcpybb_3:
//  # PRED: 3 [91.0%]  (true,exec) 5 [100.0%]  (fallthru)
  pipelineCycles += 17 - (enterBlock(0x750, 0x764) ? 7 : 0);
  memAccessCycles += simICache(0x750, 24, &csim_result); // GK
  memAccessCycles += simDCache(src_addr + ivtmp_23, 1, &csim_result); // GK
  memAccessCycles += simDCache(dest_addr + ivtmp_23, 0, &csim_result); // GK 
  *(char *)((uintptr_t)dest + (uintptr_t)ivtmp_23) = *(char *)((uintptr_t)src + (uintptr_t)ivtmp_23);
  ivtmp_23 = ivtmp_23 + 1;
  if (ivtmp_23 != count)
    goto my_memcpybb_3;
  else
    goto my_memcpybb_4;
//  # SUCC: 3 [91.0%]  (true,exec) 4 [9.0%]  (false,exec)

my_memcpybb_4:
  pipelineCycles += 8 - (enterBlock(0x768, 0x768) ? 7 : 0);
//  # PRED: 3 [9.0%]  (false,exec) 2 [9.0%]  (false,exec)
  return (uintptr_t)dest;
//  # SUCC: EXIT [100.0%] 

}



void* my_memset (void *s, unsigned long s_addr, int c, size_t n) {
  uintptr_t ivtmp_56;

my_memsetbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
pipelineCycles += 2;
enterBlock(0x76c, 0x770);
memAccessCycles += simICache(0x76c, 8, &csim_result);
SP = SP + 0x0;
  if (n != 0)
    goto my_memsetbb_5;
  else
    goto my_memsetbb_4;
//  # SUCC: 5 [91.0%]  (true,exec) 4 [9.0%]  (false,exec)

my_memsetbb_5:
//  # PRED: 2 [91.0%]  (true,exec)
  ivtmp_56 = 0;
//  # SUCC: 3 [100.0%]  (fallthru)

my_memsetbb_3:
//  # PRED: 3 [91.0%]  (true,exec) 5 [100.0%]  (fallthru)
pipelineCycles += 12 - (enterBlock(0x774, 0x784) ? 7 : 0);
memAccessCycles += simICache(0x774, 20, &csim_result);
memAccessCycles += simDCache(s_addr + ivtmp_56, 0, &csim_result);
  *(char *)((uintptr_t)s + (uintptr_t)ivtmp_56) = (char) (char) c;
  ivtmp_56 = ivtmp_56 + 1;
  if (ivtmp_56 != n)
    goto my_memsetbb_3;
  else
    goto my_memsetbb_4;
//  # SUCC: 3 [91.0%]  (true,exec) 4 [9.0%]  (false,exec)

my_memsetbb_4:
//  # PRED: 3 [9.0%]  (false,exec) 2 [9.0%]  (false,exec)
pipelineCycles += 8 - (enterBlock(0x788, 0x788) ? 7 : 0);
  return (uintptr_t)s;
//  # SUCC: EXIT [100.0%] 

}


