#include <stdio.h>
#include "main.hpp"

int main(int argc, char const *argv[])
{
    int test_cases[][2] = {
        {0b01, 0b01},
        {0b10, 0b10},
        {0b11, 0b01},
        {0b11, 0b11},
        {0b101, 0b010},
        {0b1111, 0b0001},
        {0b1111, 0b1111},
        {0b0000, 0b0000},
        {0b1010, 0b0101}
    };

    int num_tests = sizeof(test_cases) / sizeof(test_cases[0]);

    for (int i = 0; i < num_tests; i++)
    {
        int a = test_cases[i][0];
        int b = test_cases[i][1];
        int res = adder(a, b);
        int expected = a + b;

        printf("\nTest Case %d\n", i + 1);

        printf("A:        ");
        print_bits(a);

        printf("B:        ");
        print_bits(b);

        printf("Result:   ");
        print_bits(res);

        printf("Expected: ");
        print_bits(expected);

        if (res == expected)
            printf("PASS\n");
        else
            printf("FAIL\n");
    }

    return 0;
}