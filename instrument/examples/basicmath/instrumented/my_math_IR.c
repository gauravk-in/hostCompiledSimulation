/***********************************************************
 Intermediate representation of
    basicmath/app_dir/my_math.c

 Converted by ir2c v0.1

 ***********************************************************/
#include <limits.h>
#include <stdint.h>
#include "ir2c.h"
#include "cacheSim.h"
#include "branchPred.h"
extern unsigned long SP;
extern unsigned long long memAccessCycles;
extern unsigned long long pipelineCycles;

#include <stdio.h>

#define SQRTCNT 163
#define ACOSCNT 21
#define COSCNT 63
#define POWCNT 79

#define MY_MARGIN 0.002 

struct Pair
{
  long double input;
  long double output;
};

struct Pair1
{
  long double input1;
  long double input2;
  long double output;
};

struct Pair sQrt_LkUpTbl[SQRTCNT] = {
  {3.969329, 1.992317},
  {1.583333, 1.258306},
  {1.583333, 1.258306},
  {1.583333, 1.258306},
  {71.525463, 8.457273},
  {231.115741, 15.202491},
  {3557.867870, 59.647866},
  {0.313064, 0.559521},
  {0.679012, 0.824022},
  {0.679012, 0.824022},
  {0.679012, 0.824022},
  {0.313064, 0.559521},
  {0.679012, 0.824022},
  {0.679012, 0.824022},
  {0.679012, 0.824022},
  {0.313064, 0.559521},
  {0.679012, 0.824022},
  {0.679012, 0.824022},
  {0.679012, 0.824022},
  {0.313064, 0.559521},
  {0.679012, 0.824022},
  {0.679012, 0.824022},
  {0.679012, 0.824022},
  {0.242337, 0.492277},
  {0.623457, 0.789593},
  {0.623457, 0.789593},
  {0.623457, 0.789593},
  {0.242337, 0.492277},
  {0.623457, 0.789593},
  {0.623457, 0.789593},
  {0.623457, 0.789593},
  {0.242337, 0.492277},
  {0.623457, 0.789593},
  {0.623457, 0.789593},
  {0.623457, 0.789593},
  {0.242337, 0.492277},
  {0.623457, 0.789593},
  {0.623457, 0.789593},
  {0.623457, 0.789593},
  {0.183155, 0.427966},
  {0.567901, 0.753592},
  {0.567901, 0.753592},
  {0.567901, 0.753592},
  {0.183155, 0.427966},
  {0.567901, 0.753592},
  {0.567901, 0.753592},
  {0.567901, 0.753592},
  {0.183155, 0.427966},
  {0.567901, 0.753592},
  {0.567901, 0.753592},
  {0.567901, 0.753592},
  {0.183155, 0.427966},
  {0.567901, 0.753592},
  {0.567901, 0.753592},
  {0.567901, 0.753592},
  {0.134490, 0.366728},
  {0.512346, 0.715783},
  {0.512346, 0.715783},
  {0.512346, 0.715783},
  {0.134490, 0.366728},
  {0.512346, 0.715783},
  {0.512346, 0.715783},
  {0.512346, 0.715783},
  {0.134490, 0.366728},
  {0.512346, 0.715783},
  {0.512346, 0.715783},
  {0.512346, 0.715783},
  {0.114140, 0.337847},
  {0.087791, 0.296296},
  {0.444444, 0.666667},
  {0.444444, 0.666667},
  {0.444444, 0.666667},
  {0.087791, 0.296296},
  {0.444444, 0.666667},
  {0.444444, 0.666667},
  {0.444444, 0.666667},
  {0.023320, 0.152708},
  {0.162209, 0.402751},
  {0.058813, 0.242515},
  {0.388889, 0.623610},
  {0.388889, 0.623610},
  {0.388889, 0.623610},
  {0.003687, 0.060717},
  {0.114798, 0.338818},
  {0.281464, 0.530532},
  {0.037037, 0.192450},
  {0.333333, 0.577350},
  {0.333333, 0.577350},
  {0.333333, 0.577350},
  {0.074074, 0.272166},
  {0.212963, 0.461479},
  {0.407407, 0.638285},
  {0.041067, 0.202649},
  {0.152178, 0.390100},
  {0.318844, 0.564663},
  {0.541067, 0.735572},
  {0.021433, 0.146402},
  {0.277778, 0.527046},
  {0.277778, 0.527046},
  {0.277778, 0.527046},
  {0.015480, 0.124420},
  {0.079138, 0.281314},
  {0.174045, 0.417187},
  {0.001049, 0.032387},
  {0.046477, 0.215586},
  {0.123155, 0.350935},
  {0.231084, 0.480712},
  {0.021991, 0.148293},
  {0.080440, 0.283619},
  {0.170139, 0.412479},
  {0.291088, 0.539526},
  {0.046332, 0.215250},
  {0.117802, 0.343224},
  {0.220522, 0.469598},
  {0.354492, 0.595392},
  {0.026440, 0.162602},
  {0.085033, 0.291605},
  {0.174877, 0.418183},
  {0.295971, 0.544032},
  {0.046721, 0.216151},
  {0.117034, 0.342102},
  {0.218596, 0.467543},
  {0.351409, 0.592797},
  {0.070312, 0.265165},
  {0.152344, 0.390312},
  {0.265625, 0.515388},
  {0.410156, 0.640434},
  {0.097647, 0.312486},
  {0.191397, 0.437490},
  {0.316397, 0.562492},
  {0.472647, 0.687493},
  {0.017407, 0.131937},
  {0.054815, 0.234126},
  {0.112222, 0.334996},
  {0.189630, 0.435465},
  {0.028556, 0.168984},
  {0.072630, 0.269499},
  {0.136704, 0.369735},
  {0.220778, 0.469870},
  {0.041407, 0.203488},
  {0.092148, 0.303559},
  {0.162889, 0.403595},
  {0.253630, 0.503617},
  {0.056185, 0.237034},
  {0.113593, 0.337035},
  {0.191000, 0.437035},
  {0.288407, 0.537036},
  {0.033837, 0.183948},
  {0.080637, 0.283967},
  {0.147437, 0.383975},
  {0.234237, 0.483980},
  {0.045796, 0.214001},
  {0.098596, 0.314000},
  {0.171396, 0.414000},
  {0.264196, 0.514000},
  {0.059600, 0.244131},
  {0.118400, 0.344093},
  {0.197200, 0.444072},
  {0.296000, 0.544059},
  {0.075470, 0.274719},
  {0.140270, 0.374527},
  {0.225070, 0.474416},
  {0.329870, 0.574343}
};
unsigned long sQrt_LkUpTbl_addr = 0x1cc8;

