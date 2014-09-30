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


static void sha_transform(struct SHA_INFO *sha_info) {
  long unsigned int A_133;
  long unsigned int E_132;
  uintptr_t D_131;
  long unsigned int B_130;
  long unsigned int A_129;
  long unsigned int E_128;
  uintptr_t D_127;
  long unsigned int B_126;
  long unsigned int A_125;
  long unsigned int E_124;
  long unsigned int E_123;
  uintptr_t D_122;
  uintptr_t D_121;
  long unsigned int B_120;
  long unsigned int B_119;
  long unsigned int A_118;
  long unsigned int A_117;
  uintptr_t ivtmp_116;
  uintptr_t ivtmp_115;
  long unsigned int C_114;
  long unsigned int temp_113;
  long unsigned int C_105;
  long unsigned int temp_104;
  long unsigned int C_101;
  long unsigned int temp_100;
  long unsigned int C_97;
  uintptr_t ivtmp_94;
  uintptr_t ivtmp_93;
  uintptr_t D_2940;
  uintptr_t ivtmp_79;
  uintptr_t ivtmp_71;
  uintptr_t D_2917;
  uintptr_t ivtmp_63;
  long unsigned int W[80];
  long unsigned int E;
  long unsigned int D;
  long unsigned int C;
  long unsigned int B;
  long unsigned int A;
  long unsigned int temp;

sha_transformbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  ivtmp_94 = (uintptr_t)sha_info;
  ivtmp_93 = 0;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

sha_transformbb_3:
//  # PRED: 3 [94.1%]  (true,exec) 2 [100.0%]  (fallthru,exec)
  *(long unsigned int*)((uintptr_t)&W + (uintptr_t)ivtmp_93) = *(long unsigned int*)((uintptr_t)ivtmp_94 + 28);
  ivtmp_93 = ivtmp_93 + 4;
  ivtmp_94 = ivtmp_94 + 4;
  if (ivtmp_93 != 64)
    goto sha_transformbb_3;
  else
    goto sha_transformbb_4;
//  # SUCC: 3 [94.1%]  (true,exec) 4 [5.9%]  (false,exec)

sha_transformbb_4:
//  # PRED: 3 [5.9%]  (false,exec)
  ivtmp_79 = (uintptr_t)&W[13];
  ivtmp_63 = (uintptr_t)&W;
  D_2940 = ivtmp_63 + 308;
//  # SUCC: 5 [100.0%]  (fallthru,exec)

sha_transformbb_5:
//  # PRED: 5 [98.5%]  (true,exec) 4 [100.0%]  (fallthru,exec)
  *(long unsigned int*)((uintptr_t)ivtmp_79 + 12) =  ((*(long unsigned int*)((uintptr_t)ivtmp_79 + (int)4294967276) ^ *(long unsigned int*)((uintptr_t)ivtmp_79)) ^ *(long unsigned int*)((uintptr_t)ivtmp_79 + (int)4294967252)) ^ *(long unsigned int*)((uintptr_t)ivtmp_79 + (int)4294967244);
  ivtmp_79 = ivtmp_79 + 4;
  if (ivtmp_79 != D_2940)
    goto sha_transformbb_5;
  else
    goto sha_transformbb_6;
//  # SUCC: 5 [98.5%]  (true,exec) 6 [1.5%]  (false,exec)

sha_transformbb_6:
//  # PRED: 5 [1.5%]  (false,exec)
  A = sha_info->digest[0];
  B = sha_info->digest[1];
  C = sha_info->digest[2];
  D = sha_info->digest[3];
  E = sha_info->digest[4];
  A_133 = A;
  ivtmp_71 = 0;
//  # SUCC: 7 [100.0%]  (fallthru,exec)

sha_transformbb_7:
//  # PRED: 13 [100.0%]  (fallthru) 6 [100.0%]  (fallthru,exec)
  temp = (((*(long unsigned int*)((uintptr_t)&W + (uintptr_t)ivtmp_71) + 1518500249) + E) + ((A_133<<27)|(A_133>>(sizeof(A_133)*CHAR_BIT-27)))) + (~B & D | C & B);
  C_97 = (B<<2)|(B>>(sizeof(B)*CHAR_BIT-2));
  ivtmp_71 = ivtmp_71 + 4;
  if (ivtmp_71 != 80)
    goto sha_transformbb_13;
  else
    goto sha_transformbb_8;
//  # SUCC: 13 [95.2%]  (true,exec) 8 [4.8%]  (false,exec)

sha_transformbb_13:
//  # PRED: 7 [95.2%]  (true,exec)
  E = D;
  D = C;
  C = C_97;
  B = A_133;
  A_133 = temp;
  goto sha_transformbb_7;
//  # SUCC: 7 [100.0%]  (fallthru)

sha_transformbb_8:
//  # PRED: 7 [4.8%]  (false,exec)
  D_2917 = ivtmp_63 + 80;
  ivtmp_116 = ivtmp_63;
  E_132 = D;
  D_131 = C;
  B_130 = A_133;
  A_129 = temp;
//  # SUCC: 9 [100.0%]  (fallthru,exec)

sha_transformbb_9:
//  # PRED: 14 [100.0%]  (fallthru) 8 [100.0%]  (fallthru,exec)
  temp_100 = (((*(long unsigned int*)((uintptr_t)ivtmp_116 + 80) + 1859775393) + E_132) + ((A_129<<27)|(A_129>>(sizeof(A_129)*CHAR_BIT-27)))) + ((C_97 ^ B_130) ^ D_131);
  C_101 = (B_130<<2)|(B_130>>(sizeof(B_130)*CHAR_BIT-2));
  ivtmp_116 = ivtmp_116 + 4;
  if (ivtmp_116 != D_2917)
    goto sha_transformbb_14;
  else
    goto sha_transformbb_16;
//  # SUCC: 14 [95.2%]  (true,exec) 16 [4.8%]  (false,exec)

sha_transformbb_16:
//  # PRED: 9 [4.8%]  (false,exec)
  ivtmp_115 = ivtmp_63;
  E_128 = D_131;
  D_127 = C_97;
  B_126 = A_129;
  A_125 = temp_100;
  goto sha_transformbb_10;
//  # SUCC: 10 [100.0%]  (fallthru)

sha_transformbb_14:
//  # PRED: 9 [95.2%]  (true,exec)
  E_132 = D_131;
  D_131 = C_97;
  C_97 = C_101;
  B_130 = A_129;
  A_129 = temp_100;
  goto sha_transformbb_9;
//  # SUCC: 9 [100.0%]  (fallthru)

sha_transformbb_15:
//  # PRED: 10 [95.2%]  (true,exec)
  E_128 = D_127;
  D_127 = C_101;
  C_101 = C_105;
  B_126 = A_125;
  A_125 = temp_104;
//  # SUCC: 10 [100.0%]  (fallthru)

sha_transformbb_10:
//  # PRED: 15 [100.0%]  (fallthru) 16 [100.0%]  (fallthru)
  temp_104 = (((*(long unsigned int*)((uintptr_t)ivtmp_115 + 160) + (int)2400959708) + E_128) + ((A_125<<27)|(A_125>>(sizeof(A_125)*CHAR_BIT-27)))) + ((D_127 | C_101) & B_126 | D_127 & C_101);
  C_105 = (B_126<<2)|(B_126>>(sizeof(B_126)*CHAR_BIT-2));
  ivtmp_115 = ivtmp_115 + 4;
  if (ivtmp_115 != D_2917)
    goto sha_transformbb_15;
  else
    goto sha_transformbb_18;
//  # SUCC: 15 [95.2%]  (true,exec) 18 [4.8%]  (false,exec)

sha_transformbb_18:
//  # PRED: 10 [4.8%]  (false,exec)
  E_123 = D_127;
  D_121 = C_101;
  B_119 = A_125;
  A_117 = temp_104;
//  # SUCC: 11 [100.0%]  (fallthru)

sha_transformbb_11:
//  # PRED: 17 [100.0%]  (fallthru) 18 [100.0%]  (fallthru)
  temp_113 = (((*(long unsigned int*)((uintptr_t)ivtmp_63 + 240) + (int)3395469782) + E_123) + ((A_117<<27)|(A_117>>(sizeof(A_117)*CHAR_BIT-27)))) + ((C_105 ^ B_119) ^ D_121);
  C_114 = (B_119<<2)|(B_119>>(sizeof(B_119)*CHAR_BIT-2));
  ivtmp_63 = ivtmp_63 + 4;
  if (ivtmp_63 != D_2917)
    goto sha_transformbb_17;
  else
    goto sha_transformbb_19;
//  # SUCC: 17 [95.2%]  (true,exec) 19 [4.8%]  (false,exec)

sha_transformbb_17:
//  # PRED: 11 [95.2%]  (true,exec)
  E_123 = D_121;
  D_121 = C_105;
  C_105 = C_114;
  B_119 = A_117;
  A_117 = temp_113;
  goto sha_transformbb_11;
//  # SUCC: 11 [100.0%]  (fallthru)

sha_transformbb_19:
//  # PRED: 11 [4.8%]  (false,exec)
  E_124 = D_121;
  D_122 = C_105;
  B_120 = A_117;
  A_118 = temp_113;
//  # SUCC: 12 [100.0%]  (fallthru)

sha_transformbb_12:
//  # PRED: 19 [100.0%]  (fallthru)
  sha_info->digest[0] =  A_118 + A;
  sha_info->digest[1] =  B_120 + sha_info->digest[1];
  sha_info->digest[2] =  C_114 + sha_info->digest[2];
  sha_info->digest[3] =  D_122 + sha_info->digest[3];
  sha_info->digest[4] =  E_124 + sha_info->digest[4];
  return;
//  # SUCC: EXIT [100.0%] 

}



