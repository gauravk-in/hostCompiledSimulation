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
  int j_76;
  uintptr_t ivtmp_75;
  unsigned int temp_74;
  int i_72;
  uintptr_t ivtmp_68;
  uintptr_t D_2256;
  uintptr_t ivtmp_58;
  uintptr_t D_2245;
  uintptr_t ivtmp_49;
  uintptr_t D_2233;
  uintptr_t D_2223;
  uintptr_t ivtmp_36;
  int j;
  int i;
  unsigned int D_2182;

mainbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  ivtmp_68 = 0;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

mainbb_3:
//  # PRED: 3 [99.0%]  (true,exec) 2 [100.0%]  (fallthru,exec)
  *(unsigned int*)((uintptr_t)&sieve + (uintptr_t)ivtmp_68) = 1;
  *(unsigned int*)((uintptr_t)&results + (uintptr_t)ivtmp_68) = 0;
  ivtmp_68 = ivtmp_68 + 4;
  if (ivtmp_68 != 2000000)
    goto mainbb_3;
  else
    goto mainbb_17;
//  # SUCC: 3 [99.0%]  (true,exec) 17 [1.0%]  (false,exec)

mainbb_17:
//  # PRED: 3 [1.0%]  (false,exec)
  ivtmp_49 = 6;
  ivtmp_58 = 4;
  i_72 = 2;
//  # SUCC: 4 [100.0%]  (fallthru)

mainbb_4:
//  # PRED: 7 [99.0%]  (true,exec) 17 [100.0%]  (fallthru)
  D_2256 = (unsigned int) i_72;
  if (*(unsigned int*)((uintptr_t)&sieve + (uintptr_t)D_2256 * 4) != 0)
    goto mainbb_5;
  else
    goto mainbb_7;
//  # SUCC: 5 [50.0%]  (true,exec) 7 [50.0%]  (false,exec)

mainbb_5:
//  # PRED: 4 [50.0%]  (true,exec)
  j_76 = (int) ivtmp_58;
  if (j_76 <= 499999)
    goto mainbb_18;
  else
    goto mainbb_7;
//  # SUCC: 18 [91.0%]  (true,exec) 7 [9.0%]  (false,exec)

mainbb_18:
//  # PRED: 5 [91.0%]  (true,exec)
  ivtmp_75 = ivtmp_49;
//  # SUCC: 6 [100.0%]  (fallthru)

mainbb_6:
//  # PRED: 6 [91.0%]  (true,exec) 18 [100.0%]  (fallthru)
  sieve[j_76] = 0;
  D_2245 = D_2256 + (unsigned int) j_76;
  j_76 = (int) D_2245;
  ivtmp_75 = D_2256 + ivtmp_75;
  if ((int) (ivtmp_75 - D_2256) <= 499999)
    goto mainbb_6;
  else
    goto mainbb_7;
//  # SUCC: 6 [91.0%]  (true,exec) 7 [9.0%]  (false,exec)

mainbb_7:
//  # PRED: 4 [50.0%]  (false,exec) 6 [9.0%]  (false,exec) 5 [9.0%]  (false,exec)
  i_72 = i_72 + 1;
  ivtmp_58 = ivtmp_58 + 2;
  ivtmp_49 = ivtmp_49 + 3;
  if (i_72 * i_72 <= 499999)
    goto mainbb_4;
  else
    goto mainbb_8;
//  # SUCC: 4 [99.0%]  (true,exec) 8 [1.0%]  (false,exec)

mainbb_8:
//  # PRED: 7 [1.0%]  (false,exec)
//Invalid sum of outgoing probabilities 0.0%
  j = 2;
  i = 0;
//  # SUCC: 9 (fallthru,exec)

mainbb_9:
//  # PRED: 11 [99.0%]  (true,exec) 8 (fallthru,exec)
  D_2233 = (unsigned int) j;
  if (*(unsigned int*)((uintptr_t)&sieve + (uintptr_t)D_2233 * 4) != 0)
    goto mainbb_10;
  else
    goto mainbb_11;
//  # SUCC: 10 [50.0%]  (true,exec) 11 [50.0%]  (false,exec)

mainbb_10:
//  # PRED: 9 [50.0%]  (true,exec)
  results[i] = D_2233;
  i = i + 1;
//  # SUCC: 11 [100.0%]  (fallthru,exec)

mainbb_11:
//  # PRED: 9 [50.0%]  (false,exec) 10 [100.0%]  (fallthru,exec)
  j = j + 1;
  if (j != 500000)
    goto mainbb_9;
  else
    goto mainbb_12;
//  # SUCC: 9 [99.0%]  (true,exec) 12 [1.0%]  (false,exec)

mainbb_12:
//  # PRED: 11 [1.0%]  (false,exec)
  temp_74 = results[0];
  if (temp_74 == 0)
    goto mainbb_15;
  else
    goto mainbb_16;
//  # SUCC: 15 [4.5%]  (true,exec) 16 [95.5%]  (false,exec)

mainbb_13:
//  # PRED: 14 [98.9%]  (true,exec) 16 [100.0%]  (fallthru,exec)
  D_2182 = *(unsigned int*)((uintptr_t)ivtmp_36 + 4);
  if (D_2182 == 0)
    goto mainbb_15;
  else
    goto mainbb_14;
//  # SUCC: 15 [4.5%]  (true,exec) 14 [95.5%]  (false,exec)

mainbb_14:
//  # PRED: 13 [95.5%]  (false,exec)
  printf (&"%d\n"[0], D_2182);
  ivtmp_36 = ivtmp_36 + 4;
  if (ivtmp_36 != D_2223)
    goto mainbb_13;
  else
    goto mainbb_15;
//  # SUCC: 13 [98.9%]  (true,exec) 15 [1.1%]  (false,exec)

mainbb_15:
//  # PRED: 13 [4.5%]  (true,exec) 14 [1.1%]  (false,exec) 12 [4.5%]  (true,exec)
  return 0;
//  # SUCC: EXIT [100.0%] 

mainbb_16:
//  # PRED: 12 [95.5%]  (false,exec)
  printf (&"%d\n"[0], temp_74);
  ivtmp_36 = (uintptr_t)&results;
  D_2223 = ivtmp_36 + 1999996;
  goto mainbb_13;
//  # SUCC: 13 [100.0%]  (fallthru,exec)

}