struct Pair aCos_LkUpTbl[ACOSCNT] = {
  {-0.941115, 2.796710},
  {0.498908, 1.048458},
  {0.201034, 1.368383},
  {-0.096840, 1.667788},
  {-0.394713, 1.976552},
  {0.378967, 1.182116},
  {0.040405, 1.530381},
  {-0.298158, 1.873559},
  {-0.636721, 2.261035},
  {0.219560, 1.349433},
  {-0.169879, 1.741503},
  {-0.559318, 2.164359},
  {-0.948757, 2.820075},
  {0.003740, 1.567056},
  {-0.450728, 2.038377},
  {-0.905197, 2.702640},
  {0.000000, 1.570796},
  {-0.562500, 2.168203},
  {-0.343622, 1.921567},
  {-0.866025, 2.617994},
  {-0.458530, 2.047137}
};
unsigned long aCos_LkUpTbl_addr = 0x26f8;

struct Pair cos_LkUpTbl[COSCNT] = {
  {0.932237, 0.596040},
  {3.026632, -0.993399},
  {5.121027, 0.397360},
  {0.349486, 0.939549},
  {2.443881, -0.766314},
  {4.538276, -0.173234},
  {0.456128, 0.897765},
  {2.550523, -0.830345},
  {4.644918, -0.067420},
  {0.555929, 0.849410},
  {2.650324, -0.881735},
  {4.744720, 0.032325},
  {0.658851, 0.790696},
  {2.753246, -0.925536},
  {4.847641, 0.134840},
  {0.394039, 0.923366},
  {2.488434, -0.794168},
  {4.582829, -0.129198},
  {0.510127, 0.872683},
  {2.604522, -0.859211},
  {4.698917, -0.013471},
  {0.624520, 0.811244},
  {2.718915, -0.911994},
  {4.813310, 0.100750},
  {0.753678, 0.729177},
  {2.848073, -0.957232},
  {4.942468, 0.228055},
  {0.449811, 0.900529},
  {2.544206, -0.826808},
  {4.638601, -0.073721},
  {0.580501, 0.836188},
  {2.674896, -0.893060},
  {4.769291, 0.056872},
  {0.721453, 0.750847},
  {2.815848, -0.947413},
  {4.910243, 0.196566},
  {0.940025, 0.589768},
  {3.034420, -0.994263},
  {5.128815, 0.404495},
  {0.522352, 0.866648},
  {2.616747, -0.865401},
  {4.711142, -0.001247},
  {0.679459, 0.777913},
  {2.773854, -0.933143},
  {4.868249, 0.155230},
  {0.900880, 0.620920},
  {2.995275, -0.989315},
  {5.089670, 0.368394},
  {0.523599, 0.866025},
  {2.617994, -0.866025},
  {4.712389, -0.000000},
  {0.722734, 0.750000},
  {2.817129, -0.947822},
  {4.911524, 0.197822},
  {0.640522, 0.801784},
  {2.734917, -0.918441},
  {4.829313, 0.116657},
  {0.872665, 0.642788},
  {2.967060, -0.984808},
  {5.061455, 0.342020},
  {0.682379, 0.776075},
  {2.776774, -0.934189},
  {4.871169, 0.158114}
};
unsigned long cos_LkUpTbl_addr = 0x2848;