void sha_init(struct SHA_INFO *sha_info) {
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



void sha_print(struct SHA_INFO *sha_info) {
sha_printbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  printf (&"%08lx %08lx %08lx %08lx %08lx\n"[0], sha_info->digest[0], sha_info->digest[1], sha_info->digest[2], sha_info->digest[3], sha_info->digest[4]);
  return;
//  # SUCC: EXIT [100.0%] 

}



void sha_final(struct SHA_INFO *sha_info) {
  int count_203;
  long unsigned int hi_bit_count;
  long unsigned int lo_bit_count;
  int count;
  long unsigned int * D_2805;

sha_finalbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  lo_bit_count = sha_info->count_lo;
  hi_bit_count = sha_info->count_hi;
  count = (int) (lo_bit_count >> 3) & 63;
  D_2805 = &sha_info->data;
  *(unsigned char*)( (uintptr_t)D_2805 + (unsigned int) count) = 128;
  count_203 = count + 1;
  if (count_203 > 56)
    goto sha_finalbb_3;
  else
    goto sha_finalbb_4;
//  # SUCC: 3 [39.0%]  (true,exec) 4 [61.0%]  (false,exec)

sha_finalbb_3:
//  # PRED: 2 [39.0%]  (true,exec)
  my_memset (D_2805 + (unsigned int) count_203, 0, (size_t) (64 - count_203));
  sha_transform (sha_info);
  my_memset (D_2805, 0, 56);
  goto sha_finalbb_5;
//  # SUCC: 5 [100.0%]  (fallthru,exec)

sha_finalbb_4:
//  # PRED: 2 [61.0%]  (false,exec)
  my_memset (D_2805 + (unsigned int) count_203, 0, (size_t) (56 - count_203));
//  # SUCC: 5 [100.0%]  (fallthru,exec)

sha_finalbb_5:
//  # PRED: 3 [100.0%]  (fallthru,exec) 4 [100.0%]  (fallthru,exec)
  sha_info->data[14] = hi_bit_count;
  sha_info->data[15] = lo_bit_count;
  sha_transform (sha_info);
  return;
//  # SUCC: EXIT [100.0%] 

}



void sha_update(struct SHA_INFO *sha_info, unsigned char *buffer, int count) {
  uintptr_t D_3103;
  uintptr_t ivtmp_232;
  int D_3089;
  uintptr_t D_3086;
  long unsigned int * D_2795;
  long unsigned int D_2787;
  long unsigned int count_1;
  long unsigned int D_2785;

sha_updatebb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  D_2785 = sha_info->count_lo;
  count_1 = (long unsigned int) count;
  D_2787 = count_1 << 3;
  if (D_2785 > D_2787 + D_2785)
    goto sha_updatebb_3;
  else
    goto sha_updatebb_4;
//  # SUCC: 3 [50.0%]  (true,exec) 4 [50.0%]  (false,exec)

sha_updatebb_3:
//  # PRED: 2 [50.0%]  (true,exec)
  sha_info->count_hi =  sha_info->count_hi + 1;
//  # SUCC: 4 [100.0%]  (fallthru,exec)

sha_updatebb_4:
//  # PRED: 2 [50.0%]  (false,exec) 3 [100.0%]  (fallthru,exec)
  sha_info->count_lo =  D_2787 + sha_info->count_lo;
  sha_info->count_hi =  (count_1 >> 29) + sha_info->count_hi;
  if (count > 63)
    goto sha_updatebb_5;
  else
    goto sha_updatebb_8;
//  # SUCC: 5 [91.0%]  (true,exec) 8 [9.0%]  (false,exec)

sha_updatebb_5:
//  # PRED: 4 [91.0%]  (true,exec)
  D_2795 = &sha_info->data;
  ivtmp_232 = 0;
//  # SUCC: 6 [100.0%]  (fallthru,exec)

sha_updatebb_6:
//  # PRED: 6 [91.0%]  (true,exec) 5 [100.0%]  (fallthru,exec)
  D_3103 = ivtmp_232 + (uintptr_t)buffer;
  my_memcpy (D_2795,  D_3103, 64);
  sha_transform (sha_info);
  ivtmp_232 = ivtmp_232 + 64;
  if ((int) (count_1 - ivtmp_232) > 63)
    goto sha_updatebb_6;
  else
    goto sha_updatebb_7;
//  # SUCC: 6 [91.0%]  (true,exec) 7 [9.0%]  (false,exec)

sha_updatebb_7:
//  # PRED: 6 [9.0%]  (false,exec)
  D_3086 = (count_1 + (int)4294967232) / 64;
  buffer = (uintptr_t)buffer + (D_3086 + 1) * 64;
  D_3089 = count + -64;
  count = D_3089 + (int) D_3086 * -64;
//  # SUCC: 8 [100.0%]  (fallthru,exec)

sha_updatebb_8:
//  # PRED: 7 [100.0%]  (fallthru,exec) 4 [9.0%]  (false,exec)
  my_memcpy (&sha_info->data, buffer, (size_t) count);
  return;
//  # SUCC: EXIT [100.0%] 

}



void sha_stream(struct SHA_INFO *sha_info, unsigned char *inData, unsigned long int dSize) {
  long unsigned int end_289;
  long unsigned int end_288;
  uintptr_t ivtmp_273;
  uintptr_t D_3143;
  uintptr_t ivtmp_267;
  unsigned char data[8192];
  long unsigned int count;
  long unsigned int end;
  long unsigned int start;
  long unsigned int j;
  unsigned int ARR_SIZE_4;

sha_streambb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
  ARR_SIZE_4 = ARR_SIZE;
  j = ARR_SIZE_4 / 8192;
  sha_init (sha_info);
  if (j != 0)
    goto sha_streambb_13;
  else
    goto sha_streambb_6;
//  # SUCC: 13 [91.0%]  (true,exec) 6 [9.0%]  (false,exec)

sha_streambb_13:
//  # PRED: 2 [91.0%]  (true,exec)
  end_289 = 0;
  count = 0;
//  # SUCC: 3 [100.0%]  (fallthru)

sha_streambb_3:
//  # PRED: 12 [100.0%]  (fallthru) 13 [100.0%]  (fallthru)
  end_288 = end_289 + 8192;
  if (end_288 > end_289)
    goto sha_streambb_14;
  else
    goto sha_streambb_5;
//  # SUCC: 14 [99.0%]  (true,exec) 5 [1.0%]  (false,exec)

sha_streambb_14:
//  # PRED: 3 [99.0%]  (true,exec)
  ivtmp_273 = 0;
//  # SUCC: 4 [100.0%]  (fallthru)

sha_streambb_4:
//  # PRED: 4 [99.0%]  (true,exec) 14 [100.0%]  (fallthru)
  *(unsigned char*)((uintptr_t)&data + (uintptr_t)ivtmp_273) = *(unsigned char *)((unsigned char *) (end_289 + (uintptr_t)inData) + (uintptr_t)ivtmp_273);
  ivtmp_273 = ivtmp_273 + 1;
  if (ivtmp_273 != 8192)
    goto sha_streambb_4;
  else
    goto sha_streambb_5;
//  # SUCC: 4 [99.0%]  (true,exec) 5 [1.0%]  (false,exec)

sha_streambb_5:
//  # PRED: 4 [1.0%]  (false,exec) 3 [1.0%]  (false,exec)
  sha_update (sha_info, &data, 8192);
  count = count + 1;
  if (j > count)
    goto sha_streambb_12;
  else
    goto sha_streambb_6;
//  # SUCC: 12 [91.0%]  (true,exec) 6 [9.0%]  (false,exec)

sha_streambb_12:
//  # PRED: 5 [91.0%]  (true,exec)
  end_289 = end_288;
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
  D_3143 = end - start;
  ivtmp_267 = 0;
//  # SUCC: 9 [100.0%]  (fallthru,exec)

sha_streambb_9:
//  # PRED: 9 [99.0%]  (true,exec) 8 [100.0%]  (fallthru,exec)
  *(unsigned char*)((uintptr_t)&data + (uintptr_t)ivtmp_267) = *(unsigned char *)((uintptr_t)inData + start + (uintptr_t)ivtmp_267);
  ivtmp_267 = ivtmp_267 + 1;
  if (ivtmp_267 != D_3143)
    goto sha_streambb_9;
  else
    goto sha_streambb_10;
//  # SUCC: 9 [99.0%]  (true,exec) 10 [1.0%]  (false,exec)

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


