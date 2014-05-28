/***********************************************************
 Intermediate representation of
    simple/app_dir/simple.c

 Converted by ir2c v0.1

 ***********************************************************/
#include <limits.h>
#include <stdint.h>
#include "ir2c.h"



#define FIB_MAX_NUM 15

int a=0, b=1;
int i;


int main(int argc, char* argv) {
  int prephitmp_42;
  int prephitmp_41;
  int prephitmp_40;
  uintptr_t ivtmp_33;
  int prephitmp_18;

mainbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  prephitmp_41 = b;
  prephitmp_40 = a;
  ivtmp_33 = 0;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

mainbb_3:
//  # PRED: 5 [100.0%]  (fallthru) 2 [100.0%]  (fallthru,exec)
  prephitmp_18 = prephitmp_40 + prephitmp_41;
  ivtmp_33 = ivtmp_33 + 1;
  if (ivtmp_33 != 98)
    goto mainbb_5;
  else
    goto mainbb_6;
//  # SUCC: 5 [91.0%]  (dfs_back,true,exec) 6 [9.0%]  (false,exec)

mainbb_5:
//  # PRED: 3 [91.0%]  (dfs_back,true,exec)
  prephitmp_40 = prephitmp_41;
  prephitmp_41 = prephitmp_18;
  goto mainbb_3;
//  # SUCC: 3 [100.0%]  (fallthru)

mainbb_6:
//  # PRED: 3 [9.0%]  (false,exec)
  prephitmp_42 = prephitmp_18;
//  # SUCC: 4 [100.0%]  (fallthru)

mainbb_4:
//  # PRED: 6 [100.0%]  (fallthru)
  b = prephitmp_18;
  a = prephitmp_41;
  i = 101;
  return prephitmp_42;
//  # SUCC: EXIT [100.0%] 

}


