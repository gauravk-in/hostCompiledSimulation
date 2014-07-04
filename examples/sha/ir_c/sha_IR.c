/***********************************************************
 Intermediate representation of
    sha/app_dir/sha.c

 Converted by ir2c v0.1

 ***********************************************************/
#include <limits.h>
#include <stdint.h>
#include "ir2c.h"

/* NIST Secure Hash Algorithm */
/* heavily modified by Uwe Hollerbach uh@alumni.caltech edu */
/* from Peter C. Gutmann's implementation as found in */
/* Applied Cryptography by Bruce Schneier */

/* NIST's proposed modification to SHA of 7/11/94 may be */
/* activated by defining USE_MODIFIED_SHA */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "sha.h"
#include "my_mem.h"
//#include "my_defines.h"
//#include "my_variable.h"
/* SHA f()-functions */
extern unsigned int ARR_SIZE;

#define f1(x,y,z)	((x & y) | (~x & z))
#define f2(x,y,z)	(x ^ y ^ z)
#define f3(x,y,z)	((x & y) | (x & z) | (y & z))
#define f4(x,y,z)	(x ^ y ^ z)

/* SHA constants */

#define CONST1		0x5a827999L
#define CONST2		0x6ed9eba1L
#define CONST3		0x8f1bbcdcL
#define CONST4		0xca62c1d6L

/* 32-bit rotate */

#define ROT32(x,n)	((x << n) | (x >> (32 - n)))

#define FUNC(n,i)						\
    temp = ROT32(A,5) + f##n(B,C,D) + E + W[i] + CONST##n;	\
    E = D; D = C; C = ROT32(B,30); B = A; A = temp

/* do SHA transformation */


