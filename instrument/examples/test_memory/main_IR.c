/***********************************************************
 Intermediate representation of
    test_memory/app_dir/main.c

 Converted by ir2c v0.1

 ***********************************************************/
#include <limits.h>
#include <stdint.h>
#include "ir2c.h"

#include "test_memory.h"


int main() {
mainbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  fill_L1_DCache ();
  fill_L2_Cache ();
  fill_L1_read_again ();
  return 0;
//  # SUCC: EXIT [100.0%] 

}


