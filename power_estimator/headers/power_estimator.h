/**
 * Power Estimator:
 *
 * Objective: API to call power estimation.
 *
 * Description: The power estimator, takes as input some trace statistics over a
 * period of time, and generates the amount of energy used over the period.
 */

extern double estimate_power(char *blockName,
		unsigned long long execCycles,
		unsigned long long memAccessCycles,
		unsigned long long L2_Hits,
		unsigned long long memAccesses);

extern void power_estimator_init();

extern void power_estimator_fini();
