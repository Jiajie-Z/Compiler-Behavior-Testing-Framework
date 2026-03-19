#include <stdio.h>

int fact(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * fact(n - 1);
}

int main(void) {
    printf("fact=%d\n", fact(5));
    return 0;
}