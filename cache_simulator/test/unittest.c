#include <stdio.h>

#define ADDRESS_LEN_BITS 32

int log_base2(int val)
{
	int ret = 0;
	while (val >>= 1) ++ret;
	return ret;
}

inline unsigned long getTagFromAddress(unsigned long address,
		unsigned int tagLengthBits, unsigned long tagMask)
{
	return (address & tagMask) >> (ADDRESS_LEN_BITS - tagLengthBits);
}

inline unsigned long getIndexFromAddress(unsigned long address,
		unsigned int offsetLengthBits, unsigned long indexMask)
{

	return (address & indexMask) >> offsetLengthBits;
}


void main()
{
	unsigned long address = 0x12345678;
	unsigned long tag;
	unsigned long index;
	int i;
	unsigned long indexMask;

	indexMask = 0;
	for (i = 0; i < 8; i++)
	{
		indexMask = indexMask << 1;
		indexMask |= 0x00000001;
	}
	indexMask = indexMask << log_base2(16);

	tag = getTagFromAddress(address, 20, 0xFFFFF000);
	index = getIndexFromAddress(address, 4, indexMask);

	printf("log_base2(16) = %d\n", log_base2(16));
	printf("IndexMask = %lx\n", indexMask);
	printf("Tag = %lx\n", tag);
	printf("Index = %lx\n", index);

}
