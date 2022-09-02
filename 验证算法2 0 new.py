# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 00:18:07 2022

@author: 53513
"""

import random
import math
import numpy as np

#变量声明
x=random.randint(0,10) # 声源x坐标
y=random.randint(0,10) # 声源y坐标
z=random.randint(0,10) # 声源z坐标

x1 = 0.1
x2 = 0.01

y1 = 0.2
y2 = 0.03

z1 = 0.05
z2 = 0.03
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

def get_tdelay(re,so):#传入参数是坐标点，返回一个时间差值
    return ((math.sqrt((so[0]-re[0])**2+(so[1]-re[1])**2+(so[2]-re[2])**2)-(math.sqrt(so[0]**2+so[1]**2+so[2]**2)))/340)

def get_est_pointlist(re,so,tdelat):#传入坐标点列表，以及监测点矩阵时间差列表,返回定位值列表
    positionlist=[]
    for i in range(len(so)):
        positionlist.append(get_est_point(re,tdelat[i],i))
    return positionlist

def get_est_point(re,tdelay,i):#传入监测点列表，某个声源点对监测点阵列时间差，以及声源点的下标,返回对应声源点的坐标估计
    a1 = re[0][0]
    b1 = re[1][0]-re[0][0]
    m1 = -(tdelay[0]*340)
    n1 = (tdelay[1]-tdelay[0])*340
    l1 = (b1 * m1 * m1+ a1 * n1 * n1 - a1 * a1 * b1 - a1 * b1 * b1) / (2 * (b1 * m1 + a1 * n1))

    a2 = re[2][1]
    b2 = re[3][1]-re[2][1]
    m2 = -(tdelay[2]*340)
    n2 = (tdelay[3]-tdelay[2])*340
    l2 = (b2 * m2 * m2 + a2 * n2 * n2 - a2 * a2 * b2 - a2 * b2 * b2) / (2 * (b2 * m2 + a2 * n2))

    a3 = re[4][2]
    b3 = re[5][2]-re[4][2]
    m3 = -(tdelay[4]*340)
    n3 = (tdelay[5]-tdelay[4])*340
    l3 = (b3 * m3 * m3 + a3 * n3 * n3 - a3 * a3 * b3 - a3 * b3 * b3) / (2 * (b3 * m3 + a3 * n3))

    return [(re[0][0]**2 + m1 * m1 - 2 * m1 * l1) / (2* re[0][0]),
            (re[2][1]**2 + m2 * m2 - 2 * m2 * l2) / (2* re[2][1]),
            (re[4][2]**2 + m3 * m3 - 2 * m3 * l3) / (2* re[4][2])]

#运行代码
if __name__ == "__main__":
    source = generate_source(10, [-5,5])
    re_tdelay = get_realtime(resource, source)
    print('随机生成声源：{}'.format(source))
    print('真实时间差：{}'.format(re_tdelay))
    est_position= get_est_pointlist(resource,source,re_tdelay)
    print('算法预测声源位置：{}'.format(est_position))
