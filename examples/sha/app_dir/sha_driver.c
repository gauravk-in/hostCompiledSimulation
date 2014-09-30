/* NIST Secure Hash Algorithm */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include "sha.h"
#include "in_small.h"
#include "my_variable.h"
struct SHA_INFO sha_info; //making global

int main()
{
  //SHA_INFO sha_info;

  sha_stream(&sha_info, in_Data, ARR_SIZE);
#ifdef PRINT_RESULTS
  sha_print(&sha_info);
#endif   

  return(0);
}
