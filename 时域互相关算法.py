import time
import numpy as np
from ctypes import *
from pyqtgraph.Qt import QtCore,QtGui
import pyqtgraph as pg
from pyqtgraph.widgets.RemoteGraphicsView import RemoteGraphicsView
from pyqtgraph import examples
from scipy.fftpack import fft,ifft
from scipy import fftpack

#参数输入
micronum=3 
freq=40*1000  #采样频率，单位赫兹
fps = 10  #帧率，单位图/秒
total_duration = 10 #总采样时长，单位秒
total_duration=total_duration-1
num = freq//fps #每张图点数，整数制
pic_num = fps*total_duration #总生成图数
print("每张图点数:"+str(num))
print("总图数："+str(pic_num))
t0list,t1list,t2list=[],[],[]

#stdcall调用约定：两种加载方式
#DAQdll = ctypes.windll.LoadLibrary("dllpath")
#cdecl调用约定：两种加载方式
#DAQdll = ctypes.cdll.LoadLibrary("dllpath")
#DAQdll = ctypes.CDLL("dllpath")
#<span style="font-family:Microsoft YaHei;">

#首先打开设备


#由于int __stdcall ADSingleV12(int ad_mod, int chan, int gain, float* adResult);
#函数需要返回一个采集结果，使用float*传入一个地址，采集结果写入这个指针所指向的地址，
#所以需要先申明一个float类型的变量，然后使用byref得到这个变量地址当做指针传给函数
#调用函数采集通道1的电压，单端模式，量程默认正负10V
#打印采集到的电压值

#绘图设置初始化
app = pg.mkQApp("Plot Auto Range Example")
win = pg.GraphicsLayoutWidget(show=True, title="Plot auto-range examples")
win.resize(800,600)
win.setWindowTitle('pyqtgraph example: PlotAutoRange')
p0 = win.addPlot(title="Auto Pan Only")
p0.setAutoPan(y=True)
p1=win.addPlot(title="Auto Pan Only")
p1.setAutoPan(y=True)
p2=win.addPlot(title="Auto Pan Only")
p2.setAutoPan(y=True)
win.nextRow()
p3 = win.addPlot(title="Auto Pan Only")
curve0 = p0.plot()
curve1=p1.plot()
curve2=p2.plot()
curve3 = p3.plot()

#函数定义
def Rxy(x,y,tran):#x是第一个信号列表，y是第二个信号列表,返回值将是dx-dy,tran是平移量，是
    a = 0
    b = 0
    c = 0
    if tran < 0:
        #print(tran)
        for i in range(len(x)-abs(tran)):
            a+=x[i+abs(tran)]*y[i]
            b = x[i+abs(tran)]**2
            c = y[i]**2
    else:
        for i in range(len(x)-abs(tran)):
            a+= x[i]*y[i+tran]
            b = x[i]**2
            c = y[i+tran]**2
    d = a/(b*c)
    return d
def tdelay(x,y,num):
    Rxylist = []
    n=num*(-1)+1
    for i in range(n,num):
        Rxylist.append(Rxy(x,y,i))
    m = max(Rxylist)
    curve3.setData(Rxylist)
    t = (Rxylist.index(m)-40)/(40000)
    return t

def update():
    global t0list, t1list, t2list
    T=[]*num
    if (DAQdll.GetAdBuffSizeV12() >= num*micronum):
        value0=[]
        value1=[]
        value2=[]
        DAQdll.ReadAdBuffV12(byref(advalue), num*micronum)
        for i in range(3):
            for j in range(num):
                if i==0:
                    value0.append(advalue[i][j])
                if i==1:
                    value1.append(advalue[i][j])
                if i==2:
                    value2.append(advalue[i][j])
        curve0.setData(value0)
        curve1.setData(value1)
        curve2.setData(value2)
        t10 = tdelay(value1,value0,num//100)
        t20 = tdelay(value2,value0,num//100)
        #t0list.append(t10)
        #curve3.setData(t0list)
        print(t10,t20)
        


#数据准备与初始化
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)

#打开采集卡，连续采集与关闭
if __name__ == '__main__':
    DAQdll = WinDLL("./USBDAQ_DLL_V12X64.dll")
    erro = DAQdll.OpenUsbV12()
    advalue = (c_float * int(num) * micronum)()
    erro = DAQdll.ADSingleV12(1, 0, 1, byref(advalue))
    print(advalue)
    erro = DAQdll.MADContinuConfigV12(1, 0, micronum-1, 1 , freq)
    pg.exec()
    erro = DAQdll.ADContinuStopV12()
    erro = DAQdll.CloseUsbV12()
