#include <cstdint>
#include <stdio.h>
#include <stdlib.h>

#define SIZE 32

void print_bits(uint32_t num)
{
	for (int i = SIZE - 1; i >= 0; i--)
    {
        printf("%u", (num >> i) & 0b1);
    }
    printf("\n");	
}

uint32_t set_bit(uint32_t num, int n, int b)
{
	if (n < 0 || n >= SIZE || (b != 0 && b != 1))
    {
        printf("Invalid values\n");
        exit(-1);
    }
	if (b == 1)
		return num | (0b1 << n);
	return num & ~(0b1 << n);
}

uint32_t get_bit(uint32_t num, int n) {
	if (n < 0 || n >= 32)
    {
        printf("get_bit: Invalid values\n");
        exit(-1);
    }
    return (num >> n) & 0b1;
}

uint32_t adder(uint32_t a, uint32_t b)
{
	uint32_t res = 0;
	int carry_over = 0;

	int a_saved = a;
	int b_saved = b;
	
	for (int i = 0; i < SIZE; i++)
	{
		// resove carry over from last digit
		if (carry_over)
		{
			// save current bit of value
			int curr_bit_a_tmp = get_bit(a, i);

			// mutate XOR A curret digit to carry out carryover
			a = set_bit(a, i, (curr_bit_a_tmp ^ 0b1));

			// check if saved A needa to carry over using AND. If no, set to 0
			if (!(curr_bit_a_tmp & 0b1))
				carry_over = 0;
		}

		// XOR A and B together, this will be current bit result of res
		uint32_t curr_bit_a = get_bit(a, i);
		uint32_t curr_bit_b = get_bit(b, i);
		res = set_bit(res, i, (curr_bit_a ^ curr_bit_b));

		// if carry flag is tripped here, continue.
		if (carry_over)
			continue;

		// check if A and B current digit needs to carry over using AND. If yes, trip the carry over flag. else continue
		if (curr_bit_a & curr_bit_b)
			carry_over = 0b1;

	}

	// print_bits(a_saved);
	// print_bits(b_saved);
	// print_bits(res);
	return res;
}