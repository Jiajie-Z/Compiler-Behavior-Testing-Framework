#include <stdio.h>

int main(void) {
    int *p = NULL;
    /* Likely runtime crash */
    printf("%d\n", *p);
    return 0;
}