# CS353 Project 1 

姓名：彭嘉淇

学号：519030910229

## 实验一 

1. 编写模块实现以下要求
   接受三个参数： operand1 类型为 int， operand2 类型为 int 数组， operator 类型为 charp（字符串）。
   创建 proc ⽂件 /proc/<你的学号>/calc 。
   如果 operator 为 add，那么 operand2 的每⼀个元素都加上 operand1 ，得到结果数组；如果oerator 为 mul，那么 operand2 的每⼀个元素都乘上 operand1 ，得到结果数组。
   当读取 proc ⽂件时，输出结果数组，每个元素⽤逗号分隔。
   当⽤户向 proc ⽂件写⼊⼀个数字时，这个数字作为新的 operand1 重新进⾏计算。

1、实验过程：

实验环境：ubuntu20.04、linux 5.13.0-37

下载代码模板

```git
git clone https://github.com/chengjiagan/CS353-2022-Spring.git
```

查阅ppt，找到实现上述功能的对应函数

```c
module_param(test, int, 0644); // 传递参数
proc_create //创建文件
proc_mkdir //创建目录
procfile_read //读取函数
procfile_write //写入函数
copy_from_user //数据从内核区拷贝到用户区
```

函数说明：

| 函数名     | 功能                                                         |
| ---------- | ------------------------------------------------------------ |
| proc_init  | 创建文件夹并在其文件夹下创建文件                             |
| proc_exit  | 删除文件夹以及文件                                           |
| proc_read  | 定义读取函数，对定义的操作及操作数进行计算，将结果存储到缓存区 |
| proc_write | 读取用户缓存区，并赋值给操作数1                              |

2、实验结果

![image-20220328200831790](../../source/images/CS353 Project 1/image-20220328200831790.png)

3、实验心得

$\bullet$ 在上手前多阅读相关文档，参考[The Linux Kernel Module Programming Guide (sysprog21.github.io)](https://sysprog21.github.io/lkmpg/#the-proc-file-system)编写。最初在做实验时，在linux5.4的环境，编译时显示"proc_fs.h"找不到，只好烦请助教同学答疑解惑，经提醒后改到linux5.13版本，终于编译成功。

![image-20220328201228893](../../source/images/CS353 Project 1/image-20220328201228893.png)

$\bullet$ 做实验时经常混淆用户态和内存态的缓存区，不知道在读时还是写时做相应操作，后来把老师给的相关示例弄懂，并上网查找资料，终于明白了。





## 实验二

2. 编写⼀个程序实现以下要求：
   从 /proc ⽂件系统中得到系统中的所有进程 PID 以及相关信息。
   输出这些进程的 PID，进程状态，进程的命令⾏参数三列信息。
   PID 5字符宽度，右对⻬，空格填补空缺；每列信息之间⽤⼀个空格分隔。
   输出效果可以参考命令 ps -e -ww -o pid:5,state,cmd 的输出效果。  

1、实验过程

实验环境：ubuntu20.04、linux 5.13.0-37

下载代码模板

```git
git clone https://github.com/chengjiagan/CS353-2022-Spring.git
```

在ps.c文件中编写代码。

查阅ppt，在proc文件系统中找到包含对应信息的文件，参考[proc(5) - Linux manual page (man7.org)](https://man7.org/linux/man-pages/man5/proc.5.html)了解 proc 中各个⽂件的作用。

在/proc文件夹下查找数字文件名的进程文件，需要的 proc ⽂件有 proc/<PID>/cmdline 和 /proc/PID/stat 。对于部分进程，其cmdline ⽂件为空，此时可输出 /proc/<PID>/comm ⽂件中的内容。  

2、实验结果

本实验程序结果

![image-20220328205944969](../../source/images/CS353 Project 1/image-20220328205944969.png)

运行一下命令后的结果，可见与上图几乎一致

```
ps -e -ww -o pid:5,state,cmd
```

![image-20220328205743202](../../source/images/CS353 Project 1/image-20220328205743202.png)

3、实验心得

$\bull$ 用C语言编写程序经常会遇到指针使用的问题，例如在编写程序时想对字符串进行拼接，最初采用strcat的方法，经常报错，但是采用sprintf的方式可以很方便地进行赋值，甚至还可以很好地将数字等其他类型的变量转成字符串。

```c
sprintf(stat_path, "/proc/%s/stat", entry->d_name);
```

$\bull$ 通过从底层实现ps命令，使我对/proc文件系统的理解更深了一层，以后查看系统状态时可以方便地从proc文件目录中获取相关信息。

$\bull$ 成功运行一遍程序后，时过一日再运行自己的程序时发现相关文件找不到，最后发现原来是实验一的模块没有卸载，proc的进程文件夹下没有对应的stat等文件。这是实验中值得注意的地方，在运行实验二时记得卸载实验一的模块。