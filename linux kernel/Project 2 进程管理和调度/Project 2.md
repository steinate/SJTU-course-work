# Project 2  

## Task 1  

### 实验要求

1. 创建十个CPU-bound程序，并将他们绑定在同一个CPU核心上，修改这些进程(线程)的优先级使得其中5个进程占用大约70%的CPU资源，另外5个进程使用剩下的30%。在同一组中的进程应该具有相同的优先级，使用 top 或 htop 命令验证实验结果。

2. 在相同的CPU核心上，再创建一个实时进程，验证当这个进程在运行时，会抢占其他十个进程  

### 实验过程

1. 创建十个CPU-bound程序，并将他们绑定在同一个CPU核心上。

十个程序的创建可以用fork()分别生成十个子进程，让进程运行在指定的CPU上，即修改进程的CPU亲和力，有两种做法：

a. 通过taskset命令修改

```bash
taskset -c 0 ./test # -c参数代表要绑定的cpu核，./test代表要运行的程序
```

b. sched_setaffinity

`sched_setaffinity` 函数通过 `cpu_set_t` 结构体数据类型的掩码(mask)指定 cpu，掩码的操作可以通过一些宏定义实现，比如 `CPU_SET`等。操作哪一个线程则通过参数一`pid`指定，如果`pid==0`，那么为当前正在调用`sched_setaffinity` 函数的线程指定 cpu。

```c
cpu_set_t mask;
CPU_ZERO(&mask);
CPU_SET(n, &mask);
sched_setaffinity(0, sizeof(cpu_set_t), &mask);
```

经测试后者优先级大于前者，本实验中采用后者即sched_setaffinity。



2. 修改这些进程(线程)的优先级使得其中5个进程占用大约70%的CPU资源，另外5个进程使用剩下的30%。

CFS分配CPU使用比时，这个比例会受到nice值的影响，nice值低比重就高，nice高比重就低，定量关系为：

<img src="../../source/images/Project 2/image-20220423111516910.png" alt="image-20220423111516910" style="zoom:25%;" />

nice值与weight的映射关系如下：

```c
const int sched_prio_to_weight[40] = {
 /* -20 */     88761,     71755,     56483,     46273,     36291,
 /* -15 */     29154,     23254,     18705,     14949,     11916,
 /* -10 */      9548,      7620,      6100,      4904,      3906,
 /*  -5 */      3121,      2501,      1991,      1586,      1277,
 /*   0 */      1024,       820,       655,       526,       423,
 /*   5 */       335,       272,       215,       172,       137,
 /*  10 */       110,        87,        70,        56,        45,
 /*  15 */        36,        29,        23,        18,        15,
};
```

CPU资源之比为7:3，则优先级前者更高，weight值越大，nice值可分别设置为3和7，weight比值为526:215，且子进程之间的优先级相同。

3. 验证当实时进程在运行时，会抢占其他十个进程。

linux的两种实时进程调度算法：

a. SCHED_FIFO实时调度策略，先到先服务。一旦占用cpu则一直运行。一直运行直到有更高优先级任务到达或自己放弃。

b. SCHED_RR实时调度策略，时间片轮转。当进程的时间片用完，系统将重新分配时间片，并置于就绪队列尾。放在队列尾保证了所有具有相同优先级的RR任务的调度公平。

通过以下两个函数来获得线程可以设置的最高和最低优先级

```c
int sched_get_priority_max(int policy);
int sched_get_priority_min(int policy);
```

通过sched_setscheduler设置调度器 

```c
pid_t pid = getpid();
struct sched_param param;
param.sched_priority = sched_get_priority_max(SCHED_FIFO); 
sched_setscheduler(pid, SCHED_RR, &param);  // SCHED_RR
pthread_setschedparam(pthread_self(), SCHED_FIFO, &param);   // SCHED_FIFO
```

### 实验步骤

1、创建十个CPU-bound程序 

```bash
nice -n 7 ./test1
nice -n 3 ./test1
```

![image-20220423113103006](../../source/images/Project 2/image-20220423113103006.png)

2、创建一个实时进程

```bash
sudo ./test3 # root权限
```

![image-20220423113246255](../../source/images/Project 2/image-20220423113246255.png)



## Task2

### 实验要求

修改Linux源代码，为每个进程添加调度次数的记录  

