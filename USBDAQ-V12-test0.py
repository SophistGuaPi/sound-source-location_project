import time
import numpy as np
from ctypes import *
from pyqtgraph.Qt import QtCore,QtGui
import pyqtgraph as pg
from pyqtgraph.widgets.RemoteGraphicsView import RemoteGraphicsView
from pyqtgraph import examples

micronum=3
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
curve0 = p0.plot()
curve1=p1.plot()
curve2=p2.plot()
def update():
    print(DAQdll.GetAdBuffSizeV12())
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
                else:
                    value2.append(advalue[i][j])
        curve0.setData(value0)
        curve1.setData(value1)
        curve2.setData(value2)

allvalue=[]*freq*(total_duration+1)
T = []
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)

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