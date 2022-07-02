#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sched.h>
#include <unistd.h>

void run(int n) {
    cpu_set_t mask;
    CPU_ZERO(&mask);
    CPU_SET(n, &mask);
    sched_setaffinity(0, sizeof(cpu_set_t), &mask);
    
    while(1){}
    exit(0);
}

int main(void)
{
    pid_t pid;
    printf("this is a task1 code\n");
    int i = 0, n = 1;

    for (i = 0; i < n; i++) {
        pid = fork();
        if (pid == 0) {
            break;
        }
    }

    if (i < n) {
    	run(0);
    }
    return 0;
}


