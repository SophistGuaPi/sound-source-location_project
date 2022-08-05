clear;
clc;
c=341
RPositionX=unifrnd(-100,100,100,1)
RPositionY=unifrnd(-100,100,100,1)
%plot(RPositionX,RPositionY,'r*')
rx=[0.5;-0.5;0]
ry=[0;0;0]
plot(rx,ry,'r*')
RT0=power(power(RPositionX-rx(1),2)+power(RPositionY-ry(1),2),1/2)/c-power(power(RPositionX-rx(2),2)+power(RPositionY-ry(2),2),1/2)/c
RT1=power(power(RPositionX-rx(1),2)+power(RPositionY-ry(1),2),1/2)/c-power(power(RPositionX-rx(3),2)+power(RPositionY-ry(3),2),1/2)/c
RT2=power(power(RPositionX-rx(2),2)+power(RPositionY-ry(2),2),1/2)/c-power(power(RPositionX-rx(3),2)+power(RPositionY-ry(3),2),1/2)/c
%×ø±ê¼ÆËãº¯Êý£º

funtion [x,y]=culculate(xi,yi,deltaT)
    syms x y;
    e1=power(power(x-rx(1),2)+power(y-ry(1),2),1/2)/c-power(power(x-rx(2),2)+power(y-ry(2),2),1/2)/c-RT0;
    e2=power(power(x-rx(1),2)+power(y-ry(1),2),1/2)/c-power(power(x-rx(3),2)+power(y-ry(3),2),1/2)/c-RT1;
    e3=power(power(x-rx(2),2)+power(y-ry(2),2),1/2)/c-power(power(x-rx(3),2)+power(y-ry(3),2),1/2)/c-RT2;
    [x0,y0]=solve(e1,e2,e3,x,y);
end
