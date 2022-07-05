import time
from ctypes import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style

freq=40*1000  #采样频率，单位赫兹
fps = 10  #帧率，单位图/秒
total_duration = 10 #总采样时长，单位秒
total_duration=total_duration-1
num = freq//fps #每张图点数，整数制
pic_num = fps*total_duration #总生成图数
print("每张图点数:"+str(num))
print("总图数："+str(pic_num))

#stdcall调用约定：两种加载方式
#DAQdll = ctypes.windll.LoadLibrary("dllpath")
DAQdll = WinDLL("./USBDAQ_DLL_V12X64.dll")
#cdecl调用约定：两种加载方式
#DAQdll = ctypes.cdll.LoadLibrary("dllpath")
#DAQdll = ctypes.CDLL("dllpath")
#<span style="font-family:Microsoft YaHei;">

#首先打开设备
erro=DAQdll.OpenUsbV12()

#由于int __stdcall ADSingleV12(int ad_mod, int chan, int gain, float* adResult);
#函数需要返回一个采集结果，使用float*传入一个地址，采集结果写入这个指针所指向的地址，
#所以需要先申明一个float类型的变量，然后使用byref得到这个变量地址当做指针传给函数
advalue=(c_float*int(num))()
#调用函数采集通道1的电压，单端模式，量程默认正负10V
erro=DAQdll.ADSingleV12(1,0,1,byref(advalue))
#打印采集到的电压值
print(advalue)
erro=DAQdll.ADContinuConfigV12(1,0,1,freq)
plt.ion()
for i in range(pic_num):
    T = []
    for j in range(num):
        T.append(i/fps+j/num)
    if(DAQdll.GetAdBuffSizeV12()>=num):
        DAQdll.ReadAdBuffV12(byref(advalue),num)
        print(advalue)
        plt.clf()
        plt.ylim(0, 5)
        plt.plot(T,advalue)
        plt.pause(0.000001)
        plt.ioff()
    time.sleep(1/fps)

erro=DAQdll.ADContinuStopV12()
#最后需要关闭设备
erro=DAQdll.CloseUsbV12()
