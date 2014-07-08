/***********************************************************
 Intermediate representation of
    adpcm/app_dir/adpcm.c

 Converted by ir2c v0.1

 ***********************************************************/
#include <limits.h>
#include <stdint.h>
#include "ir2c.h"

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
  int valpred_58;
  int delta_56;
  int step_55;
  int step_54;
  int valpred_53;
  uintptr_t ivtmp_47;
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
    goto adpcm_coderbb_24;
//  # SUCC: 3 [91.0%]  (true,exec) 24 [9.0%]  (false,exec)

adpcm_coderbb_3:
//  # PRED: 2 [91.0%]  (true,exec)
  outp =  outdata;
  ivtmp_47 = 0;
  bufferstep = 1;
//  # SUCC: 4 [100.0%]  (fallthru,exec)

adpcm_coderbb_4:
//  # PRED: 21 [91.0%]  (dfs_back,true,exec) 3 [100.0%]  (fallthru,exec)
  diff = (int) *(short int *)((uintptr_t)indata + (uintptr_t)ivtmp_47) - valpred;
  if (diff < 0)
    goto adpcm_coderbb_5;
  else
    goto adpcm_coderbb_25;
//  # SUCC: 5 [27.0%]  (true,exec) 25 [73.0%]  (false,exec)

adpcm_coderbb_25:
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
//  # PRED: 25 [100.0%]  (fallthru) 5 [100.0%]  (fallthru,exec)
  vpdiff = step >> 3;
  if (diff >= step)
    goto adpcm_coderbb_7;
  else
    goto adpcm_coderbb_26;
//  # SUCC: 7 [50.0%]  (true,exec) 26 [50.0%]  (false,exec)

adpcm_coderbb_26:
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
//  # PRED: 26 [100.0%]  (fallthru) 7 [100.0%]  (fallthru,exec)
  step_54 = step >> 1;
  if (diff >= step_54)
    goto adpcm_coderbb_9;
  else
    goto adpcm_coderbb_10;
//  # SUCC: 9 [50.0%]  (true,exec) 10 [50.0%]  (false,exec)

adpcm_coderbb_9:
//  # PRED: 8 [50.0%]  (true,exec)
  delta = delta | 2;
  diff = diff - step_54;
  vpdiff = vpdiff + step_54;
//  # SUCC: 10 [100.0%]  (fallthru,exec)

adpcm_coderbb_10:
//  # PRED: 8 [50.0%]  (false,exec) 9 [100.0%]  (fallthru,exec)
  step_55 = step_54 >> 1;
  if (diff >= step_55)
    goto adpcm_coderbb_11;
  else
    goto adpcm_coderbb_12;
//  # SUCC: 11 [50.0%]  (true,exec) 12 [50.0%]  (false,exec)

adpcm_coderbb_11:
//  # PRED: 10 [50.0%]  (true,exec)
  delta = delta | 1;
  vpdiff = vpdiff + step_55;
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
  valpred_53 = valpred - vpdiff;
  goto adpcm_coderbb_15;
//  # SUCC: 15 [100.0%]  (fallthru,exec)

adpcm_coderbb_14:
//  # PRED: 12 [50.0%]  (false,exec)
  valpred_53 = vpdiff + valpred;
//  # SUCC: 15 [100.0%]  (fallthru,exec)

adpcm_coderbb_15:
//  # PRED: 13 [100.0%]  (fallthru,exec) 14 [100.0%]  (fallthru,exec)
  valpred_58 = (valpred_53>-32768)?valpred_53:-32768;
  valpred = (valpred_58<32767)?valpred_58:32767;
  delta_56 = delta | sign;
  index = indexTable[delta_56] + index;
  if (index < 0)
    goto adpcm_coderbb_27;
  else
    goto adpcm_coderbb_16;
//  # SUCC: 27 [27.0%]  (true,exec) 16 [73.0%]  (false,exec)

adpcm_coderbb_27:
//  # PRED: 15 [27.0%]  (true,exec)
  index = 0;
  goto adpcm_coderbb_17;
//  # SUCC: 17 [100.0%]  (fallthru)

adpcm_coderbb_16:
//  # PRED: 15 [73.0%]  (false,exec)
  if (index > 88)
    goto adpcm_coderbb_28;
  else
    goto adpcm_coderbb_17;
//  # SUCC: 28 [68.5%]  (true,exec) 17 [31.5%]  (false,exec)

adpcm_coderbb_28:
//  # PRED: 16 [68.5%]  (true,exec)
  index = 88;
  goto adpcm_coderbb_18;
//  # SUCC: 18 [100.0%]  (fallthru)

adpcm_coderbb_17:
//  # PRED: 16 [31.5%]  (false,exec) 27 [100.0%]  (fallthru)
//  # SUCC: 18 [100.0%]  (fallthru,exec)

