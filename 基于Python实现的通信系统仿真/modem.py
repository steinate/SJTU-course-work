import numpy as np
from math import pi, cos, sin, atan

class QPSK_modem:
    def __init__(self, fc, fs, N):
        self.carrier_frequency = fc
        self.sample_rate = fs
        self.wave_points = N
        self.ratio = int(fc/fs)

    def qpsk_modulate(self, raw_data):
        # 功能：将0-1原始数据调制成QPSK格式
        # raw_data: 原始数据
        # fc: 载波中心频率
        # fs: 采样频率
        # N: 每个载波周期采样点
        length = len(raw_data)//2
        raw_data = raw_data.reshape(length,2)

        mod_data =np.zeros(length*self.wave_points*self.ratio)
        I_signal = np.zeros((self.wave_points,1))
        Q_signal = np.zeros((self.wave_points,1))
        # 将数据点映射到星座图上某一点坐标
        star_map = [(2**0.5/2,2**0.5/2), (-2**0.5/2,2**0.5/2),
                    (-2**0.5/2,-2**0.5/2), (2**0.5/2,-2**0.5/2)]
        # 生成载波信号
        for i in range(self.wave_points):
            I_signal[i] = cos(2*pi/(self.wave_points-1)*i)
            Q_signal[i] = -sin(2*pi/(self.wave_points-1)*i)
        # 将信息加到载波上
        for i in range(length):
            ind = raw_data[i,0]*2+raw_data[i,1]
            I_amp, Q_amp = star_map[int(ind)]
            for j in range(self.wave_points):
                for k in range(self.ratio):
                    mod_data[i*self.wave_points*self.ratio+j+k*self.wave_points]=I_amp*I_signal[j]+Q_amp*Q_signal[j]
        return mod_data

    def qpsk_demodulate(self, rec_data):
        # 将QPSK信号格式信号解调为0-1数据
        ratio = self.ratio
        N = self.wave_points
        length = len(rec_data)//(ratio*N)
        dem_data = np.zeros((length,2))

        # 本地载波信号的生成
        I_signal = np.zeros((N,1))
        Q_signal = np.zeros((N,1))
        for i in range(N):
            I_signal[i] = cos(2*pi/(N-1)*i)
            Q_signal[i] = -sin(2*pi/(N-1)*i)

        # QPSK星座图角度表
        star_map = np.zeros(4)
        for i in range(4):
            star_map[i] = pi*i/2+pi/4
        dec2bin = np.array(
            [[0,0],
            [0,1],
            [1,0],
            [1,1]]
        )
        
        # 相干接收
        for i in range(length):
            I, Q = 0, 0
            for j in range(ratio):
                for k in range(N): 
                    I += I_signal[k] * rec_data[i*ratio*N+j*N+k]
                    Q += Q_signal[k] * rec_data[i*ratio*N+j*N+k]       
            # 判决，利用解调结果对应的角度值与星座图比较
            angle = atan(Q/I)
            if I < 0:
                angle += pi
            elif Q < 0:
                angle += 2*pi
            # 比较接收信号与星座图的角度值得到判决结果
            ind = 0
            for k in range(4):
                if abs(angle - star_map[k]) <= pi/4:
                    ind = k
                    break
            dem_data[i] = dec2bin[ind]

        return dem_data.reshape(length*2)

def AWGN(data,amp):
    # 功能:在传输数据上加上噪声
    # data: 原始数据
    # amp: 噪声幅度
    length = len(data)
    noise = amp*np.random.randn(length)
    data_n = data + noise
    return data_n