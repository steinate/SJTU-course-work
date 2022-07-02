#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sched.h>
#include <unistd.h>


int main()
{
	int i, j;
	
	cpu_set_t mask;
    CPU_ZERO(&mask);
    CPU_SET(0, &mask);
    sched_setaffinity(0, sizeof(cpu_set_t), &mask);
	
	pid_t pid = getpid();
	struct sched_param param;
	param.sched_priority = sched_get_priority_max(SCHED_FIFO); 
	sched_setscheduler(pid, SCHED_RR, &param);           
	pthread_setschedparam(pthread_self(), SCHED_FIFO, &param);
	
	for(i=1;i<100000;i++){
	    for(j=1;j<5000000;j++){}
  	}
}
