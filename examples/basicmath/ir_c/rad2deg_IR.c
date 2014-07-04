/***********************************************************
 Intermediate representation of
    basicmath/app_dir/rad2deg.c

 Converted by ir2c v0.1

 ***********************************************************/
#include <limits.h>
#include <stdint.h>
#include "ir2c.h"

/* +++Date last modified: 05-Jul-1997 */

/*
**  RAD2DEG.C - Functions to convert between radians and degrees
*/

#include <math.h>
#include "snipmath.h"

#undef rad2deg                /* These are macros defined in PI.H */
#undef deg2rad


double rad2deg(double rad) {
rad2degbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  return (rad * 1.8e+2) / 3.14159265358979311599796346854418516159057617188e+0;
//  # SUCC: EXIT [100.0%] 

}



double deg2rad(double deg) {
deg2radbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  return (deg * 3.14159265358979311599796346854418516159057617188e+0) / 1.8e+2;
//  # SUCC: EXIT [100.0%] 

}


