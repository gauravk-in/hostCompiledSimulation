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


void sieve_func() {
  int j_76;
  uintptr_t ivtmp_74;
  int i_72;
  uintptr_t ivtmp_68;
  uintptr_t D_2263;
  uintptr_t ivtmp_58;
  uintptr_t D_2252;
  uintptr_t ivtmp_49;
  uintptr_t D_2240;
  uintptr_t D_2230;
  uintptr_t ivtmp_36;
  int j;
  int i;
  unsigned int sieve[500000];

sieve_funcbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  ivtmp_68 = 0;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

sieve_funcbb_3:
//  # PRED: 3 [99.0%]  (true,exec) 2 [100.0%]  (fallthru,exec)
  *(unsigned int*)((uintptr_t)&results + (uintptr_t)ivtmp_68) = 0;
  *(unsigned int*)((uintptr_t)&sieve + (uintptr_t)ivtmp_68) = 1;
  ivtmp_68 = ivtmp_68 + 4;
  if (ivtmp_68 != 2000000)
    goto sieve_funcbb_3;
  else
    goto sieve_funcbb_17;
//  # SUCC: 3 [99.0%]  (true,exec) 17 [1.0%]  (false,exec)

sieve_funcbb_17:
//  # PRED: 3 [1.0%]  (false,exec)
  ivtmp_49 = 6;
  ivtmp_58 = 4;
  i_72 = 2;
//  # SUCC: 4 [100.0%]  (fallthru)

sieve_funcbb_4:
//  # PRED: 7 [99.0%]  (true,exec) 17 [100.0%]  (fallthru)
  D_2263 = (unsigned int) i_72;
  if (*(unsigned int*)((uintptr_t)&sieve + (uintptr_t)D_2263 * 4) != 0)
    goto sieve_funcbb_5;
  else
    goto sieve_funcbb_7;
//  # SUCC: 5 [50.0%]  (true,exec) 7 [50.0%]  (false,exec)

sieve_funcbb_5:
//  # PRED: 4 [50.0%]  (true,exec)
  j_76 = (int) ivtmp_58;
  if (j_76 <= 499999)
    goto sieve_funcbb_18;
  else
    goto sieve_funcbb_7;
//  # SUCC: 18 [91.0%]  (true,exec) 7 [9.0%]  (false,exec)

sieve_funcbb_18:
//  # PRED: 5 [91.0%]  (true,exec)
  ivtmp_74 = ivtmp_49;
//  # SUCC: 6 [100.0%]  (fallthru)

sieve_funcbb_6:
//  # PRED: 6 [91.0%]  (true,exec) 18 [100.0%]  (fallthru)
  sieve[j_76] = 0;
  D_2252 = (unsigned int) j_76 + D_2263;
  j_76 = (int) D_2252;
  ivtmp_74 = D_2263 + ivtmp_74;
  if ((int) (ivtmp_74 - D_2263) <= 499999)
    goto sieve_funcbb_6;
  else
    goto sieve_funcbb_7;
//  # SUCC: 6 [91.0%]  (true,exec) 7 [9.0%]  (false,exec)

sieve_funcbb_7:
//  # PRED: 4 [50.0%]  (false,exec) 6 [9.0%]  (false,exec) 5 [9.0%]  (false,exec)
  i_72 = i_72 + 1;
  ivtmp_58 = ivtmp_58 + 2;
  ivtmp_49 = ivtmp_49 + 3;
  if (i_72 * i_72 <= 499999)
    goto sieve_funcbb_4;
  else
    goto sieve_funcbb_8;
//  # SUCC: 4 [99.0%]  (true,exec) 8 [1.0%]  (false,exec)

sieve_funcbb_8:
//  # PRED: 7 [1.0%]  (false,exec)
  j = 2;
  i = 0;
//  # SUCC: 9 [100.0%]  (fallthru,exec)

sieve_funcbb_9:
//  # PRED: 11 [99.0%]  (true,exec) 8 [100.0%]  (fallthru,exec)
  D_2240 = (unsigned int) j;
  if (*(unsigned int*)((uintptr_t)&sieve + (uintptr_t)D_2240 * 4) != 0)
    goto sieve_funcbb_10;
  else
    goto sieve_funcbb_11;
//  # SUCC: 10 [50.0%]  (true,exec) 11 [50.0%]  (false,exec)

sieve_funcbb_10:
//  # PRED: 9 [50.0%]  (true,exec)
  results[i] = D_2240;
  i = i + 1;
//  # SUCC: 11 [100.0%]  (fallthru,exec)

sieve_funcbb_11:
//  # PRED: 9 [50.0%]  (false,exec) 10 [100.0%]  (fallthru,exec)
  j = j + 1;
  if (j != 500000)
    goto sieve_funcbb_9;
  else
    goto sieve_funcbb_12;
//  # SUCC: 9 [99.0%]  (true,exec) 12 [1.0%]  (false,exec)

sieve_funcbb_12:
//  # PRED: 11 [1.0%]  (false,exec)
  if (results[0] == 0)
    goto sieve_funcbb_16;
  else
    goto sieve_funcbb_13;
//  # SUCC: 16 [4.5%]  (true,exec) 13 [95.5%]  (false,exec)

sieve_funcbb_13:
//  # PRED: 12 [95.5%]  (false,exec)
  ivtmp_36 = (uintptr_t)&results;
  D_2230 = ivtmp_36 + 1999996;
//  # SUCC: 14 [100.0%]  (fallthru,exec)

sieve_funcbb_14:
//  # PRED: 15 [98.9%]  (true,exec) 13 [100.0%]  (fallthru,exec)
  if (*(unsigned int*)((uintptr_t)ivtmp_36 + 4) == 0)
    goto sieve_funcbb_16;
  else
    goto sieve_funcbb_15;
//  # SUCC: 16 [4.5%]  (true,exec) 15 [95.5%]  (false,exec)

sieve_funcbb_15:
//  # PRED: 14 [95.5%]  (false,exec)
  ivtmp_36 = ivtmp_36 + 4;
  if (ivtmp_36 != D_2230)
    goto sieve_funcbb_14;
  else
    goto sieve_funcbb_16;
//  # SUCC: 14 [98.9%]  (true,exec) 16 [1.1%]  (false,exec)

sieve_funcbb_16:
//  # PRED: 14 [4.5%]  (true,exec) 15 [1.1%]  (false,exec) 12 [4.5%]  (true,exec)
  m.v = 0;
  return;
//  # SUCC: EXIT [100.0%] 

}



int main(void) {
mainbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  sieve_func ();
  return 0;
//  # SUCC: EXIT [100.0%] 

}


