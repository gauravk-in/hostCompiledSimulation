/***********************************************************
 Intermediate representation of
    sha/app_dir/sha_driver.c

 Converted by ir2c v0.1

 ***********************************************************/
#include <limits.h>
#include <stdint.h>
#include "ir2c.h"

/* NIST Secure Hash Algorithm */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include "sha.h"
#include "in_small.h"
#include "my_variable.h"
struct SHA_INFO sha_info; //making global


int main() {
mainbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  sha_stream (&sha_info, &in_Data, ARR_SIZE);
  return 0;
//  # SUCC: EXIT [100.0%] 

}


