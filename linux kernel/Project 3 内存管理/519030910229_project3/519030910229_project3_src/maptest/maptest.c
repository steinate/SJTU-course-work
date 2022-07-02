#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/proc_fs.h>
#include <linux/mm.h>
#include <linux/string.h>
#include <linux/slab.h>
#include <linux/highmem.h>

static struct proc_dir_entry *proc_ent;
static struct page* page;
/*
static char content[] =
    "Listen to me say thanks\n"
    "Thanks to you, I'm warm all the time\n"
    "I thank you\n"
    "For being there\n"
    "The world is sweeter\n"
    "I want to say thanks\n"
    "Thanks to you, love is in my heart\n"
    "I thank you, for being there\n"
    "To bring happiness\n";*/

static char content[] =
    "Our lover is but a bubble\n"
    "blown by fancy under a name!\n"
    "Take the letter, \n"
    "you can make the false play come true\n"
    "I was a sick, aimless voice of love now\n"
    "these wandering birds have a place to roost\n"
    "You can see it in the letter Take it!\n"
    "Because the words are not true, it is very beautiful!\n"
    "Take it. Let's do it\n";

static int proc_mmap(struct file* fp, struct vm_area_struct* vma)
{
    // TODO
    int ret;
    unsigned long pfn = page_to_pfn(page); // page fame number
    unsigned long size = vma->vm_end - vma->vm_start;
    if (size > PAGE_SIZE) return -EIO;
    
    // remap kernel memory to userspace
	ret = remap_pfn_range(vma,vma->vm_start,pfn,size,vma->vm_page_prot);
							
	if (ret){
        printk("%s: remap_pfn_range failed at [0x%lx  0x%lx]\n",
            __func__, vma->vm_start, vma->vm_end);
        return -EAGAIN;}
    else
        printk("%s: map to 0x%lx, size: 0x%lx\n", __func__,
            vma->vm_start, size);
            
    return ret;
}

static const struct proc_ops proc_ops = {
    .proc_mmap = proc_mmap,
};

static int __init maptest_init(void)
{
    void* base;

    proc_ent = proc_create("maptest", 0666, NULL, &proc_ops);
    if (!proc_ent)
    {
        proc_remove(proc_ent);
        pr_alert("Error: Could not initialize /proc/maptest\n");
        return -EFAULT;
    }
    pr_info("/proc/maptest created\n");

    // TODO: allocate page and copy content
	page = alloc_page(GFP_KERNEL); // order = 0 2^0=1 page
	base = kmap_local_page(page);
	memcpy(base, content, sizeof(content));
	kunmap_local(base); // unmap a page mapped via kmap_local_page()

    return 0;
}

static void __exit maptest_exit(void)
{
    proc_remove(proc_ent);
    pr_info("/proc/maptest removed\n");
    __free_page(page);
    pr_info("memory freed\n");
}

module_init(maptest_init);
module_exit(maptest_exit);
MODULE_LICENSE("GPL");
