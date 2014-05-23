#ifndef __BACK_ANNOTATE_H
#define __BACK_ANNOTATE_H

#ifdef PLATFORM_MODEL
#include "advance_time.h"
#endif
enum fnTracker
{
  efn_adpcm_coder,
  efn_adpcm_decoder,
  efn_main,
  dummyFN 
};

enum bbTracker
{
  ebb_adpcm_coderbb_28,
  ebb_adpcm_coderbb_20,
  ebb_adpcm_coderbb_21,
  ebb_adpcm_coderbb_21_BrIdGe_adpcm_coderbb_4,
  ebb_adpcm_coderbb_22,
  ebb_adpcm_coderbb_23,
  ebb_adpcm_coderbb_24,
  ebb_adpcm_coderbb_25,
  ebb_adpcm_coderbb_26,
  ebb_adpcm_coderbb_27,
  ebb_adpcm_coderbb_5,
  ebb_adpcm_coderbb_4,
  ebb_adpcm_coderbb_7,
  ebb_adpcm_coderbb_6,
  ebb_adpcm_coderbb_3,
  ebb_adpcm_coderbb_9,
  ebb_adpcm_coderbb_8,
  ebb_adpcm_coderbb_11,
  ebb_adpcm_coderbb_10,
  ebb_adpcm_coderbb_13,
  ebb_adpcm_coderbb_12,
  ebb_adpcm_coderbb_15,
  ebb_adpcm_coderbb_14,
  ebb_adpcm_coderbb_17,
  ebb_adpcm_coderbb_16,
  ebb_adpcm_coderbb_19,
  ebb_adpcm_coderbb_18,
  ebb_adpcm_coder,
  ebb_adpcm_decoder,
  ebb_adpcm_decoderbb_4,
  ebb_adpcm_decoderbb_5,
  ebb_adpcm_decoderbb_6,
  ebb_adpcm_decoderbb_7,
  ebb_adpcm_decoderbb_3,
  ebb_adpcm_decoderbb_8,
  ebb_adpcm_decoderbb_9,
  ebb_adpcm_decoderbb_18,
  ebb_adpcm_decoderbb_19,
  ebb_adpcm_decoderbb_16,
  ebb_adpcm_decoderbb_17,
  ebb_adpcm_decoderbb_14,
  ebb_adpcm_decoderbb_15,
  ebb_adpcm_decoderbb_12,
  ebb_adpcm_decoderbb_13,
  ebb_adpcm_decoderbb_10,
  ebb_adpcm_decoderbb_11,
  ebb_adpcm_decoderbb_24,
  ebb_adpcm_decoderbb_23,
  ebb_adpcm_decoderbb_22,
  ebb_adpcm_decoderbb_21,
  ebb_adpcm_decoderbb_20,
  ebb_mainbb_5,
  ebb_mainbb_11,
  ebb_mainbb_14,
  ebb_mainbb_8,
  ebb_mainbb_8_BrIdGe_mainbb_11,
  ebb_mainbb_9,
  ebb_mainbb_6,
  ebb_mainbb_7,
  ebb_mainbb_4,
  ebb_mainbb_4_BrIdGe_mainbb_5,
  ebb_main,
  ebb_mainbb_10,
  ebb_mainbb_3,
  ebb_mainbb_12,
  ebb_mainbb_13,
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
