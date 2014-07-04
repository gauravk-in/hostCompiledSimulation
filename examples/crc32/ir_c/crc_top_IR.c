/***********************************************************
 Intermediate representation of
    crc32/app_dir/crc_top.c

 Converted by ir2c v0.1

 ***********************************************************/
#include <limits.h>
#include <stdint.h>
#include "ir2c.h"

#include "crc.h"
#include <stdio.h>
#include "in_data.h"
//#include "in_large.h"
#include "my_variables.h"

DWORD my_crc;
long int my_charcnt;


int main() {
  Boolean_T D_2724;

mainbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  D_2724 = crc32file (&in_Data, &my_crc, &my_charcnt);
  return (int) D_2724 != 0;
//  # SUCC: EXIT [100.0%] 

}


