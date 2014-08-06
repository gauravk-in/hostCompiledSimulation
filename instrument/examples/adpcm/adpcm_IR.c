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
  int valpred_43;
  int index_42;
  int index_40;
  int delta_39;
  int step_38;
  int step_37;
  int valpred_36;
  uintptr_t ivtmp_30;
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
  ivtmp_30 = 0;
  bufferstep = 1;
//  # SUCC: 4 [100.0%]  (fallthru,exec)

adpcm_coderbb_4:
//  # PRED: 18 [91.0%]  (true,exec) 3 [100.0%]  (fallthru,exec)
  diff = (int) *(short int *)((uintptr_t)indata + (uintptr_t)ivtmp_30) - valpred;
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
  step_37 = step >> 1;
  if (diff >= step_37)
    goto adpcm_coderbb_9;
  else
    goto adpcm_coderbb_10;
//  # SUCC: 9 [50.0%]  (true,exec) 10 [50.0%]  (false,exec)

adpcm_coderbb_9:
//  # PRED: 8 [50.0%]  (true,exec)
  delta = delta | 2;
  diff = diff - step_37;
  vpdiff = vpdiff + step_37;
//  # SUCC: 10 [100.0%]  (fallthru,exec)

adpcm_coderbb_10:
//  # PRED: 8 [50.0%]  (false,exec) 9 [100.0%]  (fallthru,exec)
  step_38 = step_37 >> 1;
  if (diff >= step_38)
    goto adpcm_coderbb_11;
  else
    goto adpcm_coderbb_12;
//  # SUCC: 11 [50.0%]  (true,exec) 12 [50.0%]  (false,exec)

adpcm_coderbb_11:
//  # PRED: 10 [50.0%]  (true,exec)
  delta = delta | 1;
  vpdiff = vpdiff + step_38;
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
  valpred_36 = valpred - vpdiff;
  goto adpcm_coderbb_15;
//  # SUCC: 15 [100.0%]  (fallthru,exec)

adpcm_coderbb_14:
//  # PRED: 12 [50.0%]  (false,exec)
  valpred_36 = vpdiff + valpred;
//  # SUCC: 15 [100.0%]  (fallthru,exec)

adpcm_coderbb_15:
//  # PRED: 13 [100.0%]  (fallthru,exec) 14 [100.0%]  (fallthru,exec)
  valpred_43 = (valpred_36>-32768)?valpred_36:-32768;
  valpred = (valpred_43<32767)?valpred_43:32767;
  delta_39 = delta | sign;
  index_40 = indexTable[delta_39] + index;
  index_42 = (index_40>0)?index_40:0;
  index = (index_42<88)?index_42:88;
  step = stepsizeTable[index];
  if (bufferstep != 0)
    goto adpcm_coderbb_16;
  else
    goto adpcm_coderbb_17;
//  # SUCC: 16 [50.0%]  (true,exec) 17 [50.0%]  (false,exec)

adpcm_coderbb_16:
//  # PRED: 15 [50.0%]  (true,exec)
  outputbuffer = delta_39 << 4 & 255;
  goto adpcm_coderbb_18;
//  # SUCC: 18 [100.0%]  (fallthru,exec)

adpcm_coderbb_17:
//  # PRED: 15 [50.0%]  (false,exec)
  *outp =  (signed char) delta_39 & 15 | (signed char) outputbuffer;
  outp = (uintptr_t)outp + 1;
//  # SUCC: 18 [100.0%]  (fallthru,exec)

adpcm_coderbb_18:
//  # PRED: 16 [100.0%]  (fallthru,exec) 17 [100.0%]  (fallthru,exec)
  bufferstep = bufferstep == 0;
  len = len + -1;
  ivtmp_30 = ivtmp_30 + 2;
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



