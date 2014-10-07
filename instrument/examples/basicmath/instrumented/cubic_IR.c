/***********************************************************
 Intermediate representation of
    basicmath/app_dir/cubic.c

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

/* +++Date last modified: 05-Jul-1997 */

/*
**  CUBIC.C - Solve a cubic polynomial
**  public domain by Ross Cottrell
*/

#include <math.h>
#include <stdlib.h>
#include "snipmath.h"


void SolveCubic(double  a,
                double  b,
                double  c,
                double  d,
                int    *solutions,
                double *x)
{
  double theta;
  double R2_Q3;
  long double R;
  long double Q;
  long double a2;
  long double a1;
  double iftmp_1;
  double D_2478;
  double D_2475;
  double D_2471;
  double D_2467;
  double D_2463;
  double D_2459;
  long double D_2456;
  double D_2454;
  double D_2451;
  double D_2448;
  long double D_2444;

SolveCubicbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  a1 = b / a;
  a2 = c / a;
  Q = (a1 * a1 + a2 * -3.0e+0) / 9.0e+0;
  R = ((((a1 * 2.0e+0) * a1) * a1 + (a1 * -9.0e+0) * a2) + (d / a) * 2.7e+1) / 5.4e+1;
  D_2444 = (Q * Q) * Q;
  R2_Q3 = R * R - D_2444;
  if (R2_Q3 <= 0.0 != 0)
    goto SolveCubicbb_3;
  else
    goto SolveCubicbb_4;
//  # SUCC: 3 [39.0%]  (true,exec) 4 [61.0%]  (false,exec)

SolveCubicbb_3:
//  # PRED: 2 [39.0%]  (true,exec)
  *solutions = 3;
  D_2448 = sqrt (D_2444);
  theta = acos (R / D_2448);
  D_2451 = sqrt (Q);
  D_2454 = cos (theta / 3.0e+0);
  D_2456 = a1 / -3.0e+0;
  *x =  (D_2451 * -2.0e+0) * D_2454 + D_2456;
  D_2459 = sqrt (Q);
  D_2463 = cos ((theta + 6.28318530717958623199592693708837032318115234375e+0) / 3.0e+0);
  *(double*)((uintptr_t)x + 8) =  D_2456 + (D_2459 * -2.0e+0) * D_2463;
  D_2467 = sqrt (Q);
  D_2471 = cos ((theta + 1.25663706143591724639918538741767406463623046875e+1) / 3.0e+0);
  *(double*)((uintptr_t)x + 16) =  D_2456 + (D_2467 * -2.0e+0) * D_2471;
  goto SolveCubicbb_7;
//  # SUCC: 7 [100.0%]  (fallthru,exec)

SolveCubicbb_4:
//  # PRED: 2 [61.0%]  (false,exec)
  *solutions = 1;
  D_2475 = sqrt (R2_Q3);
  D_2478 = pow (D_2475 + fabsl(R), 3.33333333333333314829616256247390992939472198486e-1);
  if (R < 0.0 != 0)
    goto SolveCubicbb_5;
  else
    goto SolveCubicbb_8;
//  # SUCC: 5 [50.0%]  (true,exec) 8 [50.0%]  (false,exec)

SolveCubicbb_8:
//  # PRED: 4 [50.0%]  (false,exec)
  iftmp_1 = -1.0e+0;
  goto SolveCubicbb_6;
//  # SUCC: 6 [100.0%]  (fallthru)

SolveCubicbb_5:
//  # PRED: 4 [50.0%]  (true,exec)
  iftmp_1 = 1.0e+0;
//  # SUCC: 6 [100.0%]  (fallthru,exec)

SolveCubicbb_6:
//  # PRED: 5 [100.0%]  (fallthru,exec) 8 [100.0%]  (fallthru)
  *x =  iftmp_1 * (D_2478 + Q / D_2478) + a1 / -3.0e+0;
//  # SUCC: 7 [100.0%]  (fallthru,exec)

SolveCubicbb_7:
//  # PRED: 3 [100.0%]  (fallthru,exec) 6 [100.0%]  (fallthru,exec)
  return;
//  # SUCC: EXIT [100.0%] 

}