struct Pair1 pow_LkUpTbl[POWCNT] = {
  {14.082273, 0.333333, 2.414854},
  {19.457121, 0.333333, 2.689632},
  {170.099829, 0.333333, 5.540742},
  {0.836475, 0.333333, 0.942217},
  {0.486041, 0.333333, 0.786244},
  {0.902751, 0.333333, 0.966472},
  {0.310717, 0.333333, 0.677311},
  {0.755485, 0.333333, 0.910770},
  {1.113865, 0.333333, 1.036599},
  {0.605499, 0.333333, 0.846001},
  {0.961479, 0.333333, 0.986991},
  {1.304951, 0.333333, 1.092777},
  {0.452649, 0.333333, 0.767810},
  {0.806766, 0.333333, 0.930928},
  {1.147996, 0.333333, 1.047081},
  {1.485572, 0.333333, 1.141032},
  {0.316550, 0.333333, 0.681523},
  {0.598444, 0.333333, 0.842703},
  {0.859317, 0.333333, 0.950717},
  {0.151600, 0.333333, 0.533211},
  {0.459799, 0.333333, 0.771832},
  {0.720148, 0.333333, 0.896342},
  {0.974925, 0.333333, 0.991571},
  {0.319589, 0.333333, 0.683697},
  {0.579915, 0.333333, 0.833915},
  {0.833775, 0.333333, 0.941202},
  {1.085822, 0.333333, 1.027826},
  {0.438629, 0.333333, 0.759800},
  {0.691603, 0.333333, 0.884339},
  {0.942978, 0.333333, 0.980619},
  {1.193772, 0.333333, 1.060817},
  {0.334477, 0.333333, 0.694154},
  {0.588480, 0.333333, 0.838000},
  {0.840058, 0.333333, 0.943561},
  {1.090907, 0.333333, 1.029428},
  {0.434901, 0.333333, 0.757641},
  {0.685852, 0.333333, 0.881881},
  {0.936293, 0.333333, 0.978297},
  {1.186547, 0.333333, 1.058673},
  {0.530790, 0.333333, 0.809669},
  {0.780937, 0.333333, 0.920885},
  {1.031013, 0.333333, 1.010233},
  {1.281059, 0.333333, 1.086067},
  {0.624986, 0.333333, 0.854981},
  {0.874990, 0.333333, 0.956462},
  {1.124992, 0.333333, 1.040039},
  {1.374993, 0.333333, 1.111988},
  {0.268974, 0.333333, 0.645511},
  {0.471163, 0.333333, 0.778139},
  {0.672033, 0.333333, 0.875918},
  {0.872502, 0.333333, 0.955554},
  {0.339354, 0.333333, 0.697511},
  {0.539869, 0.333333, 0.814260},
  {0.740105, 0.333333, 0.904547},
  {0.940240, 0.333333, 0.979670},
  {0.407192, 0.333333, 0.741196},
  {0.607263, 0.333333, 0.846822},
  {0.807299, 0.333333, 0.931132},
  {1.007320, 0.333333, 1.002434},
  {0.474071, 0.333333, 0.779736},
  {0.674072, 0.333333, 0.876803},
  {0.874073, 0.333333, 0.956128},
  {1.074073, 0.333333, 1.024105},
  {0.367948, 0.333333, 0.716576},
  {0.567967, 0.333333, 0.828147},
  {0.767975, 0.333333, 0.915762},
  {0.967980, 0.333333, 0.989211},
  {0.428001, 0.333333, 0.753613},
  {0.628000, 0.333333, 0.856354},
  {0.828000, 0.333333, 0.939024},
  {1.028000, 0.333333, 1.009248},
  {0.488131, 0.333333, 0.787370},
  {0.688093, 0.333333, 0.882841},
  {0.888072, 0.333333, 0.961205},
  {1.088059, 0.333333, 1.028531},
  {0.548719, 0.333333, 0.818685},
  {0.748527, 0.333333, 0.907965},
  {0.948416, 0.333333, 0.982501},
  {1.148343, 0.333333, 1.047186}
};
unsigned long pow_LkUpTbl_addr = 0x2c38;


