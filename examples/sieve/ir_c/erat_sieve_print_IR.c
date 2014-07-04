/***********************************************************
 Intermediate representation of
    sieve/app_dir/erat_sieve_print.c

 Converted by ir2c v0.1

 ***********************************************************/
#include <limits.h>
#include <stdint.h>
#include "ir2c.h"

#include <stdio.h>

#define N 500000
unsigned int sieve[N];
unsigned int results[N];


 int main() {
  uintptr_t ivtmp_83;
  int j_82;
  int i_81;
  uintptr_t ivtmp_77;
  uintptr_t D_2264;
  uintptr_t ivtmp_67;
  uintptr_t D_2253;
  uintptr_t ivtmp_60;
  uintptr_t D_2241;
  uintptr_t ivtmp_45;
  int j;
  int i;
  unsigned int D_2182;

mainbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  ivtmp_77 = 0;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

mainbb_3:
//  # PRED: 3 [99.0%]  (dfs_back,true,exec) 2 [100.0%]  (fallthru,exec)
  *(unsigned int*)((uintptr_t)&sieve + (uintptr_t)ivtmp_77) = 1;
  *(unsigned int*)((uintptr_t)&results + (uintptr_t)ivtmp_77) = 0;
  ivtmp_77 = ivtmp_77 + 4;
  if (ivtmp_77 != 2000000)
    goto mainbb_3;
  else
    goto mainbb_15;
//  # SUCC: 3 [99.0%]  (dfs_back,true,exec) 15 [1.0%]  (false,exec)

mainbb_15:
//  # PRED: 3 [1.0%]  (false,exec)
  ivtmp_60 = 6;
  ivtmp_67 = 4;
  i_81 = 2;
//  # SUCC: 4 [100.0%]  (fallthru)

mainbb_4:
//  # PRED: 15 [100.0%]  (fallthru) 7 [99.0%]  (dfs_back,true,exec)
  D_2264 = (unsigned int) i_81;
  if (*(unsigned int*)((uintptr_t)&sieve + (uintptr_t)D_2264 * 4) != 0)
    goto mainbb_5;
  else
    goto mainbb_7;
//  # SUCC: 5 [50.0%]  (true,exec) 7 [50.0%]  (false,exec)

mainbb_5:
//  # PRED: 4 [50.0%]  (true,exec)
  j = (int) ivtmp_67;
  if (j <= 499999)
    goto mainbb_16;
  else
    goto mainbb_7;
//  # SUCC: 16 [91.0%]  (true,exec) 7 [9.0%]  (false,exec)

mainbb_16:
//  # PRED: 5 [91.0%]  (true,exec)
  ivtmp_83 = ivtmp_60;
//  # SUCC: 6 [100.0%]  (fallthru)

mainbb_6:
//  # PRED: 6 [91.0%]  (dfs_back,true,exec) 16 [100.0%]  (fallthru)
  sieve[j] = 0;
  D_2253 = D_2264 + (unsigned int) j;
  j = (int) D_2253;
  ivtmp_83 = ivtmp_83 + D_2264;
  if ((int) (ivtmp_83 - D_2264) <= 499999)
    goto mainbb_6;
  else
    goto mainbb_7;
//  # SUCC: 6 [91.0%]  (dfs_back,true,exec) 7 [9.0%]  (false,exec)

mainbb_7:
//  # PRED: 4 [50.0%]  (false,exec) 6 [9.0%]  (false,exec) 5 [9.0%]  (false,exec)
  i_81 = i_81 + 1;
  ivtmp_67 = ivtmp_67 + 2;
  ivtmp_60 = ivtmp_60 + 3;
  if (i_81 * i_81 <= 499999)
    goto mainbb_4;
  else
    goto mainbb_8;
//  # SUCC: 4 [99.0%]  (dfs_back,true,exec) 8 [1.0%]  (false,exec)

mainbb_8:
//  # PRED: 7 [1.0%]  (false,exec)
  j_82 = 2;
  i = 0;
//  # SUCC: 9 [100.0%]  (fallthru,exec)

mainbb_9:
//  # PRED: 11 [99.0%]  (dfs_back,true,exec) 8 [100.0%]  (fallthru,exec)
  D_2241 = (unsigned int) j_82;
  if (*(unsigned int*)((uintptr_t)&sieve + (uintptr_t)D_2241 * 4) != 0)
    goto mainbb_10;
  else
    goto mainbb_11;
//  # SUCC: 10 [50.0%]  (true,exec) 11 [50.0%]  (false,exec)

mainbb_10:
//  # PRED: 9 [50.0%]  (true,exec)
  results[i] = D_2241;
  i = i + 1;
//  # SUCC: 11 [100.0%]  (fallthru,exec)

mainbb_11:
//  # PRED: 9 [50.0%]  (false,exec) 10 [100.0%]  (fallthru,exec)
  j_82 = j_82 + 1;
  if (j_82 != 500000)
    goto mainbb_9;
  else
    goto mainbb_17;
//  # SUCC: 9 [99.0%]  (dfs_back,true,exec) 17 [1.0%]  (false,exec)

mainbb_17:
//  # PRED: 11 [1.0%]  (false,exec)
  ivtmp_45 = 0;
//  # SUCC: 12 [100.0%]  (fallthru)

mainbb_12:
//  # PRED: 17 [100.0%]  (fallthru) 13 [98.9%]  (dfs_back,true,exec)
  D_2182 = *(unsigned int*)((uintptr_t)&results + (uintptr_t)ivtmp_45);
  if (D_2182 == 0)
    goto mainbb_14;
  else
    goto mainbb_13;
//  # SUCC: 14 [4.5%]  (true,exec) 13 [95.5%]  (false,exec)

mainbb_13:
//  # PRED: 12 [95.5%]  (false,exec)
  printf (&"%d\n"[0], D_2182);
  ivtmp_45 = ivtmp_45 + 4;
  if (ivtmp_45 != 2000000)
    goto mainbb_12;
  else
    goto mainbb_14;
//  # SUCC: 12 [98.9%]  (dfs_back,true,exec) 14 [1.1%]  (false,exec)

mainbb_14:
//  # PRED: 12 [4.5%]  (true,exec) 13 [1.1%]  (false,exec)
  return 0;
//  # SUCC: EXIT [100.0%] 

}


