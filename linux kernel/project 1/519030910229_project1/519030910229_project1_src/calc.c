#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/proc_fs.h>
#include <linux/uaccess.h>

#define MAX_SIZE 128
#define ID "519030910229"

static int operand1;
module_param(operand1, int, 0);
static char *operator;
module_param(operator, charp, 0);
static int operand2[MAX_SIZE];
static int ninp;
module_param_array(operand2, int, &ninp, 0);

static struct proc_dir_entry *proc_ent;
static struct proc_dir_entry *proc_dir;
// static char output[MAX_SIZE];
// int out_len;
static char buf[MAX_SIZE];
static int result[MAX_SIZE];
// static bool flag = false; // check if change operand1,default: no

static ssize_t proc_read(struct file *fp, char __user *ubuf, size_t len, loff_t *pos)
{
    /* TODO */
    pr_info("into proc_read");
    ssize_t ret = len;
    int i = 0;
	int j = 0;

    if (*pos > 0) return 0;
    if (len < MAX_SIZE) return -EFAULT;

	if(!strcmp(operator, "add")){
    	pr_info("write: add_add in write\n");
    	pr_info("ninp: %d\n", ninp);
    	pr_info("operand1: %d\n", operand1);
    	for(i=0;i < ninp;i++){
    	    result[i] = operand2[i] + operand1;
    	    pr_info("result: %d\n", result[i]);
    	}
	}else if(!strcmp(operator, "mul")){
		for(i=0;i < ninp;i++){
		    result[i] = operand2[i] * operand1;
			pr_info("result: %d\n", result[i]);
		}
	}
	for(i=0, j=0;i < ninp;i++){
		//buf[j++] = '0' + result[i];
		if(result[i] >= 10){
			buf[j++] = '0' + (result[i] / 10);
			buf[j++] = '0' + (result[i] % 10);
		}else{
			buf[j++] = '0' + result[i];
		}
		if(i != ninp-1){
			buf[j++] = ',';
		}else{
			buf[j] = '\n';
		}
	}
	len = j+1;

    if (copy_to_user(ubuf, buf, len)) return -EFAULT;
    *pos += len;
    return ret;
}

static ssize_t proc_write(struct file *fp, const char __user *ubuf, size_t len, loff_t *pos)
{
    /* TODO */
    pr_info("into proc_write");
    if (*pos > 0 || len > MAX_SIZE) return -EFAULT;

    if (copy_from_user(buf, ubuf, len)) return -EFAULT;
    buf[len+1] = '\0';
	operand1 = buf[0] - '0';
    pr_info("write: %s\n", buf);

    return len;
}

static const struct proc_ops proc_file_fops = {
    .proc_read = proc_read,
    .proc_write = proc_write,
};

static int __init proc_init(void)
{
    /* TODO */
    proc_dir = proc_mkdir(ID, NULL);
    proc_ent = proc_create("calc", 0666, proc_dir, &proc_file_fops);
    if (!proc_ent)
    {
        proc_remove(proc_ent);
        pr_alert("Error: Could not initialize /proc/ID/calc\n");
        return -ENOMEM;
    }
    pr_info("/proc/ID/calc created\n");
    
    return 0;
}

static void __exit proc_exit(void)
{
    /* TODO */
    proc_remove(proc_ent);
    proc_remove(proc_dir);
    pr_info("/proc/ID/calc removed\n");
}

module_init(proc_init);
module_exit(proc_exit);

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Calc");
MODULE_AUTHOR("pjq");