long double  sqrt (long double in) {
  uintptr_t ivtmp_32;
  long double rValue;
  unsigned int i;
  long double D_2171;

sqrtbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
SP = SP + 0x28;
// Simulating I Cache for obj block 0
memAccessCycles += simICache(0xb40, 28);
pipelineCycles += 23 - (enterBlock(0x2f0, 0x2f6) ? 7 : 0);
  ivtmp_32 = (uintptr_t)&sQrt_LkUpTbl[0].input;
  i = 0;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

sqrtbb_3:
//  # PRED: 6 [99.0%]  (true,exec) 2 [100.0%]  (fallthru,exec)
// Simulating I Cache for obj block 1
memAccessCycles += simICache(0xb5c, 48);
pipelineCycles += 15 - (enterBlock(0x2f7, 0x302) ? 7 : 0);
  D_2171 = *(long double*)((uintptr_t)ivtmp_32);
  if (D_2171 + 2.00000000000000004163336342344337026588618755341e-3 >= in != 0)
    goto sqrtbb_4;
  else
    goto sqrtbb_6;
//  # SUCC: 4 [50.0%]  (true,exec) 6 [50.0%]  (false,exec)

sqrtbb_4:
//  # PRED: 3 [50.0%]  (true,exec)
// Simulating I Cache for obj block 2
memAccessCycles += simICache(0xb8c, 56);
pipelineCycles += 16 - (enterBlock(0x303, 0x310) ? 7 : 0);
  if (D_2171 - 2.00000000000000004163336342344337026588618755341e-3 < in != 0)
    goto sqrtbb_5;
  else
    goto sqrtbb_6;
//  # SUCC: 5 [4.5%]  (true,exec) 6 [95.5%]  (false,exec)

sqrtbb_5:
//  # PRED: 4 [4.5%]  (true,exec)
pipelineCycles += 17 - (enterBlock(0x317, 0x318) ? 7 : 0);
  rValue = sQrt_LkUpTbl[i].output;
  goto sqrtbb_7;
//  # SUCC: 7 [100.0%]  (fallthru,exec)

sqrtbb_6:
//  # PRED: 3 [50.0%]  (false,exec) 4 [95.5%]  (false,exec)
// Simulating I Cache for obj block 3
memAccessCycles += simICache(0xbc4, 16);
pipelineCycles += 9 - (enterBlock(0x311, 0x314) ? 7 : 0);
  i = i + 1;
  ivtmp_32 = ivtmp_32 + 16;
  if (i != 163)
    goto sqrtbb_3;
  else
    goto sqrtbb_8;
//  # SUCC: 3 [99.0%]  (true,exec) 8 [1.0%]  (false,exec)

sqrtbb_8:
//  # PRED: 6 [1.0%]  (false,exec)
// Simulating I Cache for obj block 4
memAccessCycles += simICache(0xbd4, 8);
pipelineCycles += 9 - (enterBlock(0x315, 0x316) ? 7 : 0);
  rValue = 0.0;
//  # SUCC: 7 [100.0%]  (fallthru)

sqrtbb_7:
//  # PRED: 5 [100.0%]  (fallthru,exec) 8 [100.0%]  (fallthru)
// Simulating I Cache for obj block 5
memAccessCycles += simICache(0xbdc, 8);
  return rValue;
//  # SUCC: EXIT [100.0%] 

}



