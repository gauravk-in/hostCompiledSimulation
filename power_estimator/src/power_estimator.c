/**
 * Power Estimator:
 *
 * Objective: API to call power estimation.
 *
 * Description: The power estimator, takes as input some trace statistics over a
 * period of time, and generates the amount of energy used over the period.
 */
#include <stdio.h>

#define POWER_OUTPUT_FILE "power_trace.dat"

// Input Data from Target Hardware
double CPU_A_ABV = 131;
double CPU_C_ABV = 22.39;
double CPU_freq = 256;
double CPU_volt = 0.905;
double CPU_A_power;
double CPU_C_power;

double L2_A_ABV = 24.23925;
double L2_C_ABV = 8.652627;
double L2_freq = 128;
double L2_volt = 0.905;
double L2_A_power;
double L2_C_power;
unsigned int L2_Hit_Cycles = 8;

double MEM_A_ABV = 42.82 + 91.73 + 33.32 + 3.4;
double MEM_C_ABV = 26.21 + 64.38 + 16.39 + 3.4;
double MEM_freq = 400;
double MEM_volt = 1.2;
double MEM_A_power;
double MEM_C_power;
unsigned int MEM_Access_Cycles = 50;

FILE *output_fp;

unsigned long long totalCycles = 0;
unsigned long long prev_L2_Hits = 0;
unsigned long long prev_memAccesses = 0;

double totalEnergy = 0.0;

/**
 * @brief API to estimate the power
 *
 * @param Number of cycles spent in active state of CPU
 * @param Number of cycles spent in fetching data from memory
 * @param Number of L2 Hits Occured
 * @param Number of L2 Misses Occured
 *
 * @return Amount of Energy spent in the period of time in uJ.
 */
double estimate_power(char *blockName,
		unsigned long long execCycles,
		unsigned long long memAccessCycles,
		unsigned long long L2_Hits,
		unsigned long long memAccesses)
{
	unsigned long long startCycle;
	unsigned long long currBlock_L2_Hits;
	unsigned long long currBlock_memAccesses;
	double energy = 0.0;
	double power = 0.0;

	startCycle = totalCycles;
	totalCycles += execCycles + memAccessCycles;

	// CPU
	energy = CPU_A_power * execCycles / CPU_freq;
	energy += CPU_C_power * memAccessCycles / CPU_freq;

	// L2
	currBlock_L2_Hits = prev_L2_Hits - L2_Hits;
	energy += L2_A_power * currBlock_L2_Hits * L2_Hit_Cycles / L2_freq;
	energy += L2_C_power * (((totalCycles - startCycle) / CPU_freq) - (currBlock_L2_Hits * L2_Hit_Cycles / L2_freq));

	// MEM
	currBlock_memAccesses = prev_memAccesses - memAccesses;
	energy += MEM_A_power * currBlock_memAccesses * MEM_Access_Cycles / MEM_freq;
	energy += MEM_C_power * (((totalCycles - startCycle) / CPU_freq) - (currBlock_memAccesses * MEM_Access_Cycles / MEM_freq));

	totalEnergy += energy;
	power = energy / ((totalCycles - startCycle) / CPU_freq);

	fprintf(output_fp, "%s, %llu, %f, %llu, %llu, %lu, %lu\n",
			blockName, startCycles, power, execCycles, memAccessCycles,
			currBlock_L2_Hits, currBlock_memAccesses);

	return power;
}

void power_estimator_init()
{
	output_fp = fopen(POWER_OUTPUT_FILE, "w");

	CPU_A_power = CPU_A_ABV * CPU_volt * CPU_volt * CPU_freq;
	CPU_C_power = CPU_C_ABV * CPU_volt * CPU_volt * CPU_freq;

	L2_A_power = L2_A_ABV * L2_volt * L2_volt * L2_freq;
	L2_C_power = L2_C_ABV * L2_volt * L2_volt * L2_freq;

	MEM_A_power = MEM_A_ABV * MEM_volt * MEM_volt * MEM_freq;
	MEM_C_power = MEM_C_ABV * MEM_volt * MEM_volt * MEM_freq;
}

void power_estimator_fini()
{
	fclose(fp);
}
