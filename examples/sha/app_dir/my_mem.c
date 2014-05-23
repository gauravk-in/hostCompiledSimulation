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
  char* dst8 = (char*)dest;
  char* src8 = (char*)src;

  while (count--) {
      *dst8++ = *src8++;
  }

  return dest;
}

void* my_memset(void *s, int c, size_t n)
{
    char* p=s;
    while(n--)
        *p++ = (char)c;
    return s;
}
