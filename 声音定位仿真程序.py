import numpy as np
from numpy import random
import math
from scipy.fftpack import fft,ifft
from scipy import fftpack
import matplotlib.pyplot as plt

speed = 340
tlen = 1
tstep = 0.00001
freq = num = int(1/tstep)
sensor = np.array([[0,0],[0,0.2],[0.1,0]])
se_num = 3
rate=1000
"""
def Rxy(x,y,tran):#x是第一个信号列表，y是第二个信号列表,返回值将是dx-dy,tran是平移量，是
    a = 0
    b = 0
    c = 0
    print(tran)
    if tran < 0:
        for i in range(len(x)-tran):
            a+= x[i-tran]*y[i]
            b = x[i-tran]**2
            c = y[i]**2
    else:
        for i in range(len(x)-tran):
            a+= x[i]*y[i+tran]
            b = x[i]**2
            c = y[i+tran]**2
    d = a/(b*c)
    return d
def time_est(x,y):
    Rxylist = []
    displace = 1000
    for i in range(-displace+1,displace):
        Rxylist.append(Rxy(x,y,i))
    m = max(Rxylist)
    t = (Rxylist.index(m)-num)/(num*10)
    return t
"""
def time_est(x,y):#时间延迟估计函数，x和y分别是采样列表，注意是数组
    xf = fft(x)
    yf = fft(y)
    yf = yf.conjugate() #取共扼运算
    Rxy = []
    xf = np.array(xf.tolist()+[0 for i in range(len(x)-1)])
    yf = np.array(yf.tolist()+[0 for i in range(len(y)-1)])
    Rxy = xf*yf
    Rxy = np.array(Rxy)
    Rxy_abs = abs(ifft(Rxy))
    Rxy = ifft(Rxy/Rxy_abs)
    Rxy = np.array(Rxy[int(num):].tolist()+Rxy[:int(num)].tolist())
    #plt.plot(np.real(Rxy))
    #plt.show()
    tidelay = Rxy.argmax()
    print(tidelay)
    tidelay = (tidelay-num)*tstep
    return tidelay

def locate(se1,se2,se3,t10,t20):#定位算法，x0，y0只能为0，x1和y2也为0
    h = se2[1]
    p = se3[0]
    c1 = speed*t10
    c2 = speed*t20
    A = p*(h**2-c1**2)
    B = -h*(p**2-c2**2)
    D = c1*(p**2-c2**2)-c2*(h**2-c1**2)
    print(A,B,D)
    print(D/(A**2+B**2))
    H = math.acos(D/(A**2+B**2))+math.acos(A/(A**2+B**2))
    r = (h**2-c1**2)/(2*(h*np.sin(H)+c1))
    print(r)
    x = r*np.cos(H)
    y = r*np.sin(H)
    return x,y
def distance(re,se1):
    d = ((re[0]-se1[0])**2+(re[1]-se1[1])**2)**0.5
    return d
def signgenerate(tlist):
    signlist = []
    for i in tlist:
        if 0<=i<=3/rate:
            sign = np.sin(2*rate*np.pi*i)
            signlist.append(sign)
        else:
            signlist.append(0)
    return np.array(signlist)
def noise(tlen,tstep):
    pass
def signreceive(re,se,num):
    global tdelaytrue
    ttrue1 = []
    resign = []
    tdelaytrue1 = []
    for i in range(num):
        tlist =np.arange(0,tlen,tstep)
        d = distance(re,se[i])
        attcoef = (0.01/d)**2
        t = d/speed
        ttrue1.append(t)
        #print(t)
        noise = 0.01*np.random.randn(len(tlist))
        receive = signgenerate(tlist-t)+noise
        #plt.plot(receive)
        #plt.show()
        resign.append(receive)
    for i in range(2):
        tdelay = ttrue1[i+1]-ttrue1[0]
        tdelaytrue1.append(tdelay)
    tdelaytrue.append(tdelaytrue1)
    return resign
def dotgenerate(num):
    dotarray = random.rand(num,2)
    return dotarray
resource = 10*dotgenerate(3)
tdelaytrue = []
signlist = []
for i in resource:
    signlist.append(signreceive(i,sensor,se_num))#三个通道数据，对同一声源
tdelay = []
for i in range(len(resource)):
    tdelay1 = []
    for j in range(2):
        tdelay1.append(time_est(signlist[i][j+1],signlist[i][0]))
    tdelay.append(tdelay1)
coordinatest = []
for i in range(3):
    coordinatest1 = []
    x,y = locate(sensor[0],sensor[1],sensor[2],tdelay[i][0],tdelay[i][1])
    coordinatest1.append(x)
    coordinatest1.append(y)
    coordinatest.append(coordinatest1)
coordinatest = np.array(coordinatest)
coorerror = resource-coordinatest
terror = np.array(tdelaytrue)-np.array(tdelay)
tdelay = np.array(tdelay)

print(terror*34000)

    
