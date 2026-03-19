#include <stdio.h>

int compute(int x) {
    if (x < 0) {
        return -1;
    } else if (x == 0) {
        return 0;
    } else {
        return x * 2;
    }
}

int main(void) {
    printf("result=%d\n", compute(5));
    return 0;
}