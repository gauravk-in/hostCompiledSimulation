#include "crc.h"
#include <stdio.h>
#include "in_data.h"
//#include "in_large.h"
#include "my_variables.h"

DWORD my_crc;
long my_charcnt;

int main()
{
      //DWORD crc;
      //long charcnt;
      register errors = 0;
      //char inFile[] = "../adpcm/data/small.pcm";
      
      errors |= crc32file(in_Data, &my_crc, &my_charcnt);
#ifdef PRINT_RESULTS
     printf("%08lX %7ld \n", my_crc, my_charcnt);
#endif

      return(errors != 0);
}