long double  acos (long double in) {
  uintptr_t ivtmp_64;
  long double rValue;
  unsigned int i;
  long double D_2190;

acosbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
SP = SP + 0x28;
// Simulating I Cache for obj block 0
memAccessCycles += simICache(0xbf8, 28);
pipelineCycles += 23 - (enterBlock(0x320, 0x326) ? 7 : 0);
  ivtmp_64 = (uintptr_t)&aCos_LkUpTbl[0].input;
  i = 0;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

acosbb_3:
//  # PRED: 6 [95.5%]  (true,exec) 2 [100.0%]  (fallthru,exec)
// Simulating I Cache for obj block 1
memAccessCycles += simICache(0xc14, 48);
pipelineCycles += 15 - (enterBlock(0x327, 0x332) ? 7 : 0);
  D_2190 = *(long double*)((uintptr_t)ivtmp_64);
  if (D_2190 + 2.00000000000000004163336342344337026588618755341e-3 >= in != 0)
    goto acosbb_4;
  else
    goto acosbb_6;
//  # SUCC: 4 [50.0%]  (true,exec) 6 [50.0%]  (false,exec)

acosbb_4:
//  # PRED: 3 [50.0%]  (true,exec)
// Simulating I Cache for obj block 2
memAccessCycles += simICache(0xc44, 56);
pipelineCycles += 16 - (enterBlock(0x333, 0x340) ? 7 : 0);
  if (D_2190 - 2.00000000000000004163336342344337026588618755341e-3 < in != 0)
    goto acosbb_5;
  else
    goto acosbb_6;
//  # SUCC: 5 [4.5%]  (true,exec) 6 [95.5%]  (false,exec)

acosbb_5:
//  # PRED: 4 [4.5%]  (true,exec)
pipelineCycles += 17 - (enterBlock(0x347, 0x348) ? 7 : 0);
  rValue = aCos_LkUpTbl[i].output;
  goto acosbb_7;
//  # SUCC: 7 [100.0%]  (fallthru,exec)

acosbb_6:
//  # PRED: 3 [50.0%]  (false,exec) 4 [95.5%]  (false,exec)
// Simulating I Cache for obj block 3
memAccessCycles += simICache(0xc7c, 16);
pipelineCycles += 9 - (enterBlock(0x341, 0x344) ? 7 : 0);
  i = i + 1;
  ivtmp_64 = ivtmp_64 + 16;
  if (i != 21)
    goto acosbb_3;
  else
    goto acosbb_8;
//  # SUCC: 3 [95.5%]  (true,exec) 8 [4.5%]  (false,exec)

acosbb_8:
//  # PRED: 6 [4.5%]  (false,exec)
// Simulating I Cache for obj block 4
memAccessCycles += simICache(0xc8c, 8);
pipelineCycles += 9 - (enterBlock(0x345, 0x346) ? 7 : 0);
  rValue = 0.0;
//  # SUCC: 7 [100.0%]  (fallthru)

acosbb_7:
//  # PRED: 5 [100.0%]  (fallthru,exec) 8 [100.0%]  (fallthru)
// Simulating I Cache for obj block 5
memAccessCycles += simICache(0xc94, 8);
  return rValue;
//  # SUCC: EXIT [100.0%] 

}



