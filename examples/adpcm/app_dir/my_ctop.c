/*
** Timing - Test timing on adpcm coder and decoder.
**
** The program creates 10Kb garbage, and runs the compressor and
** the decompressor on it.
*/

#include <stdio.h>
#include "adpcm.h"
#include "in_small.h"
//#include "in_large.h"
#include "my_variables.h"
#define DATASIZE 10*1024	/* Data block size */
//ARR_SIZE is the number of short type elements in 
//input data array. defined in in_data_small.h
//unsigned int ARR_SIZE = 13305601;
//unsigned int ARR_SIZE = 684433;
short pcmdata[DATASIZE];
char adpcmdata[DATASIZE/2];

struct adpcm_state coder_1_state;

int main() {
    int i, k;
    unsigned long j, start, end;
    unsigned long count = 0;
#ifdef PRINT_RESULT
    FILE * fOut;
    fOut = fopen("adpcm_encoding.output", "w");
    unsigned long elemCnt = 0;
#endif

    j = ARR_SIZE/(DATASIZE); //no. of blocks
    k = ARR_SIZE%(DATASIZE); //size of last block

    for( count = 0; count < j ; count++)
    {
      start = count*(DATASIZE);
      end = start + (DATASIZE);

      for(i=start; i<end; i++) //get pcm data from source,
                               //in blocks of DATASIZE
      {
        pcmdata[i-start] = in_Data[i];
      }

      //ENCODE into ADPCM
      adpcm_coder(pcmdata, adpcmdata, DATASIZE, &coder_1_state);

    #ifdef PRINT_RESULT
      for(i=0; i<DATASIZE/2; i++)
      {
        elemCnt++;
        if (elemCnt % 500 == 0)
          fprintf(fOut,"%d, \n", (short)adpcmdata[i]);
        else
          fprintf(fOut,"%d,", (short)adpcmdata[i]);
      }
    #endif
    }
    
    //check for left over data in source
    if(k)
    {
      start = j*(DATASIZE);
      end = ARR_SIZE;
      for(i=start; i<end; i++) //get pcm data from source,
                               //in blocks of DATASIZE
      {
        pcmdata[i-start] = in_Data[i];
      }
      //no need to clear rest of pcmdata's old data
      //as can specify size of new data in call to adpcm_coder
      //ENCODE into ADPCM
      adpcm_coder(pcmdata, adpcmdata,(end-start), &coder_1_state);

    #ifdef PRINT_RESULT
      for(i=0; i<(end-start)/2; i++)
      {
        elemCnt++;
        if (elemCnt % 500 == 0)
          fprintf(fOut,"%d, \n", (short)adpcmdata[i]);
        else
          fprintf(fOut,"%d,", (short)adpcmdata[i]);
      }
    #endif

    }

#ifdef PRINT_RESULT
    fprintf(fOut, "\n};");
    printf("Total Elements %lu\n", elemCnt);
    fclose(fOut);
#endif
    
    //printf("\n Size of struct adpcm_state is %d\n", sizeof(struct adpcm_state));
    return 0;
}
