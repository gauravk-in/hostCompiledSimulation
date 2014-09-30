

#include <stdio.h>
#include "test_data_8192_32k.h"
#include "test_data_131072_512k.h"

void half_fill_L1_DCache()
{
	unsigned long i;
	unsigned long long sum = 0;

	for (i = 0; i < 4096; i++)
	{
		sum += data_131072[i];
	}

	printf("fill_L1_DCache : Sum (8192) = %llu\n", sum);
}

void fill_L1_DCache()
{
	unsigned long i;
	unsigned long long sum = 0;

	for (i = 0; i < 8192; i++)
	{
		sum += data_8192[i];
	}

	printf("fill_L1_DCache : Sum (8192) = %llu\n", sum);
}

void fill_L2_Cache()
{
	unsigned long i;
	unsigned long long sum = 0;

	for (i = 0; i < 131072; i++)
	{
		sum += data_131072[i];
	}

	printf("fill_L1_DCache : Sum (131072) = %llu\n", sum);
}

void fill_L1_read_again()
{
	unsigned long i;
	unsigned long long sum = 0;

	for (i = 0; i < 8192; i++)
	{
		sum += data_8192[i];
	}

	printf("fill_L1_DCache : Sum (8192) = %llu\n", sum);

	sum = 0;
	for (i = 0; i <= 8192; i++)
	{
		sum += data_8192[i];
	}

	printf("fill_L1_DCache : Sum (8192) = %llu\n", sum);
}
