#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/proc_fs.h>
#include <linux/uaccess.h>
#include <linux/string.h>
#include <linux/sched.h>
#include <linux/sched/cputime.h>
#include <linux/mm.h>

#define MAX_SIZE 128

static struct proc_dir_entry *proc_ent;
static char output[MAX_SIZE];
static int out_len;
static struct task_struct* taskp;


static u64 get_utime(struct task_struct *taskp)
{
	u64 utime = taskp->signal->utime;
	struct task_struct* t;

	for_each_thread(taskp, t) {
		utime += t->utime;
	} 
	return utime;
}

static inline int _ptep_test_and_clear_young(struct task_struct *taskp,
unsigned long vaddr)
{
	int ret = 0;
	pgd_t *pgd;
	p4d_t *p4d;
	pud_t *pud;
	pmd_t *pmd;
	pte_t *pte;
	
	pgd = pgd_offset(taskp->mm, vaddr);
    if (pgd_none(*pgd))
        return 0;
    p4d = p4d_offset(pgd, vaddr);
    if (p4d_none(*p4d))
        return 0;
    pud = pud_offset(p4d, vaddr);
    if (pud_none(*pud))
        return 0;
    pmd = pmd_offset(pud, vaddr);
    if (pmd_none(*pmd))
        return 0;
    pte = pte_offset_kernel(pmd, vaddr);
	
	if(pte_young(*pte))
		ret = test_and_clear_bit(_PAGE_BIT_ACCESSED, (unsigned long *)&pte->pte);
	return ret;
}

static unsigned long get_pagenum(struct task_struct *taskp)
{
	int cnt = 0;
	unsigned long vaddr;
	struct vm_area_struct *vma;
	
	for (vma = taskp->mm->mmap; vma; vma = vma->vm_next){
    	for (vaddr = vma->vm_start; vaddr < vma->vm_end; vaddr += PAGE_SIZE) {
            cnt += _ptep_test_and_clear_young(taskp, vaddr);
        }
    }
	
	return cnt;
}

static ssize_t proc_read(struct file *fp, char __user *ubuf, size_t len, loff_t *pos)
{
    int count = 0; /* the number of characters to be copied */
    u64 utime=0;
    unsigned long pagenum = 0;
    
    if (*pos == 0) {
        /* a new read, update process' status */
        /* TODO */
        utime = get_utime(taskp);
        pagenum = get_pagenum(taskp);
        sprintf(output, "%lld, %ld\n", utime, pagenum);
		out_len = strlen(output);
    }
   
    if (out_len - *pos > len) {
        count = len;
    } else {
        count = out_len - *pos;
    }

    pr_info("Reading the proc file\n");
    if (copy_to_user(ubuf, output + *pos, count)) return -EFAULT;
    *pos += count;
    
    return count;
}

static ssize_t proc_write(struct file *fp, const char __user *ubuf, size_t len, loff_t *pos)
{
    int pid;

    if (*pos > 0) return -EFAULT;
    pr_info("Writing the proc file\n");
    if(kstrtoint_from_user(ubuf, len, 10, &pid)) return -EFAULT;

    taskp = get_pid_task(find_get_pid(pid), PIDTYPE_PID);

    *pos += len;
    return len;
}

static const struct proc_ops proc_ops = {
    .proc_read = proc_read,
    .proc_write = proc_write,
};

static int __init watch_init(void)
{
    proc_ent = proc_create("watch", 0666, NULL, &proc_ops);
    if (!proc_ent) {
        proc_remove(proc_ent);
        pr_alert("Error: Could not initialize /proc/watch\n");
        return -EFAULT;
    }
    pr_info("/proc/watch created\n");
    return 0;
}

static void __exit watch_exit(void)
{
    proc_remove(proc_ent);
    pr_info("/proc/watch removed\n");
}

module_init(watch_init);
module_exit(watch_exit);
MODULE_LICENSE("GPL");
