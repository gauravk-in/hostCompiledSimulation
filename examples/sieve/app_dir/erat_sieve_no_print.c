#include <stdio.h>

#define N 500000

unsigned int results[N];

struct test {
  unsigned int v;
  unsigned int k;
} m = { 1, 1 };

void sieve()
 {
   unsigned int sieve[N];
 
    int i,j;
    for (i = 0; i != N; ++i) {
       sieve[i] = 0;
       results[i] = 0;
       sieve[i] = 1;
    }
 
    m.v = 0;

    for (i = 2; i*i < N; ++i) {
       if (sieve[i]) {
          for (j = i+i; j < N; j += i) {
             sieve[j] = 0;
          }
       }
    }

    m.v = 1;
 
    i = 0;
    for (j = 2; j < N; ++j) {
       if (sieve[j]) {
          results[i++] = j;
       }
    }
 
    for (i = 0; i != N; ++i) {
       if (!results[i]) {
          break;
       }
       //printf ("%d\n",results[i]);
    }
 
    m.v = 0;
 }

int main(void)
{
  sieve();
  return 0;
}
