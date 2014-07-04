/***********************************************************
 Intermediate representation of
    sieve/app_dir/erat_sieve_no_print.c

 Converted by ir2c v0.1

 ***********************************************************/
#include <limits.h>
#include <stdint.h>
#include "ir2c.h"

#include <stdio.h>

#define N 500000

unsigned int results[N];

struct test {
  unsigned int v;
  unsigned int k;
} m = { 1, 1 };


void sieve() {
  uintptr_t ivtmp_84;
  int j_82;
  int i_81;
  uintptr_t ivtmp_77;
  uintptr_t D_2271;
  uintptr_t ivtmp_67;
  uintptr_t D_2260;
  uintptr_t ivtmp_58;
  uintptr_t D_2248;
  uintptr_t ivtmp_45;
  int j;
  int i;
  unsigned int sieve[500000];

sievebb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  ivtmp_77 = 0;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

sievebb_3:
//  # PRED: 3 [99.0%]  (dfs_back,true,exec) 2 [100.0%]  (fallthru,exec)
  *(unsigned int*)((uintptr_t)&results + (uintptr_t)ivtmp_77) = 0;
  *(unsigned int*)((uintptr_t)&sieve + (uintptr_t)ivtmp_77) = 1;
  ivtmp_77 = ivtmp_77 + 4;
  if (ivtmp_77 != 2000000)
    goto sievebb_3;
  else
    goto sievebb_15;
//  # SUCC: 3 [99.0%]  (dfs_back,true,exec) 15 [1.0%]  (false,exec)

sievebb_15:
//  # PRED: 3 [1.0%]  (false,exec)
  ivtmp_84 = 6;
  ivtmp_67 = 4;
  i_81 = 2;
//  # SUCC: 4 [100.0%]  (fallthru)

sievebb_4:
//  # PRED: 15 [100.0%]  (fallthru) 7 [99.0%]  (dfs_back,true,exec)
  D_2271 = (unsigned int) i_81;
  if (*(unsigned int*)((uintptr_t)&sieve + (uintptr_t)D_2271 * 4) != 0)
    goto sievebb_5;
  else
    goto sievebb_7;
//  # SUCC: 5 [50.0%]  (true,exec) 7 [50.0%]  (false,exec)

sievebb_5:
//  # PRED: 4 [50.0%]  (true,exec)
  j_82 = (int) ivtmp_67;
  if (j_82 <= 499999)
    goto sievebb_16;
  else
    goto sievebb_7;
//  # SUCC: 16 [91.0%]  (true,exec) 7 [9.0%]  (false,exec)

sievebb_16:
//  # PRED: 5 [91.0%]  (true,exec)
  ivtmp_58 = ivtmp_84;
//  # SUCC: 6 [100.0%]  (fallthru)

sievebb_6:
//  # PRED: 6 [91.0%]  (dfs_back,true,exec) 16 [100.0%]  (fallthru)
  sieve[j_82] = 0;
  D_2260 = (unsigned int) j_82 + D_2271;
  j_82 = (int) D_2260;
  ivtmp_58 = ivtmp_58 + D_2271;
  if ((int) (ivtmp_58 - D_2271) <= 499999)
    goto sievebb_6;
  else
    goto sievebb_7;
//  # SUCC: 6 [91.0%]  (dfs_back,true,exec) 7 [9.0%]  (false,exec)

sievebb_7:
//  # PRED: 4 [50.0%]  (false,exec) 6 [9.0%]  (false,exec) 5 [9.0%]  (false,exec)
  i_81 = i_81 + 1;
  ivtmp_67 = ivtmp_67 + 2;
  ivtmp_84 = ivtmp_84 + 3;
  if (i_81 * i_81 <= 499999)
    goto sievebb_4;
  else
    goto sievebb_8;
//  # SUCC: 4 [99.0%]  (dfs_back,true,exec) 8 [1.0%]  (false,exec)

sievebb_8:
//  # PRED: 7 [1.0%]  (false,exec)
  j = 2;
  i = 0;
//  # SUCC: 9 [100.0%]  (fallthru,exec)

sievebb_9:
//  # PRED: 11 [99.0%]  (dfs_back,true,exec) 8 [100.0%]  (fallthru,exec)
  D_2248 = (unsigned int) j;
  if (*(unsigned int*)((uintptr_t)&sieve + (uintptr_t)D_2248 * 4) != 0)
    goto sievebb_10;
  else
    goto sievebb_11;
//  # SUCC: 10 [50.0%]  (true,exec) 11 [50.0%]  (false,exec)

sievebb_10:
//  # PRED: 9 [50.0%]  (true,exec)
  results[i] = D_2248;
  i = i + 1;
//  # SUCC: 11 [100.0%]  (fallthru,exec)

sievebb_11:
//  # PRED: 9 [50.0%]  (false,exec) 10 [100.0%]  (fallthru,exec)
  j = j + 1;
  if (j != 500000)
    goto sievebb_9;
  else
    goto sievebb_17;
//  # SUCC: 9 [99.0%]  (dfs_back,true,exec) 17 [1.0%]  (false,exec)

sievebb_17:
//  # PRED: 11 [1.0%]  (false,exec)
  ivtmp_45 = 0;
//  # SUCC: 12 [100.0%]  (fallthru)

sievebb_12:
//  # PRED: 17 [100.0%]  (fallthru) 13 [98.9%]  (dfs_back,true,exec)
  if (*(unsigned int*)((uintptr_t)&results + (uintptr_t)ivtmp_45) == 0)
    goto sievebb_14;
  else
    goto sievebb_13;
//  # SUCC: 14 [4.5%]  (true,exec) 13 [95.5%]  (false,exec)

sievebb_13:
//  # PRED: 12 [95.5%]  (false,exec)
  ivtmp_45 = ivtmp_45 + 4;
  if (ivtmp_45 != 2000000)
    goto sievebb_12;
  else
    goto sievebb_14;
//  # SUCC: 12 [98.9%]  (dfs_back,true,exec) 14 [1.1%]  (false,exec)

sievebb_14:
//  # PRED: 12 [4.5%]  (true,exec) 13 [1.1%]  (false,exec)
  m.v = 0;
  return;
//  # SUCC: EXIT [100.0%] 

}



int main(void) {
mainbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  sieve ();
  return 0;
//  # SUCC: EXIT [100.0%] 

}