adpcm_coderbb_18:
//  # PRED: 17 [100.0%]  (fallthru,exec) 28 [100.0%]  (fallthru)
  step = stepsizeTable[index];
  if (bufferstep != 0)
    goto adpcm_coderbb_19;
  else
    goto adpcm_coderbb_20;
//  # SUCC: 19 [50.0%]  (true,exec) 20 [50.0%]  (false,exec)

adpcm_coderbb_19:
//  # PRED: 18 [50.0%]  (true,exec)
  outputbuffer = delta_56 << 4 & 255;
  goto adpcm_coderbb_21;
//  # SUCC: 21 [100.0%]  (fallthru,exec)

adpcm_coderbb_20:
//  # PRED: 18 [50.0%]  (false,exec)
  *outp =  (signed char) delta_56 & 15 | (signed char) outputbuffer;
  outp = (uintptr_t)outp + 1;
//  # SUCC: 21 [100.0%]  (fallthru,exec)

adpcm_coderbb_21:
//  # PRED: 19 [100.0%]  (fallthru,exec) 20 [100.0%]  (fallthru,exec)
  bufferstep = bufferstep ^ 1;
  len = len + -1;
  ivtmp_47 = ivtmp_47 + 2;
  if (len != 0)
    goto adpcm_coderbb_4;
  else
    goto adpcm_coderbb_22;
//  # SUCC: 4 [91.0%]  (dfs_back,true,exec) 22 [9.0%]  (false,exec)

adpcm_coderbb_22:
//  # PRED: 21 [9.0%]  (false,exec)
  if (bufferstep == 0)
    goto adpcm_coderbb_23;
  else
    goto adpcm_coderbb_24;
//  # SUCC: 23 [67.0%]  (true,exec) 24 [33.0%]  (false,exec)

adpcm_coderbb_23:
//  # PRED: 22 [67.0%]  (true,exec)
  *outp = (signed char) (signed char) outputbuffer;
//  # SUCC: 24 [100.0%]  (fallthru,exec)

adpcm_coderbb_24:
//  # PRED: 22 [33.0%]  (false,exec) 23 [100.0%]  (fallthru,exec) 2 [9.0%]  (false,exec)
  state->valprev = (short int) (short int) valpred;
  state->index = (char) (char) index;
  return;
//  # SUCC: EXIT [100.0%] 

}



