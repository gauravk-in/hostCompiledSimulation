#ifndef __BACK_ANNOTATE_H
#define __BACK_ANNOTATE_H

#ifdef PLATFORM_MODEL
#include "advance_time.h"
#endif
enum fnTracker
{
  efn_main,
  efn_sha_print,
  efn_my_memcpy,
  efn_sha_transform,
  efn_sha_final,
  efn_sha_update,
  efn_my_memset,
  efn_sha_stream,
  efn_sha_init,
  dummyFN 
};

enum bbTracker
{
  ebb_main,
  ebb_sha_print,
  ebb_my_memcpybb_4,
  ebb_my_memcpybb_5,
  ebb_my_memcpybb_3,
  ebb_my_memcpy,
  ebb_sha_transformbb_7,
  ebb_sha_transformbb_6,
  ebb_sha_transformbb_5,
  ebb_sha_transformbb_4,
  ebb_sha_transformbb_3,
  ebb_sha_transformbb_12,
  ebb_sha_transformbb_11,
  ebb_sha_transformbb_16,
  ebb_sha_transformbb_10,
  ebb_sha_transformbb_15,
  ebb_sha_transformbb_9,
  ebb_sha_transformbb_8,
  ebb_sha_transform,
  ebb_sha_transformbb_19,
  ebb_sha_transformbb_13,
  ebb_sha_transformbb_18,
  ebb_sha_transformbb_17,
  ebb_sha_final,
  ebb_sha_finalbb_4,
  ebb_sha_finalbb_3,
  ebb_sha_finalbb_5,
  ebb_sha_update,
  ebb_sha_update_BrIdGe_sha_updatebb_4,
  ebb_sha_updatebb_8,
  ebb_sha_updatebb_5,
  ebb_sha_updatebb_4,
  ebb_sha_updatebb_7,
  ebb_sha_updatebb_6,
  ebb_sha_updatebb_3,
  ebb_my_memsetbb_3,
  ebb_my_memsetbb_4,
  ebb_my_memset,
  ebb_my_memsetbb_5,
  ebb_sha_streambb_10,
  ebb_sha_streambb_11,
  ebb_sha_streambb_12,
  ebb_sha_streambb_13,
  ebb_sha_streambb_14,
  ebb_sha_streambb_8,
  ebb_sha_streambb_9,
  ebb_sha_streambb_9_BrIdGe_sha_streambb_10,
  ebb_sha_streambb_3,
  ebb_sha_stream,
  ebb_sha_streambb_6,
  ebb_sha_streambb_7,
  ebb_sha_streambb_4,
  ebb_sha_streambb_5,
  ebb_sha_init,
  dummyBB 
};

extern enum fnTracker Cur_Fn;
extern enum bbTracker Cur_Block;
extern int Cur_SubBb;

#ifndef PLATFORM_MODEL
extern unsigned long Cycle_count;
#endif
extern double Energy_count;

extern const unsigned int cycle_Data[dummyBB][dummyBB];
extern const double energy_Data[dummyBB][dummyBB];

static inline void incrCycleCount(unsigned int n)
{
  #ifdef PLATFORM_MODEL
    sysc_advanceTime(n);
  #else
    Cycle_count += n;
  #endif
}

static inline void incrEnergyCount(double m)
{
  Energy_count += m;
}

static inline void incrCycleCountFor(enum fnTracker fn, enum bbTracker bb)
{
  #ifdef PLATFORM_MODEL
    sysc_advanceTime(cycle_Data[bb][Cur_Block]);
  #else
    Cycle_count += cycle_Data[bb][Cur_Block];
  #endif
}

static inline void incrEnergyCountFor(enum fnTracker fn, enum bbTracker bb)
{
  Energy_count += energy_Data[bb][Cur_Block];
}

#endif
