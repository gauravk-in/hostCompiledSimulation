#include "test_memory.h"

int main()
{
	fill_L1_DCache();

	fill_L2_Cache();

	fill_L1_read_again();

	return 0;
}