void adpcm_decoder(char indata[], short int outdata[], int len, struct adpcm_state *state) {
  int valpred_113;
  int delta_112;
  int valpred_111;
  uintptr_t ivtmp_101;
  short int prephitmp_86;
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
  valpred_111 = state->valprev;
  index = state->index;
  step = stepsizeTable[index];
  if (len > 0)
    goto adpcm_decoderbb_4;
  else
    goto adpcm_decoderbb_3;
//  # SUCC: 4 [91.0%]  (true,exec) 3 [9.0%]  (false,exec)

adpcm_decoderbb_3:
//  # PRED: 2 [9.0%]  (false,exec)
  prephitmp_86 = (short int) valpred_111;
  goto adpcm_decoderbb_22;
//  # SUCC: 22 [100.0%]  (fallthru,exec)

adpcm_decoderbb_4:
//  # PRED: 2 [91.0%]  (true,exec)
  inp =  indata;
  ivtmp_101 = 0;
  bufferstep = 0;
//  # SUCC: 5 [100.0%]  (fallthru,exec)

adpcm_decoderbb_5:
//  # PRED: 21 [100.0%]  (fallthru,dfs_back,exec) 4 [100.0%]  (fallthru,exec)
  if (bufferstep != 0)
    goto adpcm_decoderbb_6;
  else
    goto adpcm_decoderbb_7;
//  # SUCC: 6 [50.0%]  (true,exec) 7 [50.0%]  (false,exec)

adpcm_decoderbb_6:
//  # PRED: 5 [50.0%]  (true,exec)
  delta = inputbuffer & 15;
  goto adpcm_decoderbb_8;
//  # SUCC: 8 [100.0%]  (fallthru,exec)

adpcm_decoderbb_7:
//  # PRED: 5 [50.0%]  (false,exec)
  inputbuffer = (int) *inp;
  inp = (uintptr_t)inp + 1;
  delta = inputbuffer >> 4 & 15;
//  # SUCC: 8 [100.0%]  (fallthru,exec)

adpcm_decoderbb_8:
//  # PRED: 6 [100.0%]  (fallthru,exec) 7 [100.0%]  (fallthru,exec)
  index = indexTable[delta] + index;
  if (index < 0)
    goto adpcm_decoderbb_23;
  else
    goto adpcm_decoderbb_9;
//  # SUCC: 23 [27.0%]  (true,exec) 9 [73.0%]  (false,exec)

adpcm_decoderbb_23:
//  # PRED: 8 [27.0%]  (true,exec)
  index = 0;
  goto adpcm_decoderbb_10;
//  # SUCC: 10 [100.0%]  (fallthru)

adpcm_decoderbb_9:
//  # PRED: 8 [73.0%]  (false,exec)
  if (index > 88)
    goto adpcm_decoderbb_24;
  else
    goto adpcm_decoderbb_10;
//  # SUCC: 24 [68.5%]  (true,exec) 10 [31.5%]  (false,exec)

adpcm_decoderbb_24:
//  # PRED: 9 [68.5%]  (true,exec)
  index = 88;
  goto adpcm_decoderbb_11;
//  # SUCC: 11 [100.0%]  (fallthru)

adpcm_decoderbb_10:
//  # PRED: 9 [31.5%]  (false,exec) 23 [100.0%]  (fallthru)
//  # SUCC: 11 [100.0%]  (fallthru,exec)

adpcm_decoderbb_11:
//  # PRED: 10 [100.0%]  (fallthru,exec) 24 [100.0%]  (fallthru)
  delta_112 = delta & 7;
  vpdiff = step >> 3;
  if (delta_112 & 4 != 0)
    goto adpcm_decoderbb_12;
  else
    goto adpcm_decoderbb_13;
//  # SUCC: 12 [50.0%]  (true,exec) 13 [50.0%]  (false,exec)

adpcm_decoderbb_12:
//  # PRED: 11 [50.0%]  (true,exec)
  vpdiff = vpdiff + step;
//  # SUCC: 13 [100.0%]  (fallthru,exec)

adpcm_decoderbb_13:
//  # PRED: 11 [50.0%]  (false,exec) 12 [100.0%]  (fallthru,exec)
  if (delta_112 & 2 != 0)
    goto adpcm_decoderbb_14;
  else
    goto adpcm_decoderbb_15;
//  # SUCC: 14 [50.0%]  (true,exec) 15 [50.0%]  (false,exec)

adpcm_decoderbb_14:
//  # PRED: 13 [50.0%]  (true,exec)
  vpdiff = vpdiff + (step >> 1);
//  # SUCC: 15 [100.0%]  (fallthru,exec)

adpcm_decoderbb_15:
//  # PRED: 13 [50.0%]  (false,exec) 14 [100.0%]  (fallthru,exec)
  if (delta_112 & 1 != 0)
    goto adpcm_decoderbb_16;
  else
    goto adpcm_decoderbb_17;
//  # SUCC: 16 [50.0%]  (true,exec) 17 [50.0%]  (false,exec)

adpcm_decoderbb_16:
//  # PRED: 15 [50.0%]  (true,exec)
  vpdiff = vpdiff + (step >> 2);
//  # SUCC: 17 [100.0%]  (fallthru,exec)

adpcm_decoderbb_17:
//  # PRED: 15 [50.0%]  (false,exec) 16 [100.0%]  (fallthru,exec)
  if (delta & 8 != 0)
    goto adpcm_decoderbb_18;
  else
    goto adpcm_decoderbb_19;
//  # SUCC: 18 [50.0%]  (true,exec) 19 [50.0%]  (false,exec)

adpcm_decoderbb_18:
//  # PRED: 17 [50.0%]  (true,exec)
  valpred = valpred_111 - vpdiff;
  goto adpcm_decoderbb_20;
//  # SUCC: 20 [100.0%]  (fallthru,exec)

adpcm_decoderbb_19:
//  # PRED: 17 [50.0%]  (false,exec)
  valpred = vpdiff + valpred_111;
//  # SUCC: 20 [100.0%]  (fallthru,exec)

adpcm_decoderbb_20:
//  # PRED: 18 [100.0%]  (fallthru,exec) 19 [100.0%]  (fallthru,exec)
  valpred_113 = (valpred>-32768)?valpred:-32768;
  valpred_111 = (valpred_113<32767)?valpred_113:32767;
  step = stepsizeTable[index];
  prephitmp_86 = (short int) valpred_111;
  *(short int *)((uintptr_t)outdata + (uintptr_t)ivtmp_101) = prephitmp_86;
  len = len + -1;
  ivtmp_101 = ivtmp_101 + 2;
  if (len != 0)
    goto adpcm_decoderbb_21;
  else
    goto adpcm_decoderbb_22;
//  # SUCC: 21 [91.0%]  (true,exec) 22 [9.0%]  (false,exec)

adpcm_decoderbb_21:
//  # PRED: 20 [91.0%]  (true,exec)
  bufferstep = bufferstep ^ 1;
  goto adpcm_decoderbb_5;
//  # SUCC: 5 [100.0%]  (fallthru,dfs_back,exec)

adpcm_decoderbb_22:
//  # PRED: 20 [9.0%]  (false,exec) 3 [100.0%]  (fallthru,exec)
  state->valprev = prephitmp_86;
  state->index = (char) (char) index;
  return;
//  # SUCC: EXIT [100.0%] 

}