static void sha_transform(SHA_INFO *sha_info) {
  LONG D_187;
  LONG A_185;
  uintptr_t ivtmp_171;
  uintptr_t ivtmp_170;
  LONG A_169;
  LONG D_168;
  LONG A_167;
  LONG D_166;
  LONG E_165;
  LONG E_164;
  LONG D_163;
  LONG D_162;
  LONG D_161;
  LONG B_160;
  LONG B_159;
  LONG A_158;
  LONG A_157;
  LONG A_156;
  LONG A_155;
  LONG B_154;
  LONG E_153;
  LONG E_152;
  LONG D_151;
  LONG B_150;
  LONG A_149;
  LONG A_148;
  LONG C_147;
  LONG temp_146;
  LONG D_138;
  LONG C_137;
  LONG temp_136;
  LONG C_133;
  LONG temp_132;
  LONG C_129;
  uintptr_t D_2984;
  uintptr_t ivtmp_121;
  uintptr_t ivtmp_113;
  uintptr_t D_2961;
  uintptr_t ivtmp_105;
  LONG W[80];
  LONG E;
  LONG D;
  LONG C;
  LONG B;
  LONG A;
  LONG temp;

sha_transformbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  W[0] = sha_info->data[0];
  W[1] = sha_info->data[1];
  W[2] = sha_info->data[2];
  W[3] = sha_info->data[3];
  W[4] = sha_info->data[4];
  W[5] = sha_info->data[5];
  W[6] = sha_info->data[6];
  W[7] = sha_info->data[7];
  W[8] = sha_info->data[8];
  W[9] = sha_info->data[9];
  W[10] = sha_info->data[10];
  W[11] = sha_info->data[11];
  W[12] = sha_info->data[12];
  W[13] = sha_info->data[13];
  W[14] = sha_info->data[14];
  W[15] = sha_info->data[15];
  ivtmp_121 = (uintptr_t)&W[13];
  ivtmp_105 = (uintptr_t)&W;
  D_2984 = ivtmp_105 + 308;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

sha_transformbb_3:
//  # PRED: 3 [98.4%]  (dfs_back,true,exec) 2 [100.0%]  (fallthru,exec)
  *(LONG*)((uintptr_t)ivtmp_121 + 12) =  ((*(LONG*)((uintptr_t)ivtmp_121 + (int)4294967276) ^ *(LONG*)((uintptr_t)ivtmp_121)) ^ *(LONG*)((uintptr_t)ivtmp_121 + (int)4294967252)) ^ *(LONG*)((uintptr_t)ivtmp_121 + (int)4294967244);
  ivtmp_121 = ivtmp_121 + 4;
  if (ivtmp_121 != D_2984)
    goto sha_transformbb_3;
  else
    goto sha_transformbb_4;
//  # SUCC: 3 [98.4%]  (dfs_back,true,exec) 4 [1.6%]  (false,exec)

sha_transformbb_4:
//  # PRED: 3 [1.6%]  (false,exec)
  A = sha_info->digest[0];
  B = sha_info->digest[1];
  C = sha_info->digest[2];
  D = sha_info->digest[3];
  E = sha_info->digest[4];
  A_155 = A;
  ivtmp_113 = 0;
//  # SUCC: 5 [100.0%]  (fallthru,exec)

sha_transformbb_5:
//  # PRED: 11 [100.0%]  (fallthru) 4 [100.0%]  (fallthru,exec)
  temp = (((*(LONG*)((uintptr_t)&W + (uintptr_t)ivtmp_113) + 1518500249) + E) + ((A_155<<27)|(A_155>>(sizeof(A_155)*CHAR_BIT-27)))) + (~B & D | C & B);
  C_129 = (B<<2)|(B>>(sizeof(B)*CHAR_BIT-2));
  ivtmp_113 = ivtmp_113 + 4;
  A_185 = temp;
  B = A_155;
  D_187 = C;
  E = D;
  if (ivtmp_113 != 80)
    goto sha_transformbb_11;
  else
    goto sha_transformbb_6;
//  # SUCC: 11 [95.0%]  (dfs_back,true,exec) 6 [5.0%]  (false,exec)

sha_transformbb_11:
//  # PRED: 5 [95.0%]  (dfs_back,true,exec)
  D = D_187;
  C = C_129;
  A_155 = A_185;
  goto sha_transformbb_5;
//  # SUCC: 5 [100.0%]  (fallthru)

sha_transformbb_6:
//  # PRED: 5 [5.0%]  (false,exec)
  D_2961 = ivtmp_105 + 80;
  ivtmp_171 = ivtmp_105;
  E_153 = D;
  D_161 = C;
  B_154 = A_155;
  A_156 = temp;
//  # SUCC: 7 [100.0%]  (fallthru,exec)

sha_transformbb_7:
//  # PRED: 12 [100.0%]  (fallthru) 6 [100.0%]  (fallthru,exec)
  temp_132 = (((*(LONG*)((uintptr_t)ivtmp_171 + 80) + 1859775393) + E_153) + ((A_156<<27)|(A_156>>(sizeof(A_156)*CHAR_BIT-27)))) + ((C_129 ^ B_154) ^ D_161);
  C_133 = (B_154<<2)|(B_154>>(sizeof(B_154)*CHAR_BIT-2));
  ivtmp_171 = ivtmp_171 + 4;
  A_148 = temp_132;
  B_154 = A_156;
  D_138 = C_129;
  E_153 = D_161;
  if (ivtmp_171 != D_2961)
    goto sha_transformbb_12;
  else
    goto sha_transformbb_14;
//  # SUCC: 12 [95.0%]  (dfs_back,true,exec) 14 [5.0%]  (false,exec)

sha_transformbb_14:
//  # PRED: 7 [5.0%]  (false,exec)
  ivtmp_170 = ivtmp_105;
  E_164 = D_161;
  D_162 = C_129;
  B_159 = A_156;
  A_157 = temp_132;
  goto sha_transformbb_8;
//  # SUCC: 8 [100.0%]  (fallthru)

sha_transformbb_12:
//  # PRED: 7 [95.0%]  (dfs_back,true,exec)
  D_161 = D_138;
  C_129 = C_133;
  A_156 = A_148;
  goto sha_transformbb_7;
//  # SUCC: 7 [100.0%]  (fallthru)

sha_transformbb_13:
//  # PRED: 8 [95.0%]  (dfs_back,true,exec)
  D_162 = D_166;
  C_133 = C_137;
  A_157 = A_169;
//  # SUCC: 8 [100.0%]  (fallthru)

sha_transformbb_8:
//  # PRED: 13 [100.0%]  (fallthru) 14 [100.0%]  (fallthru)
  temp_136 = (((*(LONG*)((uintptr_t)ivtmp_170 + 160) + (int)2400959708) + E_164) + ((A_157<<27)|(A_157>>(sizeof(A_157)*CHAR_BIT-27)))) + ((D_162 | C_133) & B_159 | D_162 & C_133);
  C_137 = (B_159<<2)|(B_159>>(sizeof(B_159)*CHAR_BIT-2));
  ivtmp_170 = ivtmp_170 + 4;
  A_169 = temp_136;
  B_159 = A_157;
  D_166 = C_133;
  E_164 = D_162;
  if (ivtmp_170 != D_2961)
    goto sha_transformbb_13;
  else
    goto sha_transformbb_16;
//  # SUCC: 13 [95.0%]  (dfs_back,true,exec) 16 [5.0%]  (false,exec)

sha_transformbb_16:
//  # PRED: 8 [5.0%]  (false,exec)
  E_165 = D_162;
  D_163 = C_133;
  B_160 = A_157;
  A_158 = temp_136;
//  # SUCC: 9 [100.0%]  (fallthru)

sha_transformbb_9:
//  # PRED: 15 [100.0%]  (fallthru) 16 [100.0%]  (fallthru)
  temp_146 = (((*(LONG*)((uintptr_t)ivtmp_105 + 240) + (int)3395469782) + E_165) + ((A_158<<27)|(A_158>>(sizeof(A_158)*CHAR_BIT-27)))) + ((C_137 ^ B_160) ^ D_163);
  C_147 = (B_160<<2)|(B_160>>(sizeof(B_160)*CHAR_BIT-2));
  ivtmp_105 = ivtmp_105 + 4;
  A_167 = temp_146;
  B_160 = A_158;
  D_168 = C_137;
  E_165 = D_163;
  if (D_2961 != ivtmp_105)
    goto sha_transformbb_15;
  else
    goto sha_transformbb_17;
//  # SUCC: 15 [95.0%]  (dfs_back,true,exec) 17 [5.0%]  (false,exec)

sha_transformbb_15:
//  # PRED: 9 [95.0%]  (dfs_back,true,exec)
  D_163 = D_168;
  C_137 = C_147;
  A_158 = A_167;
  goto sha_transformbb_9;
//  # SUCC: 9 [100.0%]  (fallthru)

sha_transformbb_17:
//  # PRED: 9 [5.0%]  (false,exec)
  E_152 = D_163;
  D_151 = C_137;
  B_150 = A_158;
  A_149 = temp_146;
//  # SUCC: 10 [100.0%]  (fallthru)

sha_transformbb_10:
//  # PRED: 17 [100.0%]  (fallthru)
  sha_info->digest[0] =  A_149 + A;
  sha_info->digest[1] =  B_150 + sha_info->digest[1];
  sha_info->digest[2] =  C_147 + sha_info->digest[2];
  sha_info->digest[3] =  D_151 + sha_info->digest[3];
  sha_info->digest[4] =  E_152 + sha_info->digest[4];
  return;
//  # SUCC: EXIT [100.0%] 

}



