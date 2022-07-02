#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/proc_fs.h>
#include <linux/uaccess.h>
#include <linux/string.h>
#include <linux/sched.h>
#include <linux/mm.h>
#include <linux/highmem.h>
#include <linux/mm_types.h>

#define MAX_SIZE 128

static struct proc_dir_entry *proc_ent;
static char buf[MAX_SIZE];
// static int out_len;
unsigned long int pid;
unsigned long int addr, addr1, addr2;
unsigned long val;
char cmd[MAX_SIZE];
struct task_struct *task;
struct page *tgt_page;

enum operation {
    OP_READ, OP_WRITE
};

static int vaddrtopaddr(struct task_struct *task, unsigned long vaddr) {
    struct mm_struct *mm = task->mm;
    unsigned long paddr, page_addr, page_offset;

    pgd_t *pgd;
	p4d_t* p4d;
    pud_t *pud;
    pmd_t *pmd;
    pte_t *pte;

    // walk the page table
    pgd = pgd_offset(mm, vaddr);
    if (pgd_none(*pgd)) {
        printk("not mapped in pgd\n");
        return -1;
    }

	p4d = p4d_offset(pgd, vaddr);
	if (p4d_none(*p4d)) {
        printk("not mapped in p4d\n");
        return -1;
    }

    pud = pud_offset(p4d, vaddr);
	if (pud_none(*pud)) {
        printk("not mapped in pud\n");
        return -1;
    }

    pmd = pmd_offset(pud, vaddr);
	if (pmd_none(*pmd)) {
        printk("not mapped in pmd\n");
        return -1;
    }
    
    pte = pte_offset_kernel(pmd, vaddr);
	if (pte_none(*pte)) {
        printk("not mapped in pte\n");
        return -1;
    }
    
	page_addr = pte_val(*pte) & PAGE_MASK; // paddr of page
    page_offset = vaddr & ~PAGE_MASK; // offset of vaddr
 
	paddr = page_addr | page_offset; // paddr of vaddr

    return paddr;
}


static struct page *get_tgt_page(struct task_struct *task, unsigned long vaddr) {
    struct mm_struct *mm = task->mm;
    struct page *curr_page;

    pgd_t *pgd;
	p4d_t* p4d;
    pud_t *pud;
    pmd_t *pmd;
    pte_t *pte;

    // walk the page table
    pgd = pgd_offset(mm, vaddr);
    if (pgd_none(*pgd)) {
        printk("not mapped in pgd\n");
        return NULL;
    }

	p4d = p4d_offset(pgd, vaddr);
	if (p4d_none(*p4d)) {
        printk("not mapped in p4d\n");
        return NULL;
    }

    pud = pud_offset(p4d, vaddr);
	if (pud_none(*pud)) {
        printk("not mapped in pud\n");
        return NULL;
    }

    pmd = pmd_offset(pud, vaddr);
	if (pmd_none(*pmd)) {
        printk("not mapped in pmd\n");
        return NULL;
    }
    
    pte = pte_offset_kernel(pmd, vaddr);
	if (pte_none(*pte)) {
        printk("not mapped in pte\n");
        return NULL;
    }
    
    curr_page = pte_page(*pte);
    return curr_page;
}

/* Write val to the specified address */
static void mtest_write_val(struct task_struct *task, unsigned long vaddr, unsigned long val){
    struct page *curr_page = get_tgt_page(task, vaddr);
    if (!curr_page) {
        printk("unexisted page\n");
        return;
    }

    // write value
    unsigned long *kernel_addr;
    unsigned long  page_offset;
    kernel_addr = kmap(curr_page); // map to kernel vaddr
    page_offset = vaddr & (~PAGE_MASK); // offset of vaddr
    kernel_addr += page_offset; // base + offset
    *kernel_addr = val; // write val
}

static int mtest_read_val(struct task_struct *task, unsigned long vaddr) {
    struct page *curr_page = get_tgt_page(task, vaddr);
    if (!curr_page) {
        printk("unexisted page\n");
        return -1;
    }

    // write value
    unsigned long *kernel_addr;
    unsigned long  page_offset;
    kernel_addr = kmap(curr_page); // map to kernel vaddr
    page_offset = vaddr & (~PAGE_MASK); // offset of vaddr
    kernel_addr += page_offset; // base + offset
    
    return *kernel_addr;
}


static ssize_t proc_read(struct file *fp, char __user *ubuf, size_t len, loff_t *pos)
{
    int count = len; /* the number of characters to be copied */
    if (*pos > 0) return -EFAULT;
	if (len > MAX_SIZE) count = MAX_SIZE;

    pr_info("Reading the proc file\n");
    if (copy_to_user(ubuf, buf, count)) return -EFAULT;
    *pos += count;
    
    return count;
}

static ssize_t proc_write(struct file *fp, const char __user *ubuf, size_t len, loff_t *pos)
{
    // TODO: parse the input, read/write process' memory
    int count = len, offset = 0; /* the number of characters to be copied */
	char data[MAX_SIZE];
    if (*pos > 0) return -EFAULT;
	if (len > MAX_SIZE) count = MAX_SIZE;
	
	if (copy_from_user(buf, ubuf, count)) return -EFAULT;
	buf[len+1] = '\0';
	
	if(buf[0] == 'w'){
		// sscanf(buf, "%s %d %lx %d", cmd, &pid, &addr, &val);
		offset = 2;
        sscanf(buf + offset, "%s", data);
        kstrtoul(data, 16, &pid);offset++;
        while (*(buf + offset) != ' ') offset++;
        offset++;
        sscanf(buf + offset, "%s", data);
        kstrtoul(data, 16, &addr);
		while (*(buf + offset) != ' ') offset++;
        offset++;
        sscanf(buf + offset, "%s", data);
        kstrtoul(data, 16, &val);		

		task = get_pid_task(find_get_pid(pid), PIDTYPE_PID);
		mtest_write_val(task, addr, val);
	}else if(buf[0] == 'r'){
		// sscanf(buf, "%s %d %lx", cmd, &pid, &addr);
		offset = 2;
        sscanf(buf + offset, "%s", data);
        kstrtoul(data, 16, &pid);
        while (*(buf + offset) != ' ') offset++;
        offset++;
        sscanf(buf + offset, "%s", data);
        kstrtoul(data, 16, &addr);

		task = get_pid_task(find_get_pid(pid), PIDTYPE_PID);
		val = mtest_read_val(task, addr);
		buf[0] = '0' + val;
		buf[1] = '\0';
		pr_info("write: %s\n", buf);
	}
	
	return count;
    
}

static const struct proc_ops proc_ops = {
    .proc_read = proc_read,
    .proc_write = proc_write,
};

static int __init mtest_init(void)
{
	pr_info("init mtest\n");
    proc_ent = proc_create("mtest", 0666, NULL, &proc_ops);
    if (!proc_ent)
    {
        proc_remove(proc_ent);
        pr_alert("Error: Could not initialize /proc/mtest\n");
        return -EFAULT;
    }
    pr_info("/proc/mtest created\n");
    return 0;
}

static void __exit mtest_exit(void)
{
    proc_remove(proc_ent);
    pr_info("/proc/mtest removed\n");
}

module_init(mtest_init);
module_exit(mtest_exit);
MODULE_LICENSE("GPL");
