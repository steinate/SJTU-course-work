obj-m += maptest.o
all: kmod maptest_test
maptest_test: maptest_test.c
	gcc -Werror -Wall -o maptest_test maptest_test.c
kmod:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
