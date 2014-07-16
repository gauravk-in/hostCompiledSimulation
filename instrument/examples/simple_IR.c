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
  int prephitmp_52;
  int prephitmp_51;
  int prephitmp_50;
  uintptr_t ivtmp_43;
  int prephitmp_28;

mainbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  prephitmp_51 = b;
  prephitmp_50 = a;
  ivtmp_43 = 0;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

mainbb_3:
//  # PRED: 5 [100.0%]  (fallthru) 2 [100.0%]  (fallthru,exec)
  prephitmp_28 = prephitmp_50 + prephitmp_51;
  ivtmp_43 = ivtmp_43 + 1;
  if (ivtmp_43 != 98)
    goto mainbb_5;
  else
    goto mainbb_6;
//  # SUCC: 5 [91.0%]  (dfs_back,true,exec) 6 [9.0%]  (false,exec)

mainbb_5:
//  # PRED: 3 [91.0%]  (dfs_back,true,exec)
  prephitmp_50 = prephitmp_51;
  prephitmp_51 = prephitmp_28;
  goto mainbb_3;
//  # SUCC: 3 [100.0%]  (fallthru)

mainbb_6:
//  # PRED: 3 [9.0%]  (false,exec)
  prephitmp_52 = prephitmp_28;
//  # SUCC: 4 [100.0%]  (fallthru)

mainbb_4:
//  # PRED: 6 [100.0%]  (fallthru)
  b = prephitmp_28;
  a = prephitmp_51;
  i = 101;
  return prephitmp_52;
//  # SUCC: EXIT [100.0%] 

}


