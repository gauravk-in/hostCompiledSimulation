#ifndef __BACK_ANNOTATE_H
#define __BACK_ANNOTATE_H

#ifdef PLATFORM_MODEL
#include "advance_time.h"
#endif
enum fnTracker
{
  efn_main,
  efn_sieve,
  dummyFN 
};

enum bbTracker
{
  ebb_main,
  ebb_sievebb_14,
  ebb_sievebb_15,
  ebb_sievebb_16,
  ebb_sievebb_17,
  ebb_sievebb_10,
  ebb_sievebb_11,
  ebb_sievebb_12,
  ebb_sievebb_13,
  ebb_sievebb_8,
  ebb_sievebb_8_BrIdGe_sievebb_4,
  ebb_sievebb_9,
  ebb_sievebb_3,
  ebb_sieve,
  ebb_sievebb_6,
  ebb_sievebb_7,
  ebb_sievebb_4,
  ebb_sievebb_5,
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
