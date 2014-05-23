//23 Oct 2012 - Truncated the 4 nested loop counts (calling SolveCubic). Total iterations
//              reduced to 960 from 18000 in this nest of 4 loops.
// last week of Oct 2012 - Truncated even more, down to 96 iterations in the
//                         4 nested for-loops and 51 in the usqrt loops

#include "snipmath.h"
#include <math.h>

/* The printf's may be removed to isolate just the math calculations */

double Xangle[2];

int main(void)
{
  double  a1 = 1.0, b1 = -10.5, c1 = 32.0, d1 = -30.0;
  double  a2 = 1.0, b2 = -4.5, c2 = 17.0, d2 = -30.0;
  double  a3 = 1.0, b3 = -3.5, c3 = 22.0, d3 = -31.0;
  double  a4 = 1.0, b4 = -13.7, c4 = 1.0, d4 = -35.0;
  double  x[3];
  double X;
  int     solutions;
  int i;
  unsigned long l = 0x3fed0169L;
  struct int_sqrt q;
  long n = 0;

  /* solve soem cubic functions */
  /* should get 3 solutions: 2, 6 & 2.5   */
  SolveCubic(a1, b1, c1, d1, &solutions, x);  
  /* should get 1 solution: 2.5           */
  SolveCubic(a2, b2, c2, d2, &solutions, x);  
  SolveCubic(a3, b3, c3, d3, &solutions, x);
  SolveCubic(a4, b4, c4, d4, &solutions, x);
  /* Now solve some random equations */
  for(a1=3;a1<6;a1++) {
    for(b1=10;b1>8;b1--) {
      for(c1=5;c1<7;c1+=0.5) {
	for(d1=-1;d1>-5;d1--) {
	  SolveCubic(a1, b1, c1, d1, &solutions, x);  
	}
      }
    }
  }
  
  /* perform some integer square roots */
  for (i = 0; i < 51; ++i)
    {
      usqrt(i, &q);
			// remainder differs on some machines
    }
  usqrt(l, &q);


  /* convert some rads to degrees */
  for (X = 0.0; X <= 360.0; X += 1.0)
    Xangle[0] = deg2rad(X);
  for (X = 0.0; X <= (2 * PI + 1e-6); X += (PI / 180))
    Xangle[1] = rad2deg(X);
  
  
  return 0;
}