void adpcm_decoder(char indata[], short int outdata[], int len, struct adpcm_state *state) {
  int index_86;
  int valpred_85;
  int delta_83;
  int index_82;
  int valpred_81;
  uintptr_t ivtmp_71;
  int bufferstep;
  int inputbuffer;
  int index;
  int vpdiff;
  int valpred;
  int step;
  int delta;
  signed char * inp;

adpcm_decoderbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  valpred_81 = state->valprev;
  index = state->index;
  step = stepsizeTable[index];
  if (len > 0)
    goto adpcm_decoderbb_3;
  else
    goto adpcm_decoderbb_18;
//  # SUCC: 3 [91.0%]  (true,exec) 18 [9.0%]  (false,exec)

adpcm_decoderbb_3:
//  # PRED: 2 [91.0%]  (true,exec)
  inp =  indata;
  ivtmp_71 = 0;
  bufferstep = 0;
//  # SUCC: 4 [100.0%]  (fallthru,exec)

adpcm_decoderbb_4:
//  # PRED: 17 [100.0%]  (fallthru,dfs_back,exec) 3 [100.0%]  (fallthru,exec)
  if (bufferstep != 0)
    goto adpcm_decoderbb_5;
  else
    goto adpcm_decoderbb_6;
//  # SUCC: 5 [50.0%]  (true,exec) 6 [50.0%]  (false,exec)

adpcm_decoderbb_5:
//  # PRED: 4 [50.0%]  (true,exec)
  delta = inputbuffer & 15;
  goto adpcm_decoderbb_7;
//  # SUCC: 7 [100.0%]  (fallthru,exec)

adpcm_decoderbb_6:
//  # PRED: 4 [50.0%]  (false,exec)
  inputbuffer = (int) *inp;
  inp = (uintptr_t)inp + 1;
  delta = inputbuffer >> 4 & 15;
//  # SUCC: 7 [100.0%]  (fallthru,exec)

adpcm_decoderbb_7:
//  # PRED: 5 [100.0%]  (fallthru,exec) 6 [100.0%]  (fallthru,exec)
  index_82 = indexTable[delta] + index;
  index_86 = (index_82>0)?index_82:0;
  index = (index_86<88)?index_86:88;
  delta_83 = delta & 7;
  vpdiff = step >> 3;
  if (delta_83 & 4 != 0)
    goto adpcm_decoderbb_8;
  else
    goto adpcm_decoderbb_9;
//  # SUCC: 8 [50.0%]  (true,exec) 9 [50.0%]  (false,exec)

adpcm_decoderbb_8:
//  # PRED: 7 [50.0%]  (true,exec)
  vpdiff = vpdiff + step;
//  # SUCC: 9 [100.0%]  (fallthru,exec)

adpcm_decoderbb_9:
//  # PRED: 7 [50.0%]  (false,exec) 8 [100.0%]  (fallthru,exec)
  if (delta_83 & 2 != 0)
    goto adpcm_decoderbb_10;
  else
    goto adpcm_decoderbb_11;
//  # SUCC: 10 [50.0%]  (true,exec) 11 [50.0%]  (false,exec)

adpcm_decoderbb_10:
//  # PRED: 9 [50.0%]  (true,exec)
  vpdiff = vpdiff + (step >> 1);
//  # SUCC: 11 [100.0%]  (fallthru,exec)

adpcm_decoderbb_11:
//  # PRED: 9 [50.0%]  (false,exec) 10 [100.0%]  (fallthru,exec)
  if (delta_83 & 1 != 0)
    goto adpcm_decoderbb_12;
  else
    goto adpcm_decoderbb_13;
//  # SUCC: 12 [50.0%]  (true,exec) 13 [50.0%]  (false,exec)

adpcm_decoderbb_12:
//  # PRED: 11 [50.0%]  (true,exec)
  vpdiff = vpdiff + (step >> 2);
//  # SUCC: 13 [100.0%]  (fallthru,exec)

adpcm_decoderbb_13:
//  # PRED: 11 [50.0%]  (false,exec) 12 [100.0%]  (fallthru,exec)
  if (delta & 8 != 0)
    goto adpcm_decoderbb_14;
  else
    goto adpcm_decoderbb_15;
//  # SUCC: 14 [50.0%]  (true,exec) 15 [50.0%]  (false,exec)

adpcm_decoderbb_14:
//  # PRED: 13 [50.0%]  (true,exec)
  valpred = valpred_81 - vpdiff;
  goto adpcm_decoderbb_16;
//  # SUCC: 16 [100.0%]  (fallthru,exec)

adpcm_decoderbb_15:
//  # PRED: 13 [50.0%]  (false,exec)
  valpred = vpdiff + valpred_81;
//  # SUCC: 16 [100.0%]  (fallthru,exec)

adpcm_decoderbb_16:
//  # PRED: 14 [100.0%]  (fallthru,exec) 15 [100.0%]  (fallthru,exec)
  valpred_85 = (valpred>-32768)?valpred:-32768;
  valpred_81 = (valpred_85<32767)?valpred_85:32767;
  step = stepsizeTable[index];
  *(short int *)((uintptr_t)outdata + (uintptr_t)ivtmp_71) = (short int) (short int) valpred_81;
  len = len + -1;
  ivtmp_71 = ivtmp_71 + 2;
  if (len != 0)
    goto adpcm_decoderbb_17;
  else
    goto adpcm_decoderbb_18;
//  # SUCC: 17 [91.0%]  (true,exec) 18 [9.0%]  (false,exec)

adpcm_decoderbb_17:
//  # PRED: 16 [91.0%]  (true,exec)
  bufferstep = bufferstep == 0;
  goto adpcm_decoderbb_4;
//  # SUCC: 4 [100.0%]  (fallthru,dfs_back,exec)

adpcm_decoderbb_18:
//  # PRED: 16 [9.0%]  (false,exec) 2 [9.0%]  (false,exec)
  state->valprev = (short int) (short int) valpred_81;
  state->index = (char) (char) index;
  return;
//  # SUCC: EXIT [100.0%] 

}


