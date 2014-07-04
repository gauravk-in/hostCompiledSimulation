/***********************************************************
 Intermediate representation of
    sha/app_dir/my_mem.c

 Converted by ir2c v0.1

 ***********************************************************/
#include <limits.h>
#include <stdint.h>
#include "ir2c.h"

/*
Author - Suhas Chakravarty
memcpy implementation taken from 
www.danielvik.com/2010/02/fast-memcpy-in-c.html
Renamed to my_memcpy
Created - 17 Nov 2012
Last modified - 17 Nov 2012
*/

#include <stdlib.h>


void* my_memcpy(void* dest, const void* src, size_t count) {
  uintptr_t ivtmp_33;

my_memcpybb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  if (count != 0)
    goto my_memcpybb_5;
  else
    goto my_memcpybb_4;
//  # SUCC: 5 [91.0%]  (true,exec) 4 [9.0%]  (false,exec)

my_memcpybb_5:
//  # PRED: 2 [91.0%]  (true,exec)
  ivtmp_33 = 0;
//  # SUCC: 3 [100.0%]  (fallthru)

my_memcpybb_3:
//  # PRED: 3 [91.0%]  (dfs_back,true,exec) 5 [100.0%]  (fallthru)
  *(char *)((uintptr_t)dest + (uintptr_t)ivtmp_33) = *(char *)((uintptr_t)src + (uintptr_t)ivtmp_33);
  ivtmp_33 = ivtmp_33 + 1;
  if (ivtmp_33 != count)
    goto my_memcpybb_3;
  else
    goto my_memcpybb_4;
//  # SUCC: 3 [91.0%]  (dfs_back,true,exec) 4 [9.0%]  (false,exec)

my_memcpybb_4:
//  # PRED: 3 [9.0%]  (false,exec) 2 [9.0%]  (false,exec)
  return (uintptr_t)dest;
//  # SUCC: EXIT [100.0%] 

}



void* my_memset(void *s, int c, size_t n) {
  uintptr_t ivtmp_77;
  char pretmp_66;

my_memsetbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  if (n != 0)
    goto my_memsetbb_3;
  else
    goto my_memsetbb_5;
//  # SUCC: 3 [91.0%]  (true,exec) 5 [9.0%]  (false,exec)

my_memsetbb_3:
//  # PRED: 2 [91.0%]  (true,exec)
  pretmp_66 = (char) c;
  ivtmp_77 = 0;
//  # SUCC: 4 [100.0%]  (fallthru,exec)

my_memsetbb_4:
//  # PRED: 4 [91.0%]  (dfs_back,true,exec) 3 [100.0%]  (fallthru,exec)
  *(char *)((uintptr_t)s + (uintptr_t)ivtmp_77) = pretmp_66;
  ivtmp_77 = ivtmp_77 + 1;
  if (ivtmp_77 != n)
    goto my_memsetbb_4;
  else
    goto my_memsetbb_5;
//  # SUCC: 4 [91.0%]  (dfs_back,true,exec) 5 [9.0%]  (false,exec)

my_memsetbb_5:
//  # PRED: 4 [9.0%]  (false,exec) 2 [9.0%]  (false,exec)
  return (uintptr_t)s;
//  # SUCC: EXIT [100.0%] 

}