long double  cos (long double in) {
  uintptr_t ivtmp_95;
  long double rValue;
  unsigned int i;
  long double D_2209;

cosbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
SP = SP + 0x28;
// Simulating I Cache for obj block 0
memAccessCycles += simICache(0xcb0, 28);
pipelineCycles += 23 - (enterBlock(0x350, 0x356) ? 7 : 0);
  ivtmp_95 = (uintptr_t)&cos_LkUpTbl[0].input;
  i = 0;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

cosbb_3:
//  # PRED: 6 [98.4%]  (true,exec) 2 [100.0%]  (fallthru,exec)
// Simulating I Cache for obj block 1
memAccessCycles += simICache(0xccc, 48);
pipelineCycles += 15 - (enterBlock(0x357, 0x362) ? 7 : 0);
  D_2209 = *(long double*)((uintptr_t)ivtmp_95);
  if (D_2209 + 2.00000000000000004163336342344337026588618755341e-3 >= in != 0)
    goto cosbb_4;
  else
    goto cosbb_6;
//  # SUCC: 4 [50.0%]  (true,exec) 6 [50.0%]  (false,exec)

cosbb_4:
//  # PRED: 3 [50.0%]  (true,exec)
// Simulating I Cache for obj block 2
memAccessCycles += simICache(0xcfc, 56);
pipelineCycles += 16 - (enterBlock(0x363, 0x370) ? 7 : 0);
  if (D_2209 - 2.00000000000000004163336342344337026588618755341e-3 < in != 0)
    goto cosbb_5;
  else
    goto cosbb_6;
//  # SUCC: 5 [4.5%]  (true,exec) 6 [95.5%]  (false,exec)

cosbb_5:
//  # PRED: 4 [4.5%]  (true,exec)
pipelineCycles += 17 - (enterBlock(0x377, 0x378) ? 7 : 0);
  rValue = cos_LkUpTbl[i].output;
  goto cosbb_7;
//  # SUCC: 7 [100.0%]  (fallthru,exec)

cosbb_6:
//  # PRED: 3 [50.0%]  (false,exec) 4 [95.5%]  (false,exec)
// Simulating I Cache for obj block 3
memAccessCycles += simICache(0xd34, 16);
pipelineCycles += 9 - (enterBlock(0x371, 0x374) ? 7 : 0);
  i = i + 1;
  ivtmp_95 = ivtmp_95 + 16;
  if (i != 63)
    goto cosbb_3;
  else
    goto cosbb_8;
//  # SUCC: 3 [98.4%]  (true,exec) 8 [1.6%]  (false,exec)

cosbb_8:
//  # PRED: 6 [1.6%]  (false,exec)
// Simulating I Cache for obj block 4
memAccessCycles += simICache(0xd44, 8);
pipelineCycles += 9 - (enterBlock(0x375, 0x376) ? 7 : 0);
  rValue = 0.0;
//  # SUCC: 7 [100.0%]  (fallthru)

cosbb_7:
//  # PRED: 5 [100.0%]  (fallthru,exec) 8 [100.0%]  (fallthru)
// Simulating I Cache for obj block 5
memAccessCycles += simICache(0xd4c, 8);
  return rValue;
//  # SUCC: EXIT [100.0%] 

}