void sha_init(SHA_INFO *sha_info) {
sha_initbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  sha_info->digest[0] = 1732584193;
  sha_info->digest[1] = 4023233417;
  sha_info->digest[2] = 2562383102;
  sha_info->digest[3] = 271733878;
  sha_info->digest[4] = 3285377520;
  sha_info->count_lo = 0;
  sha_info->count_hi = 0;
  return;
//  # SUCC: EXIT [100.0%] 

}



void sha_print(SHA_INFO *sha_info) {
sha_printbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  printf (&"%08lx %08lx %08lx %08lx %08lx\n"[0], sha_info->digest[0], sha_info->digest[1], sha_info->digest[2], sha_info->digest[3], sha_info->digest[4]); //[tail call]
  return;
//  # SUCC: EXIT [100.0%] 

}



void sha_final(SHA_INFO *sha_info) {
  int count_290;
  LONG hi_bit_count;
  LONG lo_bit_count;
  int count;
  LONG * D_2806;

sha_finalbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  lo_bit_count = sha_info->count_lo;
  hi_bit_count = sha_info->count_hi;
  count = (int) (lo_bit_count >> 3) & 63;
  D_2806 = &sha_info->data;
  *(BYTE*)( (uintptr_t)D_2806 + (unsigned int) count) = 128;
  count_290 = count + 1;
  if (count_290 > 56)
    goto sha_finalbb_3;
  else
    goto sha_finalbb_4;
//  # SUCC: 3 [39.0%]  (true,exec) 4 [61.0%]  (false,exec)

sha_finalbb_3:
//  # PRED: 2 [39.0%]  (true,exec)
  my_memset (D_2806 + (unsigned int) count_290, 0, (size_t) (64 - count_290));
  sha_transform (sha_info);
  my_memset (D_2806, 0, 56);
  goto sha_finalbb_5;
//  # SUCC: 5 [100.0%]  (fallthru,exec)

sha_finalbb_4:
//  # PRED: 2 [61.0%]  (false,exec)
  my_memset (D_2806 + (unsigned int) count_290, 0, (size_t) (56 - count_290));
//  # SUCC: 5 [100.0%]  (fallthru,exec)

sha_finalbb_5:
//  # PRED: 3 [100.0%]  (fallthru,exec) 4 [100.0%]  (fallthru,exec)
  sha_info->data[14] = hi_bit_count;
  sha_info->data[15] = lo_bit_count;
  sha_transform (sha_info); //[tail call]
  return;
//  # SUCC: EXIT [100.0%] 

}



