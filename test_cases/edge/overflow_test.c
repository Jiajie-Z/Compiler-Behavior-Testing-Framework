#include <stdio.h>
#include <limits.h>

int main(void) {
    int x = INT_MAX;
    int y = x + 1; /* signed overflow: undefined behavior */
    printf("overflow_result=%d\n", y);
    return 0;
}