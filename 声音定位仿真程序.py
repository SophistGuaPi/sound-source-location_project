import numpy as np
from numpy import random
import math
import scipy.fft
import matplotlib.pyplot as plt

speed = 340
tlen = 1
tstep = 0.0001
sample_freq = 1/tstep #采样频率
num = int(tlen/tstep) #列表长度
sensor = np.array([[0,0],[3,0],[-3,0],[0,3],[0,-3]])
se_num = 5
rate=1000
tdelaytrue=[]
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
def locate(se,tdelay):
    coordinate = []
    x1 = se[1][0]
    x2 = se[2][0]
    y1 = se[3][1]
    y2 = se[4][1]
    timex1 = tdelay[0]
    timex2 = tdelay[1]
    timey1 = tdelay[2]
    timey2 = tdelay[3]
    a1 = x1
    b1 = x2-x1
    m1 = -(timex1*340);
    n1 = (timex2-timex1)*340
    l1 = (b1 * m1 * m1+ a1 * n1 * n1 - a1 * a1 * b1 - a1 * b1 * b1) / (2 * (b1 * m1 + a1 * n1))
    x = (x1 * x1 + m1 * m1 - 2 * m1 * l1) / 18 * x1
    a2 = y1
    b2 = y2-y1
    m2 = -(timey1*340);
    n2 = (timey2-timey1)*340
    l2 = (b2 * m2 * m2 + a2 * n2 * n2 - a2 * a2 * b2 - a2 * b2 * b2) / (2 * (b2 * m2 + a2 * n2))
    y = (y1 * y1 + m2 * m2 - 2 * m2 * l2) / 18* y1
    coordinate.append(x)
    coordinate.append(y)
    
    return coordinate
def t_est(x):
    Rx = Rxy(x)
    maxnum = Rx.argmax()
    tdelay = (maxnum-num)*tstep
    return tdelay
def Rxy(x,maxlag=100000000):
    m = np.shape(x[0])[0]
    mx1 = min(maxlag,m-1)
    m2 = findTransformLength(m)
    X = scipy.fft.fft(x[0],m2)
    Y = scipy.fft.fft(x[1],m2)
    c1 = scipy.fft.ifft(X*Y.conjugate())
    c = c1.tolist()[m2-mx1-1:m2]+c1.tolist()[0:m2-mx1]
    c = np.array(c)
    #plt.plot(c)
    #plt.show()
    return c
def findTransformLength(m):
    m = m*2
    while True:
        r = m
        p = [2,3,5,7]
        for i in p:
            if r>1 and r%i==0:
                r = r/i
                print(r)
        if r==1:
            break
        m+=1
    return m
"""
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
"""
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
def signreceive(re,se,se_num):
    global tdelaytrue
    ttrue1 = []
    resign = []
    tdelaytrue1 = []
    for i in range(se_num):
        tlist =np.arange(0,tlen,tstep)
        d = distance(re,se[i])
        attcoef = (0.01/d)**2
        t = d/speed
        ttrue1.append(t)
        #print(t)
        noise = 0.01*np.random.randn(len(tlist))
        receive = signgenerate(tlist-t)
        #plt.plot(receive)
        #plt.show()
        resign.append(receive)
    for i in range(4):
        tdelay = ttrue1[i+1]-ttrue1[0]
        tdelaytrue1.append(tdelay)
    tdelaytrue.append(tdelaytrue1)
    return resign
def dotgenerate(num):
    dotarray = random.rand(num,2)
    return dotarray
def signre(resource,sensor):#产生信号矩阵，第一个是声源坐标矩阵，第二个是探测器坐标矩阵
    signlist = []
    for i in range(len(resource)):
        signlist.append(signreceive(resource[i],sensor,se_num))
    return signlist
def time_est(sign):
    tdelay = []
    for i in range(len(sign)):
        tdelay1 = []
        for j in range(len(sensor)-1):
            signpart = []
            signpart1 = sign[i][j+1].tolist()
            signpart2 = sign[i][0].tolist()
            signpart.append(signpart1)
            signpart.append(signpart2)
            signpart = np.array(signpart)
            tdelay1.append(t_est(signpart))
        tdelay.append(tdelay1)
    tdelay = np.array(tdelay)
    return tdelay
def locatefinal(sensor,tdelay):
    coor = []
    for i in range(len(tdelay)):
        print(i)
        coor1 = locate(sensor,tdelay[i])
        coor.append(coor1)
    coor = np.array(coor)
    return coor
resource = [[10,10],[2,2],[3,3]]
signlist = signre(resource,sensor)
tdelaylist = time_est(signlist)
#tdelaytrue = np.array(tdelaytrue)
#print((tdelaytrue-tdelaylist)/tdelaytrue)
coorpre = locatefinal(sensor,tdelaylist)
print(coorpre)
coorerror = resource-coorpre



