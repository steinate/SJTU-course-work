import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk

from pcm import PCM_decode, PCM_encode
from modem import QPSK_modem, AWGN

class my_menu:
    def __init__(self):
        self.Gui = Tk()
        self.Gui.title('通信系统')
        self.Gui.geometry("220x180")
        self.ddl_label = Label(self.Gui, text='信号选项')
        self.ddl = ttk.Combobox(self.Gui)
        self.ddl['value'] = ('sin', 'img')
        self.ddl.current(0)
        
        self.ddl_label.grid(row=1, column=1, sticky=W)
        self.ddl.grid(row=1, column=2, sticky=W)
        #标签控件布局
        Label(self.Gui, text="采样频率").grid(row=2, column=1)
        Label(self.Gui, text="载波频率").grid(row=3, column=1)
        Label(self.Gui, text="模拟点数").grid(row=4, column=1)
        Label(self.Gui, text="噪声幅度").grid(row=5, column=1)
        Label(self.Gui, text="误比特率").grid(row=6, column=1)

        self.entry1=Entry(self.Gui)
        self.entry1.insert(END, 100)
        self.entry1.grid(row=2, column=2)

        self.entry2=Entry(self.Gui)
        self.entry2.insert(END, 500)
        self.entry2.grid(row=3, column=2)

        self.entry3=Entry(self.Gui)
        self.entry3.insert(END, 10)
        self.entry3.grid(row=4, column=2)

        self.entry4=Entry(self.Gui)
        self.entry4.insert(END, 0.3)
        self.entry4.grid(row=5, column=2)

        self.entry5=Entry(self.Gui)
        self.entry5.delete(0, END)
        self.entry5.grid(row=6, column=2)
        
        Button(self.Gui, text='Quit', command=self.Gui.quit).grid(row=7, column=1,sticky=W, padx=5, pady=5)
        Button(self.Gui, text='Run', command=self.communication).grid(row=7, column=2, sticky=W, padx=5, pady=5)
        self.Gui.mainloop()
    
    def get_signal(self, signal_type):
        if signal_type == 'sin':
            # 生成正弦信号
            x = np.linspace(-np.pi,np.pi,256)
            signal = np.sin(x)
            return signal, x
        elif signal_type == 'img':
            # 生成图像信号
            img = plt.imread('.\img\lena50.jpg')
            h, w, c = img.shape # (50, 50, 3)
            signal = img.flatten()
            return signal, [h, w, c]
        else:
            x = np.linspace(-np.pi,np.pi,256)
            signal = np.sin(x)
            return signal, x
    
    def get_modem(self, fs, fc, N):
        sine_modem = QPSK_modem(fc, fs, N)
        return sine_modem

    def plot(self, signal, signal_type, inf):
        if signal_type == 'img':
            [h, w, c] = inf
            img = signal.reshape((h, w, c)).astype(np.uint8)
            plt.imshow(img, cmap=plt.cm.binary)
            plt.show()
        elif signal_type == 'sin':
            x = inf
            plt.plot(x,signal,"b-",lw=2.5,label="正弦")     # 绘图
            plt.show()
    
    def wrong_rate(self, raw_data, rec_data):
        length = len(raw_data)
        cnt = 0
        for i in range(length):
            if_wrong = int(raw_data[i]) ^ int(rec_data[i])
            cnt += if_wrong
        return float(cnt)/length

    def communication(self):
        # 参数定义
        signal_type = self.ddl.get()                        # 信号类别
        fs = int(self.entry1.get())                         # 采样频率
        fc = int(self.entry2.get())                         # 载波频率
        N = int(self.entry3.get())                          # 模拟点数

        # 信号生成
        noise = float(self.entry4.get())                    # 噪声幅度
        signal, inf = self.get_signal(signal_type)          # 获取信号
        sine_modem = self.get_modem(fs, fc, N)              # 初始化调制解调器

        # 信号传输
        pcm_signal, m = PCM_encode(signal)                  # 编码
        mod_signal = sine_modem.qpsk_modulate(pcm_signal)   # 调制
        rec_signal = AWGN(mod_signal, noise)                # 噪声
        dem_signal = sine_modem.qpsk_demodulate(rec_signal) # 解调
        dec_signal = PCM_decode(dem_signal, m)              # 解码

        # 性能分析
        ber = self.wrong_rate(pcm_signal, dem_signal)
        self.entry5.insert(0, ber)                          # 求解误比特率
        self.plot(dec_signal, signal_type, inf)             # 绘图

if __name__ == '__main__':
    my_menu()