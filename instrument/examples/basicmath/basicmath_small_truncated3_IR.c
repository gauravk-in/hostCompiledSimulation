/***********************************************************
 Intermediate representation of
    basicmath/app_dir/basicmath_small_truncated3.c

 Converted by ir2c v0.1

 ***********************************************************/
#include <limits.h>
#include <stdint.h>
#include "ir2c.h"

//23 Oct 2012 - Truncated the 4 nested loop counts (calling SolveCubic). Total iterations
//              reduced to 960 from 18000 in this nest of 4 loops.
// last week of Oct 2012 - Truncated even more, down to 96 iterations in the
//                         4 nested for-loops and 51 in the usqrt loops

#include "snipmath.h"
#include <math.h>

/* The printf's may be removed to isolate just the math calculations */

double Xangle[2];


int main(void) {
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
  c1 = c1 + 5.0e-1;
  ivtmp_50 = ivtmp_50 + 1;
  if (ivtmp_50 != 4)
    goto mainbb_5;
  else
    goto mainbb_6;
//  # SUCC: 5 [91.0%]  (true,exec) 6 [9.0%]  (false,exec)

mainbb_5:
//  # PRED: 4 [91.0%]  (true,exec) 7 [100.0%]  (fallthru,exec)
  ivtmp_46 = 0;
  d1 = -1.0e+0;
  goto mainbb_3;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

mainbb_6:
//  # PRED: 4 [9.0%]  (false,exec)
  b1 = b1 - 1.0e+0;
  ivtmp_54 = ivtmp_54 + 1;
  if (ivtmp_54 != 2)
    goto mainbb_7;
  else
    goto mainbb_8;
//  # SUCC: 7 [91.0%]  (true,exec) 8 [9.0%]  (false,exec)

mainbb_7:
//  # PRED: 6 [91.0%]  (true,exec) 9 [100.0%]  (fallthru,exec)
  ivtmp_50 = 0;
  c1 = 5.0e+0;
  goto mainbb_5;
//  # SUCC: 5 [100.0%]  (fallthru,exec)

mainbb_8:
//  # PRED: 6 [9.0%]  (false,exec)
  a1 = a1 + 1.0e+0;
  ivtmp_58 = ivtmp_58 + 1;
  if (ivtmp_58 != 3)
    goto mainbb_9;
  else
    goto mainbb_16;
//  # SUCC: 9 [75.0%]  (true,exec) 16 [25.0%]  (false,exec)

mainbb_9:
//  # PRED: 8 [75.0%]  (true,exec) 2 [100.0%]  (fallthru,exec)
  ivtmp_54 = 0;
  b1 = 1.0e+1;
  goto mainbb_7;
//  # SUCC: 7 [100.0%]  (fallthru,exec)

mainbb_16:
//  # PRED: 8 [25.0%]  (false,exec)
  i = 0;
//  # SUCC: 10 [100.0%]  (fallthru)

mainbb_10:
//  # PRED: 10 [98.1%]  (true,exec) 16 [100.0%]  (fallthru)
  usqrt ((long unsigned int) i, &q);
  i = i + 1;
  if (i != 51)
    goto mainbb_10;
  else
    goto mainbb_11;
//  # SUCC: 10 [98.1%]  (true,exec) 11 [1.9%]  (false,exec)

mainbb_11:
//  # PRED: 10 [1.9%]  (false,exec)
//Invalid sum of outgoing probabilities 0.0%
  usqrt (1072497001, &q);
  ivtmp_37 = 0;
  X = 0.0;
//  # SUCC: 12 (fallthru,exec)

mainbb_12:
//  # PRED: 12 [99.0%]  (true,exec) 11 (fallthru,exec)
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
//Invalid sum of outgoing probabilities 0.0%
  Xangle[0] = Xangle_I_lsm_24;
  ivtmp_32 = 0;
  X_62 = 0.0;
//  # SUCC: 14 (fallthru,exec)

mainbb_14:
//  # PRED: 14 [91.0%]  (true,exec) 13 (fallthru,exec)
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
  Xangle[1] = Xangle_I_lsm_23;
  return 0;
//  # SUCC: EXIT [100.0%] 

}


