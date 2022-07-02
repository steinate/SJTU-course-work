import matplotlib.pyplot as plt
import numpy as np

f = open('fileio.txt')
data = f.readlines()

utime = [(d.split(' ')[0].strip()) for d in data]
pagenum = [(d.split(' ')[1].strip()) for d in data]

utime = [int(t) for t in utime]
pagenum = [int(p) for p in pagenum]

utime = np.array(utime)
pagenum = np.array(pagenum)

utime_t0 = utime[:-1]
utime_t1 = utime[1:]
time = utime_t1 - utime_t0
pagenum = pagenum[:-1]

start = 20
end = 1000

time = time[start:end]
pagenum = pagenum[start:end]

x = np.array(range(len(pagenum))) * 0.01

plt.title("fileio testbench")
ax1 = plt.gca() # 获取当前轴域
ax1.set_xlabel('time(s)') # 设置x轴标签
ax1.set_ylabel('utime time', color='red') # 设置y轴标签
ax1.plot(x, time, color='red') # 数据绘制
ax1.tick_params(axis='y', labelcolor='red') # 设置y轴刻度属性

ax2 = ax1.twinx() # 创建新axes实例，共享x轴，并设置
ax2.set_ylabel('page number', color='blue')
ax2.plot(x, pagenum, color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

plt.tight_layout() # 紧凑布局
plt.show()