void sha_update(SHA_INFO *sha_info, BYTE *buffer, int count) {
  uintptr_t D_3211;
  uintptr_t ivtmp_337;
  int D_3197;
  uintptr_t D_3194;
  size_t prephitmp_324;
  long unsigned int prephitmp_322;
  LONG * D_2796;
  long unsigned int D_2788;
  LONG D_2786;

sha_updatebb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  D_2786 = sha_info->count_lo;
  prephitmp_324 = (size_t) count;
  D_2788 = prephitmp_324 << 3;
  prephitmp_322 = D_2788 + D_2786;
  if (D_2786 > prephitmp_322)
    goto sha_updatebb_3;
  else
    goto sha_updatebb_4;
//  # SUCC: 3 [50.0%]  (true,exec) 4 [50.0%]  (false,exec)

sha_updatebb_3:
//  # PRED: 2 [50.0%]  (true,exec)
  sha_info->count_hi =  sha_info->count_hi + 1;
  prephitmp_322 = D_2788 + sha_info->count_lo;
//  # SUCC: 4 [100.0%]  (fallthru,exec)

sha_updatebb_4:
//  # PRED: 2 [50.0%]  (false,exec) 3 [100.0%]  (fallthru,exec)
  sha_info->count_lo = prephitmp_322;
  sha_info->count_hi =  (prephitmp_324 >> 29) + sha_info->count_hi;
  if (count > 63)
    goto sha_updatebb_5;
  else
    goto sha_updatebb_8;
//  # SUCC: 5 [91.0%]  (true,exec) 8 [9.0%]  (false,exec)

sha_updatebb_5:
//  # PRED: 4 [91.0%]  (true,exec)
  D_2796 = &sha_info->data;
  ivtmp_337 = 0;
//  # SUCC: 6 [100.0%]  (fallthru,exec)

sha_updatebb_6:
//  # PRED: 6 [91.0%]  (dfs_back,true,exec) 5 [100.0%]  (fallthru,exec)
  D_3211 = ivtmp_337 + (uintptr_t)buffer;
  my_memcpy (D_2796,  D_3211, 64);
  sha_transform (sha_info);
  ivtmp_337 = ivtmp_337 + 64;
  if ((int) (prephitmp_324 - ivtmp_337) > 63)
    goto sha_updatebb_6;
  else
    goto sha_updatebb_7;
//  # SUCC: 6 [91.0%]  (dfs_back,true,exec) 7 [9.0%]  (false,exec)

sha_updatebb_7:
//  # PRED: 6 [9.0%]  (false,exec)
  D_3194 = prephitmp_324 + (int)4294967232 >> 6;
  buffer = (uintptr_t)buffer + (D_3194 + 1) * 64;
  D_3197 = count + -64;
  prephitmp_324 = (size_t) (D_3197 + (int) D_3194 * -64);
//  # SUCC: 8 [100.0%]  (fallthru,exec)

sha_updatebb_8:
//  # PRED: 7 [100.0%]  (fallthru,exec) 4 [9.0%]  (false,exec)
  my_memcpy (&sha_info->data, buffer, prephitmp_324); //[tail call]
  return;
//  # SUCC: EXIT [100.0%] 

}



