obj-m += mtest.o
all: kmod mtest_test
mtest_test: mtest_test.c
	gcc -Werror -Wall -o mtest_test mtest_test.c
kmod:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
