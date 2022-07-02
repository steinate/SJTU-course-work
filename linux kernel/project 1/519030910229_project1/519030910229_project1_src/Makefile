obj-m += calc.o
all: calc ps
ps: ps.c
	gcc ps.c -o ps
calc:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
	rm ps
