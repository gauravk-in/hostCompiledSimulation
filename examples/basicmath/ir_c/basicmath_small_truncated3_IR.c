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
  double X_68;
  uintptr_t ivtmp_64;
  uintptr_t ivtmp_55;
  uintptr_t ivtmp_50;
  double Xangle_I_lsm_42;
  double Xangle_I_lsm_41;
  struct int_sqrt q;
  int i;
  int solutions;
  double X;
  double x[3];
  double a1;

mainbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  SolveCubic (1.0e+0, -1.05e+1, 3.2e+1, -3.0e+1, &solutions, &x);
  SolveCubic (1.0e+0, -4.5e+0, 1.7e+1, -3.0e+1, &solutions, &x);
  SolveCubic (1.0e+0, -3.5e+0, 2.2e+1, -3.1e+1, &solutions, &x);
  SolveCubic (1.0e+0, -1.36999999999999992894572642398998141288757324219e+1, 1.0e+0, -3.5e+1, &solutions, &x);
  ivtmp_64 = 0;
  a1 = 3.0e+0;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

mainbb_3:
//  # PRED: 3 [75.0%]  (dfs_back,true,exec) 2 [100.0%]  (fallthru,exec)
  SolveCubic (a1, 1.0e+1, 5.0e+0, -1.0e+0, &solutions, &x);
  SolveCubic (a1, 1.0e+1, 5.0e+0, -2.0e+0, &solutions, &x);
  SolveCubic (a1, 1.0e+1, 5.0e+0, -3.0e+0, &solutions, &x);
  SolveCubic (a1, 1.0e+1, 5.0e+0, -4.0e+0, &solutions, &x);
  SolveCubic (a1, 1.0e+1, 5.5e+0, -1.0e+0, &solutions, &x);
  SolveCubic (a1, 1.0e+1, 5.5e+0, -2.0e+0, &solutions, &x);
  SolveCubic (a1, 1.0e+1, 5.5e+0, -3.0e+0, &solutions, &x);
  SolveCubic (a1, 1.0e+1, 5.5e+0, -4.0e+0, &solutions, &x);
  SolveCubic (a1, 1.0e+1, 6.0e+0, -1.0e+0, &solutions, &x);
  SolveCubic (a1, 1.0e+1, 6.0e+0, -2.0e+0, &solutions, &x);
  SolveCubic (a1, 1.0e+1, 6.0e+0, -3.0e+0, &solutions, &x);
  SolveCubic (a1, 1.0e+1, 6.0e+0, -4.0e+0, &solutions, &x);
  SolveCubic (a1, 1.0e+1, 6.5e+0, -1.0e+0, &solutions, &x);
  SolveCubic (a1, 1.0e+1, 6.5e+0, -2.0e+0, &solutions, &x);
  SolveCubic (a1, 1.0e+1, 6.5e+0, -3.0e+0, &solutions, &x);
  SolveCubic (a1, 1.0e+1, 6.5e+0, -4.0e+0, &solutions, &x);
  SolveCubic (a1, 9.0e+0, 5.0e+0, -1.0e+0, &solutions, &x);
  SolveCubic (a1, 9.0e+0, 5.0e+0, -2.0e+0, &solutions, &x);
  SolveCubic (a1, 9.0e+0, 5.0e+0, -3.0e+0, &solutions, &x);
  SolveCubic (a1, 9.0e+0, 5.0e+0, -4.0e+0, &solutions, &x);
  SolveCubic (a1, 9.0e+0, 5.5e+0, -1.0e+0, &solutions, &x);
  SolveCubic (a1, 9.0e+0, 5.5e+0, -2.0e+0, &solutions, &x);
  SolveCubic (a1, 9.0e+0, 5.5e+0, -3.0e+0, &solutions, &x);
  SolveCubic (a1, 9.0e+0, 5.5e+0, -4.0e+0, &solutions, &x);
  SolveCubic (a1, 9.0e+0, 6.0e+0, -1.0e+0, &solutions, &x);
  SolveCubic (a1, 9.0e+0, 6.0e+0, -2.0e+0, &solutions, &x);
  SolveCubic (a1, 9.0e+0, 6.0e+0, -3.0e+0, &solutions, &x);
  SolveCubic (a1, 9.0e+0, 6.0e+0, -4.0e+0, &solutions, &x);
  SolveCubic (a1, 9.0e+0, 6.5e+0, -1.0e+0, &solutions, &x);
  SolveCubic (a1, 9.0e+0, 6.5e+0, -2.0e+0, &solutions, &x);
  SolveCubic (a1, 9.0e+0, 6.5e+0, -3.0e+0, &solutions, &x);
  SolveCubic (a1, 9.0e+0, 6.5e+0, -4.0e+0, &solutions, &x);
  a1 = a1 + 1.0e+0;
  ivtmp_64 = ivtmp_64 + 1;
  if (ivtmp_64 != 3)
    goto mainbb_3;
  else
    goto mainbb_10;
//  # SUCC: 3 [75.0%]  (dfs_back,true,exec) 10 [25.0%]  (false,exec)

mainbb_10:
//  # PRED: 3 [25.0%]  (false,exec)
  i = 0;
//  # SUCC: 4 [100.0%]  (fallthru)

mainbb_4:
//  # PRED: 4 [98.0%]  (dfs_back,true,exec) 10 [100.0%]  (fallthru)
  usqrt ((long unsigned int) i, &q);
  i = i + 1;
  if (i != 51)
    goto mainbb_4;
  else
    goto mainbb_5;
//  # SUCC: 4 [98.0%]  (dfs_back,true,exec) 5 [2.0%]  (false,exec)

mainbb_5:
//  # PRED: 4 [2.0%]  (false,exec)
  usqrt (1072497001, &q);
  ivtmp_55 = 0;
  X = 0.0;
//  # SUCC: 6 [100.0%]  (fallthru,exec)

mainbb_6:
//  # PRED: 6 [99.0%]  (dfs_back,true,exec) 5 [100.0%]  (fallthru,exec)
  Xangle_I_lsm_42 = (X * 3.14159265358979311599796346854418516159057617188e+0) / 1.8e+2;
  X = X + 1.0e+0;
  ivtmp_55 = ivtmp_55 + 1;
  if (ivtmp_55 != 361)
    goto mainbb_6;
  else
    goto mainbb_7;
//  # SUCC: 6 [99.0%]  (dfs_back,true,exec) 7 [1.0%]  (false,exec)

mainbb_7:
//  # PRED: 6 [1.0%]  (false,exec)
//Invalid sum of outgoing probabilities 0.0%
  Xangle[0] = Xangle_I_lsm_42;
  ivtmp_50 = 0;
  X_68 = 0.0;
//  # SUCC: 8 (fallthru,exec)

mainbb_8:
//  # PRED: 8 [91.0%]  (dfs_back,true,exec) 7 (fallthru,exec)
  Xangle_I_lsm_41 = (X_68 * 1.8e+2) / 3.14159265358979311599796346854418516159057617188e+0;
  X_68 = X_68 + 1.74532925199432954743716805978692718781530857086e-2;
  ivtmp_50 = ivtmp_50 + 1;
  if (ivtmp_50 != 361)
    goto mainbb_8;
  else
    goto mainbb_9;
//  # SUCC: 8 [91.0%]  (dfs_back,true,exec) 9 [9.0%]  (false,exec)

mainbb_9:
//  # PRED: 8 [9.0%]  (false,exec)
  Xangle[1] = Xangle_I_lsm_41;
  return 0;
//  # SUCC: EXIT [100.0%] 

}


