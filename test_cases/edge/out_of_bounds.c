#include <stdio.h>

int main(void) {
    int arr[3] = {1, 2, 3};
    /* Out-of-bounds read: undefined behavior */
    printf("oob_value=%d\n", arr[5]);
    return 0;
}