# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 00:18:07 2022

@author: 53513
"""

import random
import math
import numpy as np
import cv2
import datetime

starttime = datetime.datetime.now()
print("预计完成时间:",datetime.datetime.now()+datetime.timedelta(minutes=5.5))
#变量声明
x=random.randint(0,10) # 声源x坐标
y=random.randint(0,10) # 声源y坐标
z=random.randint(0,10) # 声源z坐标
constant = 0.00000000001 

x1 = 0.1
x2 = -0.2

y1 = 0.3
y2 = -0.2

z1 = 0.5
z2 = 0.3
sensor = [[x1,0,0],[x2,0,0],[0,y1,0],[0,y2,0],[0,0,z1],[0,0,z2],[0,0,0]]
resource=[[0.1,0,0],[0.01,0,0],[0,0.2,0],[0,0.03,0],[0,0,0.3],[0,0,0.05],[0,0,0]] #所有监测点坐标，一层索引代表一个点

#函数声明
def generate_source(num,rg):#传入生成数量和生成范围，返回生成声源坐标点集。
    source=[]
    for i in range(num):
        source.append([random.uniform(rg[0],rg[1]),random.uniform(rg[0],rg[1]),random.uniform(rg[0],rg[1])]) # 声源z坐标]))
    return source

def get_realtime(re,so):#传入的参数是点集,返回各个声源点对监测点矩阵的时间差列表
    time=[]
    for i in range (len(so)):
        t=[]
        time.append(t)
        for j in range(len(re)-1):
            t.append(get_tdelay(re[j], so[i]))
            np.array(t)
    return time

def get_tdelay(re,so):#se是声源，re是探测器，一定要注意
    return ((math.sqrt((so[0]-re[0])**2+(so[1]-re[1])**2+(so[2]-re[2])**2)-(math.sqrt(so[0]**2+so[1]**2+so[2]**2)))/(340+constant))

def get_est_pointlist(re,tdelat):#传入坐标点列表，以及监测点矩阵时间差列表,返回定位值列表
    positionlist=[]
    for i in range(len(tdelat)):
        positionlist.append(get_est_point(re,tdelat[i],i))
    return positionlist

def get_est_point(re,tdelay,i):#传入监测点列表，某个声源点对监测点阵列时间差，以及声源点的下标,返回对应声源点的坐标估计
    a1 = re[0][0]
    b1 = re[1][0]-re[0][0]
    m1 = -(tdelay[0]*340)
    n1 = (tdelay[1]-tdelay[0])*340
    l1 = (b1 * m1 * m1+ a1 * n1 * n1 - a1 * a1 * b1 - a1 * b1 * b1) / ((2 * (b1 * m1 + a1 * n1))+constant)

    a2 = re[2][1]
    b2 = re[3][1]-re[2][1]
    m2 = -(tdelay[2]*340)
    n2 = (tdelay[3]-tdelay[2])*340
    l2 = (b2 * m2 * m2 + a2 * n2 * n2 - a2 * a2 * b2 - a2 * b2 * b2) / ((2 * (b2 * m2 + a2 * n2))+constant)

    a3 = re[4][2]
    b3 = re[5][2]-re[4][2]
    m3 = -(tdelay[4]*340)
    n3 = (tdelay[5]-tdelay[4])*340
    l3 = (b3 * m3 * m3 + a3 * n3 * n3 - a3 * a3 * b3 - a3 * b3 * b3) / ((2 * (b3 * m3 + a3 * n3))+constant)

    return [(re[0][0]**2 + m1 * m1 - 2 * m1 * l1) / ((2* re[0][0])+constant),
            (re[2][1]**2 + m2 * m2 - 2 * m2 * l2) / ((2* re[2][1])+constant),
            (re[4][2]**2 + m3 * m3 - 2 * m3 * l3) / ((2* re[4][2])+constant)]
def matrixgenerate(length,width,lstep,wstep):
    list = [[[i*lstep-length/2,j*wstep-width/2,0] for i in range(int(length/lstep))] for j in range(int(width/wstep))]
    matrix = np.array(list)
    return matrix
def tmatrix(source,se):
    tlist3=[]
    for i in source:
        tlista2 = get_realtime(se,i)
        tlist3.append(tlista2)
    tlist3 = np.array(tlist3)
    return tlist3
def locate(receive,tlist3):
    point3 = []
    for i in tlist3:
        point3a2 = get_est_pointlist(receive,i)
        point3.append(point3a2)
    point3 = np.array(point3)
    return point3
def derror1(true1,pre1):
    dtrue = true1[0]**2+true1[1]**2
    dpre = pre1[0]**2+pre1[1]**2
    errorper = abs((dtrue-dpre)/(dtrue+constant))
    return errorper
def derror2(true2,pre2):
    error1 = []
    for i in range(len(true2)):
        error = derror1(true2[i],pre2[i])
        error1.append(error)
    return error1
def derror3(true3,pre3):
    error2 = []
    for i in range(len(true3)):
        error1 = derror2(true3[i],pre3[i])
        error2.append(error1)
    error2 = np.array(error2)
    return error2
def draw(value2):
    value2a2 = value2
    img2 = np.zeros_like(resource)
    img2[:,:,0] = 256-value2*256
    img2[:,:,1] = 256-value2*256
    img2[:,:,2] = 256-value2*256
    cv2.imwrite("coefficient"+str(int(con*10000))+".jpg",img2)
    return img2
resource = matrixgenerate(20,20,0.01,0.01)
tlist3 = tmatrix(resource,sensor)
con = 1.001
point3 = locate(sensor,tlist3*con)
error2 = derror3(resource,point3)
img2 = draw(error2)
endtime = datetime.datetime.now()
print((endtime-starttime).seconds)


