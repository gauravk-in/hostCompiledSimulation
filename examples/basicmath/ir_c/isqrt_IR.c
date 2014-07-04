/***********************************************************
 Intermediate representation of
    basicmath/app_dir/isqrt.c

 Converted by ir2c v0.1

 ***********************************************************/
#include <limits.h>
#include <stdint.h>
#include "ir2c.h"

/* +++Date last modified: 05-Jul-1997 */

#include <string.h>
#include "snipmath.h"

#define BITSPERLONG 32

#define TOP2BITS(x) ((x & (3L << (BITSPERLONG-2))) >> (BITSPERLONG-2))


/* usqrt:
    ENTRY x: unsigned long
    EXIT  returns floor(sqrt(x) * pow(2, BITSPERLONG/2))

    Since the square root never uses more than half the bits
    of the input, we use the other half of the bits to contain
    extra bits of precision after the binary point.

    EXAMPLE
        suppose BITSPERLONG = 32
        then    usqrt(144) = 786432 = 12 * 65536
                usqrt(32) = 370727 = 5.66 * 65536

    NOTES
        (1) change BITSPERLONG to BITSPERLONG/2 if you do not want
            the answer scaled.  Indeed, if you want n bits of
            precision after the binary point, use BITSPERLONG/2+n.
            The code assumes that BITSPERLONG is even.
        (2) This is really better off being written in assembly.
            The line marked below is really a "arithmetic shift left"
            on the double-long value with r in the upper half
            and x in the lower half.  This operation is typically
            expressible in only one or two assembly instructions.
        (3) Unrolling this loop is probably not a bad idea.

    ALGORITHM
        The calculations are the base-two analogue of the square
        root algorithm we all learned in grammar school.  Since we're
        in base 2, there is only one nontrivial trial multiplier.

        Notice that absolutely no multiplications or divisions are performed.
        This means it'll be fast on a wide range of processors.
*/


void usqrt(unsigned long int x, struct int_sqrt *q) {
  int i;
  long unsigned int e;
  long unsigned int r;
  long unsigned int a;
  long unsigned int D_2427;

usqrtbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  a = 0;
  i = 0;
  r = 0;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

usqrtbb_3:
//  # PRED: 5 [96.9%]  (dfs_back,true,exec) 2 [100.0%]  (fallthru,exec)
  D_2427 = r << 2;
  r = (x >> 30) + D_2427;
  x = x << 2;
  a = a << 1;
  e = (a << 1) + 1;
  if (r >= e)
    goto usqrtbb_4;
  else
    goto usqrtbb_5;
//  # SUCC: 4 [50.0%]  (true,exec) 5 [50.0%]  (false,exec)

usqrtbb_4:
//  # PRED: 3 [50.0%]  (true,exec)
  r = r - e;
  a = a + 1;
//  # SUCC: 5 [100.0%]  (fallthru,exec)

usqrtbb_5:
//  # PRED: 3 [50.0%]  (false,exec) 4 [100.0%]  (fallthru,exec)
  i = i + 1;
  if (i != 32)
    goto usqrtbb_3;
  else
    goto usqrtbb_6;
//  # SUCC: 3 [96.9%]  (dfs_back,true,exec) 6 [3.1%]  (false,exec)

usqrtbb_6:
//  # PRED: 5 [3.1%]  (false,exec)
  *(long unsigned int*) q = a;
  return;
//  # SUCC: EXIT [100.0%] 

}


