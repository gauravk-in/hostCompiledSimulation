#ifndef __BACK_ANNOTATE_H
#define __BACK_ANNOTATE_H

#ifdef PLATFORM_MODEL
#include "advance_time.h"
#endif
enum fnTracker
{
  efn_crc32buf,
  efn_crc32file,
  efn_main,
  efn_updateCRC32,
  dummyFN 
};

enum bbTracker
{
  ebb_crc32buf,
  ebb_crc32bufbb_5,
  ebb_crc32bufbb_4,
  ebb_crc32bufbb_7,
  ebb_crc32bufbb_6,
  ebb_crc32bufbb_3,
  ebb_crc32file,
  ebb_crc32filebb_7,
  ebb_crc32filebb_6,
  ebb_crc32filebb_5,
  ebb_crc32filebb_4,
  ebb_crc32filebb_3,
  ebb_main,
  ebb_updateCRC32,
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
