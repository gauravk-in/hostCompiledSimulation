

#define FIB_MAX_NUM 15

int a=0, b=1;
int i;

int main(int argc, char* argv)
{
	int b_tmp;

	for(i=3; i<=100; i++)
	{
		b_tmp = b;
		b = a + b;
		a = b_tmp;
	}

	// printf("%dth Fibonacci Number is %d\n", i-1, b);

	return b;
}
