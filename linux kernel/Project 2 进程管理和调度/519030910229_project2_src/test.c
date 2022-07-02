#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void run(int c, int n) {

    cpu_set_t mask;
    CPU_ZERO(&mask);
    CPU_SET(n, &mask);
    sched_setaffinity(0, sizeof(cpu_set_t), &mask);

    int i;
    for (i = 0; i != 10000; i++) {
        printf("%d-%d\n", c, sched_getcpu());
    }
}

int main()
{
    int i;
    for (i = 0; i != 20; i++) {
        int pid = fork();
        if (pid == 0) {
            run(i, i % 2);
            exit(0);
        }
    }
}
