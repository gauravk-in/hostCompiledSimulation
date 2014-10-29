/**
 * Power Estimator:
 *
 * Objective: API to call power estimation.
 *
 * Description: The power estimator, takes as input some trace statistics over a
 * period of time, and generates the amount of energy used over the period.
 */

extern double estimate_power(unsigned long long execCycles,
		unsigned long L1_Hits,
		unsigned long L2_Hits,
		unsigned long L2_Misses);
