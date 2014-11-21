/***********************************************************
 Intermediate representation of
    adpcm/app_dir/adpcm.c

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

/***********************************************************
Copyright 1992 by Stichting Mathematisch Centrum, Amsterdam, The
Netherlands.

                        All Rights Reserved

Permission to use, copy, modify, and distribute this software and its 
documentation for any purpose and without fee is hereby granted, 
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in 
supporting documentation, and that the names of Stichting Mathematisch
Centrum or CWI not be used in advertising or publicity pertaining to
distribution of the software without specific, written prior permission.

STICHTING MATHEMATISCH CENTRUM DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL STICHTING MATHEMATISCH CENTRUM BE LIABLE
FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

******************************************************************/

/*
** Intel/DVI ADPCM coder/decoder.
**
** The algorithm for this coder was taken from the IMA Compatability Project
** proceedings, Vol 2, Number 2; May 1992.
**
** Version 1.2, 18-Dec-92.
**
** Change log:
** - Fixed a stupid bug, where the delta was computed as
**   stepsize*code/4 in stead of stepsize*(code+0.5)/4.
** - There was an off-by-one error causing it to pick
**   an incorrect delta once in a blue moon.
** - The NODIVMUL define has been removed. Computations are now always done
**   using shifts, adds and subtracts. It turned out that, because the standard
**   is defined using shift/add/subtract, you needed bits of fixup code
**   (because the div/mul simulation using shift/add/sub made some rounding
**   errors that real div/mul don't make) and all together the resultant code
**   ran slower than just using the shifts all the time.
** - Changed some of the variable names to be more meaningful.
*/

#include "adpcm.h"
#include <stdio.h> /*DBG*/

#ifndef __STDC__
#define signed
#endif

/* Intel ADPCM step variation table */
static int indexTable[16] = {
    -1, -1, -1, -1, 2, 4, 6, 8,
    -1, -1, -1, -1, 2, 4, 6, 8,
};
unsigned long indexTable_addr = 0x9fc;

static int stepsizeTable[89] = {
    7, 8, 9, 10, 11, 12, 13, 14, 16, 17,
    19, 21, 23, 25, 28, 31, 34, 37, 41, 45,
    50, 55, 60, 66, 73, 80, 88, 97, 107, 118,
    130, 143, 157, 173, 190, 209, 230, 253, 279, 307,
    337, 371, 408, 449, 494, 544, 598, 658, 724, 796,
    876, 963, 1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066,
    2272, 2499, 2749, 3024, 3327, 3660, 4026, 4428, 4871, 5358,
    5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635, 13899,
    15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767
};
unsigned long stepsizeTable_addr = 0x898;


