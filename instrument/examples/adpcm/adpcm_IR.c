/***********************************************************
 Intermediate representation of
    adpcm/app_dir/adpcm.c

 Converted by ir2c v0.1

 ***********************************************************/
#include <limits.h>
#include <stdint.h>
#include "ir2c.h"

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
    

void adpcm_coder(short indata[], char outdata[], int len, struct adpcm_state *state) {
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
  int index;
  int vpdiff;
  int valpred;
  int step;
  int diff;
  int delta;
  int sign;
  signed char * outp;

adpcm_coderbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  valpred = state->valprev;
  index = state->index;
  step = stepsizeTable[index];
  if (len > 0)
    goto adpcm_coderbb_3;
  else
    goto adpcm_coderbb_21;
//  # SUCC: 3 [91.0%]  (true,exec) 21 [9.0%]  (false,exec)

adpcm_coderbb_3:
//  # PRED: 2 [91.0%]  (true,exec)
  outp =  outdata;
  ivtmp_28 = 0;
  bufferstep = 1;
//  # SUCC: 4 [100.0%]  (fallthru,exec)

adpcm_coderbb_4:
//  # PRED: 18 [91.0%]  (true,exec) 3 [100.0%]  (fallthru,exec)
  diff = (int) *(short int *)((uintptr_t)indata + (uintptr_t)ivtmp_28) - valpred;
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
  index_38 = indexTable[delta_37] + index;
  index_40 = (index_38>0)?index_38:0;
  index = (index_40<88)?index_40:88;
  step = stepsizeTable[index];
  if (bufferstep != 0)
    goto adpcm_coderbb_16;
  else
    goto adpcm_coderbb_17;
//  # SUCC: 16 [50.0%]  (true,exec) 17 [50.0%]  (false,exec)

adpcm_coderbb_16:
//  # PRED: 15 [50.0%]  (true,exec)
  outputbuffer = delta_37 << 4 & 255;
  goto adpcm_coderbb_18;
//  # SUCC: 18 [100.0%]  (fallthru,exec)

adpcm_coderbb_17:
//  # PRED: 15 [50.0%]  (false,exec)
  *outp =  (signed char) delta_37 & 15 | (signed char) outputbuffer;
  outp = (uintptr_t)outp + 1;
//  # SUCC: 18 [100.0%]  (fallthru,exec)

adpcm_coderbb_18:
//  # PRED: 16 [100.0%]  (fallthru,exec) 17 [100.0%]  (fallthru,exec)
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
  if (bufferstep == 0)
    goto adpcm_coderbb_20;
  else
    goto adpcm_coderbb_21;
//  # SUCC: 20 [67.0%]  (true,exec) 21 [33.0%]  (false,exec)

adpcm_coderbb_20:
//  # PRED: 19 [67.0%]  (true,exec)
  *outp = (signed char) (signed char) outputbuffer;
//  # SUCC: 21 [100.0%]  (fallthru,exec)

adpcm_coderbb_21:
//  # PRED: 19 [33.0%]  (false,exec) 20 [100.0%]  (fallthru,exec) 2 [9.0%]  (false,exec)
  state->valprev = (short int) (short int) valpred;
  state->index = (char) (char) index;
  return;
//  # SUCC: EXIT [100.0%] 

}


