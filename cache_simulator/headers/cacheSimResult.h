#ifndef CACHE_SIM_RESULT_H
#define CACHE_SIM_RESULT_H

struct csim_result_t
{
	unsigned long long latency;
	unsigned long long L1Hits;
	unsigned long long L2Hits;
	unsigned long long L2Misses;
	unsigned long long prefetches;
};

#endif // CACHE_SIM_RESULT_H