void sha_stream(SHA_INFO *sha_info, BYTE *inData, LONG dSize) {
  LONG end_408;
  LONG end_407;
  uintptr_t ivtmp_392;
  uintptr_t D_3265;
  uintptr_t ivtmp_386;
  BYTE data[8192];
  LONG count;
  LONG end;
  LONG start;
  LONG j;
  unsigned int ARR_SIZE_4;

sha_streambb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  ARR_SIZE_4 = ARR_SIZE;
  j = ARR_SIZE_4 >> 13;
  sha_info->digest[0] = 1732584193;
  sha_info->digest[1] = 4023233417;
  sha_info->digest[2] = 2562383102;
  sha_info->digest[3] = 271733878;
  sha_info->digest[4] = 3285377520;
  sha_info->count_lo = 0;
  sha_info->count_hi = 0;
  if (j != 0)
    goto sha_streambb_12;
  else
    goto sha_streambb_6;
//  # SUCC: 12 [91.0%]  (true,exec) 6 [9.0%]  (false,exec)

sha_streambb_12:
//  # PRED: 2 [91.0%]  (true,exec)
  end_408 = 0;
  count = 0;
//  # SUCC: 3 [100.0%]  (fallthru)

sha_streambb_3:
//  # PRED: 12 [100.0%]  (fallthru) 13 [100.0%]  (fallthru)
  end_407 = end_408 + 8192;
  if (end_407 > end_408)
    goto sha_streambb_14;
  else
    goto sha_streambb_5;
//  # SUCC: 14 [99.0%]  (true,exec) 5 [1.0%]  (false,exec)

sha_streambb_14:
//  # PRED: 3 [99.0%]  (true,exec)
  ivtmp_392 = 0;
//  # SUCC: 4 [100.0%]  (fallthru)

sha_streambb_4:
//  # PRED: 14 [100.0%]  (fallthru) 4 [99.0%]  (dfs_back,true,exec)
  *(BYTE*)((uintptr_t)&data + (uintptr_t)ivtmp_392) = *(BYTE *)((BYTE *) (end_408 + (uintptr_t)inData) + (uintptr_t)ivtmp_392);
  ivtmp_392 = ivtmp_392 + 1;
  if (ivtmp_392 != 8192)
    goto sha_streambb_4;
  else
    goto sha_streambb_5;
//  # SUCC: 4 [99.0%]  (dfs_back,true,exec) 5 [1.0%]  (false,exec)

sha_streambb_5:
//  # PRED: 4 [1.0%]  (false,exec) 3 [1.0%]  (false,exec)
  sha_update (sha_info, &data, 8192);
  count = count + 1;
  if (j > count)
    goto sha_streambb_13;
  else
    goto sha_streambb_6;
//  # SUCC: 13 [91.0%]  (dfs_back,true,exec) 6 [9.0%]  (false,exec)

sha_streambb_13:
//  # PRED: 5 [91.0%]  (dfs_back,true,exec)
  end_408 = end_407;
  goto sha_streambb_3;
//  # SUCC: 3 [100.0%]  (fallthru)

sha_streambb_6:
//  # PRED: 5 [9.0%]  (false,exec) 2 [9.0%]  (false,exec)
  if (ARR_SIZE_4 & 8191 != 0)
    goto sha_streambb_7;
  else
    goto sha_streambb_11;
//  # SUCC: 7 [61.0%]  (true,exec) 11 [39.0%]  (false,exec)

sha_streambb_7:
//  # PRED: 6 [61.0%]  (true,exec)
  start = j * 8192;
  end = ARR_SIZE;
  if (start < end)
    goto sha_streambb_8;
  else
    goto sha_streambb_10;
//  # SUCC: 8 [99.0%]  (true,exec) 10 [1.0%]  (false,exec)

sha_streambb_8:
//  # PRED: 7 [99.0%]  (true,exec)
  D_3265 = end - start;
  ivtmp_386 = 0;
//  # SUCC: 9 [100.0%]  (fallthru,exec)

sha_streambb_9:
//  # PRED: 9 [99.0%]  (dfs_back,true,exec) 8 [100.0%]  (fallthru,exec)
  *(BYTE*)((uintptr_t)&data + (uintptr_t)ivtmp_386) = *(BYTE *)((uintptr_t)inData + start + (uintptr_t)ivtmp_386);
  ivtmp_386 = ivtmp_386 + 1;
  if (ivtmp_386 != D_3265)
    goto sha_streambb_9;
  else
    goto sha_streambb_10;
//  # SUCC: 9 [99.0%]  (dfs_back,true,exec) 10 [1.0%]  (false,exec)

sha_streambb_10:
//  # PRED: 9 [1.0%]  (false,exec) 7 [1.0%]  (false,exec)
  sha_update (sha_info, &data, (int) (end - start));
//  # SUCC: 11 [100.0%]  (fallthru,exec)

sha_streambb_11:
//  # PRED: 6 [39.0%]  (false,exec) 10 [100.0%]  (fallthru,exec)
  sha_final (sha_info);
  return;
//  # SUCC: EXIT [100.0%] 

}


