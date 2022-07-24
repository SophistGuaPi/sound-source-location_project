import numpy as np
from scipy.fftpack import fft,ifft
from scipy import fftpack

freq = 40*1000 #参数输入模块

def time_est(x,y):#时间延迟估计函数，x和y分别是采样数组，注意是数组
    sample_freq = fftpack.fftfreq(x.size,1/freq)
    xf = fft(x)
    yf = fft(y)
    for i in range(len(yf)):
        yf[i] = yf[i].conjugate() #取共扼运算
    Rxy = []
    for i in range(len(yf)):
        a = xf[i]*yf[i]
        Rxy.append(a)
    Rxy = np.array(Rxy)
    Rxy = ifft(Rxy)
    tidelay = Rxy.argmax()
    return tidelay

t = np.arange(0,0.2,1/freq) #测试数据生成与处理
test1 = 7*np.sin(2*np.pi*180*t) + 2.8*np.sin(2*np.pi*390*t)
test2 = 7*np.sin(2*np.pi*180*(t+0.01)) + 2.8*np.sin(2*np.pi*390*(t+0.01))
t_delay = time_est(test1,test2)/freq
