/***********************************************************
 Intermediate representation of
    basicmath/app_dir/basicmath_small_truncated3.c

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

//23 Oct 2012 - Truncated the 4 nested loop counts (calling SolveCubic). Total iterations
//              reduced to 960 from 18000 in this nest of 4 loops.
// last week of Oct 2012 - Truncated even more, down to 96 iterations in the
//                         4 nested for-loops and 51 in the usqrt loops

#include "snipmath.h"
#include <math.h>

/* The printf's may be removed to isolate just the math calculations */

double Xangle[2];
unsigned long Xangle_addr = 0x37e0;


int  main (void) {
  double X_62;
  uintptr_t ivtmp_58;
  uintptr_t ivtmp_54;
  uintptr_t ivtmp_50;
  uintptr_t ivtmp_46;
  uintptr_t ivtmp_37;
  uintptr_t ivtmp_32;
  double Xangle_I_lsm_24;
  double Xangle_I_lsm_23;
  struct int_sqrt q;
  int i;
  int solutions;
  double X;
  double x[3];
  double d1;
  double c1;
  double b1;
  double a1;

mainbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
cacheSimInit();
branchPred_init();
SP = SP + 0x90;
memAccessCycles += simDCache((SP + 0x8), 1);  // Spilling Register
memAccessCycles += simDCache((SP + 0xc), 1);  // Spilling Register
memAccessCycles += simDCache((SP + 0x10), 1);  // Spilling Register
memAccessCycles += simDCache((SP + 0x14), 1);  // Spilling Register
memAccessCycles += simDCache((SP + 0x3c), 1);  // Spilling Register
memAccessCycles += simDCache((SP + 0x28), 1);  // Spilling Register
memAccessCycles += simDCache((SP + 0x2c), 1);  // Spilling Register
// Simulating I Cache for obj block 0
memAccessCycles += simICache(0x200, 320);
pipelineCycles += 90 - (enterBlock(0x96, 0xe5) ? 7 : 0);
  SolveCubic (1.0e+0, -1.05e+1, 3.2e+1, -3.0e+1, &solutions, &x);
  SolveCubic (1.0e+0, -4.5e+0, 1.7e+1, -3.0e+1, &solutions, &x);
  SolveCubic (1.0e+0, -3.5e+0, 2.2e+1, -3.1e+1, &solutions, &x);
  SolveCubic (1.0e+0, -1.36999999999999992894572642398998141288757324219e+1, 1.0e+0, -3.5e+1, &solutions, &x);
  ivtmp_58 = 0;
  a1 = 3.0e+0;
  goto mainbb_9;
//  # SUCC: 9 [100.0%]  (fallthru,exec)

mainbb_3:
//  # PRED: 3 [91.0%]  (true,exec) 5 [100.0%]  (fallthru,exec)
memAccessCycles += simDCache((SP + 0x8), 1);  // Spilling Register
memAccessCycles += simDCache((SP + 0xc), 1);  // Spilling Register
memAccessCycles += simDCache((SP + 0x10), 1);  // Spilling Register
memAccessCycles += simDCache((SP + 0x14), 1);  // Spilling Register
// Simulating I Cache for obj block 1
memAccessCycles += simICache(0x340, 88);
pipelineCycles += 25 - (enterBlock(0xe6, 0xfb) ? 7 : 0);
  SolveCubic (a1, b1, c1, d1, &solutions, &x);
  d1 = d1 - 1.0e+0;
  ivtmp_46 = ivtmp_46 + 1;
  if (ivtmp_46 != 4)
    goto mainbb_3;
  else
    goto mainbb_4;
//  # SUCC: 3 [91.0%]  (true,exec) 4 [9.0%]  (false,exec)

mainbb_4:
//  # PRED: 3 [9.0%]  (false,exec)
// Simulating I Cache for obj block 2
memAccessCycles += simICache(0x398, 12);
pipelineCycles += 8 - (enterBlock(0xfc, 0xfe) ? 7 : 0);
  c1 = c1 + 5.0e-1;
  ivtmp_50 = ivtmp_50 + 1;
  if (ivtmp_50 != 4)
    goto mainbb_5;
  else
    goto mainbb_6;
//  # SUCC: 5 [91.0%]  (true,exec) 6 [9.0%]  (false,exec)

mainbb_5:
//  # PRED: 4 [91.0%]  (true,exec) 7 [100.0%]  (fallthru,exec)
memAccessCycles += simDCache((SP + 0x18), 1);  // Spilling Register
memAccessCycles += simDCache((SP + 0x1c), 1);  // Spilling Register
// Simulating I Cache for obj block 3
memAccessCycles += simICache(0x3a4, 32);
// Simulating I Cache for obj block 4
memAccessCycles += simICache(0x3c4, 20);
pipelineCycles += 14 - (enterBlock(0xff, 0x106) ? 7 : 0);
pipelineCycles += 11 - (enterBlock(0x107, 0x10b) ? 7 : 0);
  ivtmp_46 = 0;
  d1 = -1.0e+0;
  goto mainbb_3;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

mainbb_6:
//  # PRED: 4 [9.0%]  (false,exec)
// Simulating I Cache for obj block 5
memAccessCycles += simICache(0x3d8, 12);
pipelineCycles += 8 - (enterBlock(0x10c, 0x10e) ? 7 : 0);
  b1 = b1 - 1.0e+0;
  ivtmp_54 = ivtmp_54 + 1;
  if (ivtmp_54 != 2)
    goto mainbb_7;
  else
    goto mainbb_8;
//  # SUCC: 7 [91.0%]  (true,exec) 8 [9.0%]  (false,exec)

mainbb_7:
//  # PRED: 6 [91.0%]  (true,exec) 9 [100.0%]  (fallthru,exec)
memAccessCycles += simDCache((SP + 0x20), 1);  // Spilling Register
memAccessCycles += simDCache((SP + 0x24), 1);  // Spilling Register
// Simulating I Cache for obj block 6
memAccessCycles += simICache(0x3e4, 32);
memAccessCycles += simDCache((SP + 0x18), 1);  // Spilling Register
memAccessCycles += simDCache((SP + 0x1c), 1);  // Spilling Register
// Simulating I Cache for obj block 7
memAccessCycles += simICache(0x404, 28);
pipelineCycles += 14 - (enterBlock(0x10f, 0x116) ? 7 : 0);
pipelineCycles += 13 - (enterBlock(0x117, 0x11d) ? 7 : 0);
  ivtmp_50 = 0;
  c1 = 5.0e+0;
  goto mainbb_5;
//  # SUCC: 5 [100.0%]  (fallthru,exec)

mainbb_8:
//  # PRED: 6 [9.0%]  (false,exec)
memAccessCycles += simDCache((SP + 0x3c), 1);  // Reading Spilt Register
memAccessCycles += simDCache((SP + 0x3c), 1);  // Spilling Register
// Simulating I Cache for obj block 8
memAccessCycles += simICache(0x420, 20);
pipelineCycles += 10 - (enterBlock(0x11e, 0x122) ? 7 : 0);
  a1 = a1 + 1.0e+0;
  ivtmp_58 = ivtmp_58 + 1;
  if (ivtmp_58 != 3)
    goto mainbb_9;
  else
    goto mainbb_16;
//  # SUCC: 9 [75.0%]  (true,exec) 16 [25.0%]  (false,exec)

mainbb_9:
//  # PRED: 8 [75.0%]  (true,exec) 2 [100.0%]  (fallthru,exec)
memAccessCycles += simDCache((SP + 0x28), 1);  // Spilling Register
memAccessCycles += simDCache((SP + 0x2c), 1);  // Spilling Register
// Simulating I Cache for obj block 9
memAccessCycles += simICache(0x434, 32);
memAccessCycles += simDCache((SP + 0x20), 1);  // Spilling Register
memAccessCycles += simDCache((SP + 0x24), 1);  // Spilling Register
memAccessCycles += simDCache((SP + 0x30), 1);  // Spilling Register
memAccessCycles += simDCache((SP + 0x34), 1);  // Spilling Register
// Simulating I Cache for obj block 10
memAccessCycles += simICache(0x454, 48);
pipelineCycles += 14 - (enterBlock(0x123, 0x12a) ? 7 : 0);
pipelineCycles += 18 - (enterBlock(0x12b, 0x136) ? 7 : 0);
  ivtmp_54 = 0;
  b1 = 1.0e+1;
  goto mainbb_7;
//  # SUCC: 7 [100.0%]  (fallthru,exec)

mainbb_16:
//  # PRED: 8 [25.0%]  (false,exec)
// Simulating I Cache for obj block 11
memAccessCycles += simICache(0x484, 8);
pipelineCycles += 9 - (enterBlock(0x137, 0x138) ? 7 : 0);
  i = 0;
//  # SUCC: 10 [100.0%]  (fallthru)

mainbb_10:
//  # PRED: 10 [98.1%]  (true,exec) 16 [100.0%]  (fallthru)
// Simulating I Cache for obj block 12
memAccessCycles += simICache(0x48c, 24);
pipelineCycles += 10 - (enterBlock(0x139, 0x13e) ? 7 : 0);
  usqrt ((long unsigned int) i,  &q, q_addr);
  i = i + 1;
  if (i != 51)
    goto mainbb_10;
  else
    goto mainbb_11;
//  # SUCC: 10 [98.1%]  (true,exec) 11 [1.9%]  (false,exec)

mainbb_11:
//  # PRED: 10 [1.9%]  (false,exec)
// Simulating I Cache for obj block 13
memAccessCycles += simICache(0x4a4, 64);
pipelineCycles += 22 - (enterBlock(0x13f, 0x14e) ? 7 : 0);
//Invalid sum of outgoing probabilities 0.0%
  usqrt (1072497001,  &q, q_addr);
  ivtmp_37 = 0;
  X = 0.0;
//  # SUCC: 12 (fallthru,exec)

mainbb_12:
//  # PRED: 12 [99.0%]  (true,exec) 11 (fallthru,exec)
memAccessCycles += simDCache((SP + 0x18), 1);  // Spilling Register
memAccessCycles += simDCache((SP + 0x1c), 1);  // Spilling Register
// Simulating I Cache for obj block 14
memAccessCycles += simICache(0x4e4, 84);
pipelineCycles += 24 - (enterBlock(0x14f, 0x163) ? 7 : 0);
  Xangle_I_lsm_24 = (X * 3.14159265358979311599796346854418516159057617188e+0) / 1.8e+2;
  X = X + 1.0e+0;
  ivtmp_37 = ivtmp_37 + 1;
  if (ivtmp_37 != 361)
    goto mainbb_12;
  else
    goto mainbb_13;
//  # SUCC: 12 [99.0%]  (true,exec) 13 [1.0%]  (false,exec)

mainbb_13:
//  # PRED: 12 [1.0%]  (false,exec)
memAccessCycles += simDCache(0x600, 1);  // PC Relative Load
// Simulating I Cache for obj block 15
memAccessCycles += simICache(0x538, 60);
pipelineCycles += 22 - (enterBlock(0x164, 0x172) ? 7 : 0);
//Invalid sum of outgoing probabilities 0.0%
  Xangle[0] = Xangle_I_lsm_24;
  ivtmp_32 = 0;
  X_62 = 0.0;
//  # SUCC: 14 (fallthru,exec)

mainbb_14:
//  # PRED: 14 [91.0%]  (true,exec) 13 (fallthru,exec)
memAccessCycles += simDCache((SP + 0x18), 1);  // Spilling Register
memAccessCycles += simDCache((SP + 0x1c), 1);  // Spilling Register
// Simulating I Cache for obj block 16
memAccessCycles += simICache(0x574, 80);
pipelineCycles += 23 - (enterBlock(0x173, 0x186) ? 7 : 0);
  Xangle_I_lsm_23 = (X_62 * 1.8e+2) / 3.14159265358979311599796346854418516159057617188e+0;
  X_62 = X_62 + 1.74532925199432954743716805978692718781530857086e-2;
  ivtmp_32 = ivtmp_32 + 1;
  if (ivtmp_32 != 361)
    goto mainbb_14;
  else
    goto mainbb_15;
//  # SUCC: 14 [91.0%]  (true,exec) 15 [9.0%]  (false,exec)

mainbb_15:
//  # PRED: 14 [9.0%]  (false,exec)
memAccessCycles += simDCache(0x600, 1);  // PC Relative Load
memAccessCycles += simDCache(Xangle_addr + (8 * (1)), 0);
// Simulating I Cache for obj block 17
memAccessCycles += simICache(0x5c4, 36);
// TODO: UnmappedLS: Store GlobalVar Xangle at line 395
pipelineCycles += 23 - (enterBlock(0x187, 0x18f) ? 7 : 0);
  Xangle[1] = Xangle_I_lsm_23;
  printf("memAccessCycles = \%llu\n", memAccessCycles);
  printf("pipelineCycles = \%llu\n", pipelineCycles);
  cacheSimFini();
  return 0;
//  # SUCC: EXIT [100.0%] 

}