void  adpcm_coder (short indata[], unsigned long indata_addr, char outdata[], unsigned long outdata_addr, int len, struct adpcm_state *state, unsigned long state_addr) {
		
  int valpred_41;
  int index_40;
  int index_38;
  int delta_37;
  int step_36;
  int step_35;
  int valpred_34;
  uintptr_t ivtmp_28;
  int bufferstep;
  int outputbuffer;
  unsigned long outputbuffer_addr = 0x8;
  int index;
  int vpdiff;
  int valpred;
  int step;
  int diff;
  int delta;
  int sign;
  signed char * outp;
  unsigned long outp_addr = 0x0;

adpcm_coderbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
SP = SP + 0x30;
memAccessCycles += simDCache((SP + 0x4), 1, &csim_result);  // Spilling Register
memAccessCycles += simDCache((SP + 0xc), 1, &csim_result);  // Spilling Register
memAccessCycles += simDCache((SP + 0xc), 1, &csim_result);  // Reading Spilt Register
memAccessCycles += simICache(0x4a8, 1, &csim_result);  // PC Relative Load
// Simulating I Cache for obj block 0
memAccessCycles += simICache(0x36c, 44, &csim_result);
estimate_power("adpcm_coderbb_2", pipelineCycles, memAccessCycles, csim_result.L2Hits, (csim_result.prefetches + csim_result.L2Misses));
// TODO: UnmappedLS: Load GlobalVar coder_1_state at line 247
// TODO: UnmappedLS: Load GlobalVar coder_1_state at line 249
pipelineCycles += 23 - (enterBlock(0xf3, 0xfd) ? 7 : 0);
  valpred = state->valprev;
  memAccessCycles += simDCache(state_addr, 1, &csim_result);
  index = state->index;
  memAccessCycles += simDCache(state_addr, 1, &csim_result);
  memAccessCycles += simDCache(stepsizeTable_addr + (4 * (index)), 1, &csim_result);
  step = stepsizeTable[index];
  if (len > 0)
    goto adpcm_coderbb_3;
  else
    goto adpcm_coderbb_21;
//  # SUCC: 3 [91.0%]  (true,exec) 21 [9.0%]  (false,exec)

adpcm_coderbb_3:
//  # PRED: 2 [91.0%]  (true,exec)
memAccessCycles += simICache(0x4a8, 1, &csim_result);  // PC Relative Load
memAccessCycles += simDCache((SP + outp_addr), 0, &csim_result);
// Simulating I Cache for obj block 1
memAccessCycles += simICache(0x398, 32, &csim_result);
estimate_power("adpcm_coderbb_3", pipelineCycles, memAccessCycles, csim_result.L2Hits, (csim_result.prefetches + csim_result.L2Misses));
pipelineCycles += 15 - (enterBlock(0xfe, 0x105) ? 7 : 0);
  outp =  outdata;
//  memAccessCycles += simDCache(outdata_addr, 1, &csim_result);
  ivtmp_28 = 0;
  bufferstep = 1;
//  # SUCC: 4 [100.0%]  (fallthru,exec)

adpcm_coderbb_4:
//  # PRED: 18 [91.0%]  (true,exec) 3 [100.0%]  (fallthru,exec)
memAccessCycles += simDCache((SP + 0x4), 1, &csim_result);  // Reading Spilt Register
pipelineCycles += 68 - (enterBlock(0x106, 0x137) ? 7 : 0);
  diff = (int) *(short int *)((uintptr_t)indata + (uintptr_t)ivtmp_28) - valpred;
  memAccessCycles += simDCache(indata_addr + (+ivtmp_28), 1, &csim_result);
  if (diff < 0)
    goto adpcm_coderbb_5;
  else
    goto adpcm_coderbb_22;
//  # SUCC: 5 [27.0%]  (true,exec) 22 [73.0%]  (false,exec)

adpcm_coderbb_22:
//  # PRED: 4 [73.0%]  (false,exec)
  sign = 0;
  goto adpcm_coderbb_6;
//  # SUCC: 6 [100.0%]  (fallthru)

adpcm_coderbb_5:
//  # PRED: 4 [27.0%]  (true,exec)
  diff = -diff;
  sign = 8;
//  # SUCC: 6 [100.0%]  (fallthru,exec)

adpcm_coderbb_6:
//  # PRED: 22 [100.0%]  (fallthru) 5 [100.0%]  (fallthru,exec)
  vpdiff = step >> 3;
  if (diff >= step)
    goto adpcm_coderbb_7;
  else
    goto adpcm_coderbb_23;
//  # SUCC: 7 [50.0%]  (true,exec) 23 [50.0%]  (false,exec)

adpcm_coderbb_23:
//  # PRED: 6 [50.0%]  (false,exec)
  delta = 0;
  goto adpcm_coderbb_8;
//  # SUCC: 8 [100.0%]  (fallthru)

adpcm_coderbb_7:
//  # PRED: 6 [50.0%]  (true,exec)
  diff = diff - step;
  vpdiff = vpdiff + step;
  delta = 4;
//  # SUCC: 8 [100.0%]  (fallthru,exec)

adpcm_coderbb_8:
//  # PRED: 23 [100.0%]  (fallthru) 7 [100.0%]  (fallthru,exec)
  step_35 = step >> 1;
  if (diff >= step_35)
    goto adpcm_coderbb_9;
  else
    goto adpcm_coderbb_10;
//  # SUCC: 9 [50.0%]  (true,exec) 10 [50.0%]  (false,exec)

adpcm_coderbb_9:
//  # PRED: 8 [50.0%]  (true,exec)
  delta = delta | 2;
  diff = diff - step_35;
  vpdiff = vpdiff + step_35;
//  # SUCC: 10 [100.0%]  (fallthru,exec)

adpcm_coderbb_10:
//  # PRED: 8 [50.0%]  (false,exec) 9 [100.0%]  (fallthru,exec)
  step_36 = step_35 >> 1;
  if (diff >= step_36)
    goto adpcm_coderbb_11;
  else
    goto adpcm_coderbb_12;
//  # SUCC: 11 [50.0%]  (true,exec) 12 [50.0%]  (false,exec)

adpcm_coderbb_11:
//  # PRED: 10 [50.0%]  (true,exec)
  delta = delta | 1;
  vpdiff = vpdiff + step_36;
//  # SUCC: 12 [100.0%]  (fallthru,exec)

adpcm_coderbb_12:
//  # PRED: 10 [50.0%]  (false,exec) 11 [100.0%]  (fallthru,exec)
  if (sign != 0)
    goto adpcm_coderbb_13;
  else
    goto adpcm_coderbb_14;
//  # SUCC: 13 [50.0%]  (true,exec) 14 [50.0%]  (false,exec)

adpcm_coderbb_13:
//  # PRED: 12 [50.0%]  (true,exec)
  valpred_34 = valpred - vpdiff;
  goto adpcm_coderbb_15;
//  # SUCC: 15 [100.0%]  (fallthru,exec)

adpcm_coderbb_14:
//  # PRED: 12 [50.0%]  (false,exec)
  valpred_34 = vpdiff + valpred;
//  # SUCC: 15 [100.0%]  (fallthru,exec)

adpcm_coderbb_15:
//  # PRED: 13 [100.0%]  (fallthru,exec) 14 [100.0%]  (fallthru,exec)
  valpred_41 = (valpred_34>-32768)?valpred_34:-32768;
  valpred = (valpred_41<32767)?valpred_41:32767;
  delta_37 = delta | sign;
  memAccessCycles += simDCache(indexTable_addr + (4 * (delta_37)), 1, &csim_result);
  index_38 = indexTable[delta_37] + index;
  index_40 = (index_38>0)?index_38:0;
  index = (index_40<88)?index_40:88;
  memAccessCycles += simDCache(stepsizeTable_addr + (4 * (index)), 1, &csim_result);
  step = stepsizeTable[index];
  if (bufferstep != 0)
    goto adpcm_coderbb_16;
  else
    goto adpcm_coderbb_17;
//  # SUCC: 16 [50.0%]  (true,exec) 17 [50.0%]  (false,exec)

adpcm_coderbb_16:
//  # PRED: 15 [50.0%]  (true,exec)
memAccessCycles += simDCache((SP + outputbuffer_addr), 0, &csim_result);
  outputbuffer = delta_37 << 4 & 255;
  goto adpcm_coderbb_18;
//  # SUCC: 18 [100.0%]  (fallthru,exec)

adpcm_coderbb_17:
//  # PRED: 15 [50.0%]  (false,exec)
memAccessCycles += simDCache((SP + outputbuffer_addr), 1, &csim_result);
memAccessCycles += simDCache(outdata_addr + (unsigned long)((uintptr_t)outp - (uintptr_t)outdata), 0, &csim_result); //MANUAL
//memAccessCycles += simDCache((SP + outp_addr), 0, &csim_result);
  *outp =  (signed char) delta_37 & 15 | (signed char) outputbuffer;
  memAccessCycles += simDCache((SP + outp_addr), 0, &csim_result);
  outp = (uintptr_t)outp + 1;
//  # SUCC: 18 [100.0%]  (fallthru,exec)

adpcm_coderbb_18:
//  # PRED: 16 [100.0%]  (fallthru,exec) 17 [100.0%]  (fallthru,exec)
// Simulating I Cache for obj block 2
memAccessCycles += simICache(0x3b8, 200, &csim_result);
estimate_power("adpcm_coderbb_18", pipelineCycles, memAccessCycles, csim_result.L2Hits, (csim_result.prefetches + csim_result.L2Misses));
// TODO: UnmappedLS: Load GlobalVar pcmdata at line 263
// TODO: UnmappedLS: Load LocalVar outp at line 305
// TODO: UnmappedLS: Store GlobalVar pcmdata at line 306
  bufferstep = bufferstep == 0;
  len = len + -1;
  ivtmp_28 = ivtmp_28 + 2;
  if (len != 0)
    goto adpcm_coderbb_4;
  else
    goto adpcm_coderbb_19;
//  # SUCC: 4 [91.0%]  (true,exec) 19 [9.0%]  (false,exec)

adpcm_coderbb_19:
//  # PRED: 18 [9.0%]  (false,exec)
pipelineCycles += 10 - (enterBlock(0x138, 0x13b) ? 7 : 0);
  if (bufferstep == 0)
    goto adpcm_coderbb_20;
  else
    goto adpcm_coderbb_21;
//  # SUCC: 20 [67.0%]  (true,exec) 21 [33.0%]  (false,exec)

adpcm_coderbb_20:
//  # PRED: 19 [67.0%]  (true,exec)
memAccessCycles += simDCache((SP + outputbuffer_addr), 1, &csim_result);
  *outp = (signed char) (signed char) outputbuffer;
  memAccessCycles += simDCache(outdata_addr + (unsigned long)((uintptr_t)outp - (uintptr_t)outdata), 0, &csim_result);

//  # SUCC: 21 [100.0%]  (fallthru,exec)

adpcm_coderbb_21:
//  # PRED: 19 [33.0%]  (false,exec) 20 [100.0%]  (fallthru,exec) 2 [9.0%]  (false,exec)
// Simulating I Cache for obj block 3
memAccessCycles += simICache(0x480, 16, &csim_result);
estimate_power("adpcm_coderbb_21", pipelineCycles, memAccessCycles, csim_result.L2Hits, (csim_result.prefetches + csim_result.L2Misses));
// TODO: UnmappedLS: Load LocalVar outp at line 314
// TODO: UnmappedLS: Store GlobalVar stepsizeTable at line 315
memAccessCycles += simDCache((SP + 0xc), 1, &csim_result);  // Reading Spilt Register
// Simulating I Cache for obj block 4
memAccessCycles += simICache(0x490, 24, &csim_result);
// TODO: UnmappedLS: Store GlobalVar coder_1_state at line 317
// TODO: UnmappedLS: Store GlobalVar coder_1_state at line 318
pipelineCycles += 19 - (enterBlock(0x13c, 0x141) ? 7 : 0);
  state->valprev = (short int) (short int) valpred;
  memAccessCycles += simDCache(state_addr, 0, &csim_result);
  state->index = (char) (char) index;
  memAccessCycles += simDCache(state_addr, 0, &csim_result);
  return;
//  # SUCC: EXIT [100.0%] 

}