long double  pow (long double in1, long double in2) {
  uintptr_t ivtmp_126;
  long double rValue;
  unsigned int i;
  long double D_2238;
  long double D_2229;

powbb_2:
//  # PRED: ENTRY [100.0%]  (fallthru,exec)
SP = SP + 0x30;
// Simulating I Cache for obj block 0
memAccessCycles += simICache(0xd68, 36);
pipelineCycles += 24 - (enterBlock(0x380, 0x388) ? 7 : 0);
  ivtmp_126 = (uintptr_t)&pow_LkUpTbl[0].input1;
  i = 0;
//  # SUCC: 3 [100.0%]  (fallthru,exec)

powbb_3:
//  # PRED: 8 [98.8%]  (true,exec) 2 [100.0%]  (fallthru,exec)
// Simulating I Cache for obj block 1
memAccessCycles += simICache(0xd8c, 44);
pipelineCycles += 14 - (enterBlock(0x389, 0x393) ? 7 : 0);
  D_2229 = *(long double*)((uintptr_t)ivtmp_126);
  if (D_2229 + 2.00000000000000004163336342344337026588618755341e-3 >= in1 != 0)
    goto powbb_4;
  else
    goto powbb_8;
//  # SUCC: 4 [50.0%]  (true,exec) 8 [50.0%]  (false,exec)

powbb_4:
//  # PRED: 3 [50.0%]  (true,exec)
// Simulating I Cache for obj block 2
memAccessCycles += simICache(0xdb8, 40);
pipelineCycles += 13 - (enterBlock(0x394, 0x39d) ? 7 : 0);
  if (D_2229 - 2.00000000000000004163336342344337026588618755341e-3 < in1 != 0)
    goto powbb_5;
  else
    goto powbb_8;
//  # SUCC: 5 [50.0%]  (true,exec) 8 [50.0%]  (false,exec)

powbb_5:
//  # PRED: 4 [50.0%]  (true,exec)
// Simulating I Cache for obj block 3
memAccessCycles += simICache(0xde0, 44);
pipelineCycles += 14 - (enterBlock(0x39e, 0x3a8) ? 7 : 0);
  D_2238 = *(long double*)((uintptr_t)ivtmp_126 + 8);
  if (D_2238 + 2.00000000000000004163336342344337026588618755341e-3 >= in2 != 0)
    goto powbb_6;
  else
    goto powbb_8;
//  # SUCC: 6 [50.0%]  (true,exec) 8 [50.0%]  (false,exec)

powbb_6:
//  # PRED: 5 [50.0%]  (true,exec)
// Simulating I Cache for obj block 4
memAccessCycles += simICache(0xe0c, 36);
pipelineCycles += 12 - (enterBlock(0x3a9, 0x3b1) ? 7 : 0);
  if (D_2238 - 2.00000000000000004163336342344337026588618755341e-3 < in2 != 0)
    goto powbb_7;
  else
    goto powbb_8;
//  # SUCC: 7 [4.5%]  (true,exec) 8 [95.5%]  (false,exec)

powbb_7:
//  # PRED: 6 [4.5%]  (true,exec)
// Simulating I Cache for obj block 5
memAccessCycles += simICache(0xe30, 24);
pipelineCycles += 11 - (enterBlock(0x3b2, 0x3b7) ? 7 : 0);
  rValue = pow_LkUpTbl[i].output;
  goto powbb_9;
//  # SUCC: 9 [100.0%]  (fallthru,exec)

powbb_8:
//  # PRED: 3 [50.0%]  (false,exec) 4 [50.0%]  (false,exec) 5 [50.0%]  (false,exec) 6 [95.5%]  (false,exec)
// Simulating I Cache for obj block 6
memAccessCycles += simICache(0xe48, 16);
pipelineCycles += 9 - (enterBlock(0x3b8, 0x3bb) ? 7 : 0);
  i = i + 1;
  ivtmp_126 = ivtmp_126 + 24;
  if (i != 79)
    goto powbb_3;
  else
    goto powbb_10;
//  # SUCC: 3 [98.8%]  (true,exec) 10 [1.2%]  (false,exec)

powbb_10:
//  # PRED: 8 [1.2%]  (false,exec)
// Simulating I Cache for obj block 7
memAccessCycles += simICache(0xe58, 8);
pipelineCycles += 9 - (enterBlock(0x3bc, 0x3bd) ? 7 : 0);
  rValue = 0.0;
//  # SUCC: 9 [100.0%]  (fallthru)

powbb_9:
//  # PRED: 7 [100.0%]  (fallthru,exec) 10 [100.0%]  (fallthru)
// Simulating I Cache for obj block 8
memAccessCycles += simICache(0xe60, 12);
pipelineCycles += 17 - (enterBlock(0x3be, 0x3c0) ? 7 : 0);
  return rValue;
//  # SUCC: EXIT [100.0%] 

}