具体要求：
1、在 task_struct 结构体中添加数据成员变量 int ctx ，用于记录进程的调度次数
2、在进程对应的 /proc/<PID> 目录下添加只读文件 ctx
3、当读取 /proc/<PID>/ctx 时，输出进程当前的调度次数  

### 实验过程

1、ctx声明

每个进程在内核中都有一个进程控制块(PCB)来维护进程相关的信息,Linux内核的进程控制块是task_struct结构体。

```c
struct task_struct *task;
```

它包含着该进程的信息，ctx在此声明。

```c
struct task_struct {
    ......
	randomized_struct_fields_start

	int 				ctx; // add here
	void				*stack;
	refcount_t			usage;
```

2、ctx初始化

在进程创建时，初始化ctx。有关进程创建的函数在kernel/fork.c  ，在使用fork/vfork/clone时系统调用底层都将调用fork.c中的kernel_clone，（5.10.x以前的版本为_do_fork）

```c
pid_t kernel_clone(struct kernel_clone_args *args)
{
	u64 clone_flags = args->flags;
	struct completion vfork;
	struct pid *pid;
	struct task_struct *p;
	......
	p = copy_process(NULL, trace, NUMA_NO_NODE, args);
    ......
```

在copy_process函数中查看task_struct *p的创建过程。

```c
static __latent_entropy struct task_struct *copy_process(
					struct pid *pid,
					int trace,
					int node,
					struct kernel_clone_args *args)
{
	int pidfd = -1, retval;
	struct task_struct *p;
	......
	p = dup_task_struct(current, node);
```

dup_task_struct中的tsk即为创建好的task_struct

```c
static struct task_struct *dup_task_struct(struct task_struct *orig, int node)
{
	struct task_struct *tsk;
	tsk = alloc_task_struct_node(node);
	......
	tsk->stack = stack;
	tsk->ctx = 0; // add here
```

3、ctx更新

在调用该进程时对ctx值进行更新。有关进程调度的函数在kernel/sched/core.c中定义，__schedule()是调度器的主函数，主要实现了两个功能，一个是选择下一个要运行的进程，另一个是进程上下文切换context_switch。在切换到该进程时对ctx进行加一操作。

```c
static __always_inline struct rq *
context_switch(struct rq *rq, struct task_struct *prev,
	       struct task_struct *next, struct rq_flags *rf)
{
	prepare_task_switch(rq, prev, next);
	arch_start_context_switch(prev);
	......
	switch_to(prev, next, prev);
    next->ctx++; // add here
	barrier();

	return finish_task_switch(prev);
}
```

4、目录创建

proc中各个进程目录文件的创建定义在fs/proc/base.c 中，

```c
static const struct pid_entry tgid_base_stuff[] = {
	DIR("task",       S_IRUGO|S_IXUGO, proc_task_inode_operations, proc_task_operations),
	......
	REG("environ",    S_IRUSR, proc_environ_operations),
	REG("auxv",       S_IRUSR, proc_auxv_operations),
	ONE("status",     S_IRUGO, proc_pid_status),
	ONE("personality", S_IRUSR, proc_pid_personality),
	ONE("limits",	  S_IRUGO, proc_pid_limits),
	......
#ifdef CONFIG_HAVE_ARCH_TRACEHOOK
	ONE("syscall",    S_IRUSR, proc_pid_syscall),
#endif
	REG("cmdline",    S_IRUGO, proc_pid_cmdline_ops),
	ONE("stat",       S_IRUGO, proc_tgid_stat),
	ONE("statm",      S_IRUGO, proc_pid_statm),
	REG("maps",       S_IRUGO, proc_pid_maps_operations),
    ONE("ctx"， 		 S_IRUGO, proc_pid_ctx) // add here
```

在fs/proc/base.c中定义函数proc_pid_ctx

```c
static int proc_pid_ctx(struct seq_file *m, struct pid_namespace *ns,
struct pid *pid, struct task_struct *task)
{
    seq_printf(m, "ctx: %d\n", task->ctx);
    return 0;
}
```

### 实验步骤

1、编译linux内核

```bash
make menuconfig
make -j4
make modules_install
make install
```

2、运行实例程序

![image-20220423234458797](../../source/images/Project 2/image-20220423234458797.png)

3、验证

![微信图片_20220423234847](../../source/images/Project 2/微信图片_20220423234847.png)