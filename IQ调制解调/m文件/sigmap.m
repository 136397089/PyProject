close all;
clc;
M=16;
data = randi([0 M-1],1000,1); %生成1000行数，数值为随机【0，M-1】中的整数
data2=pskmod(data,M,pi/M);    %psk modulation
noisedata = awgn(data2,20);   %添加噪声
data3 = qammod(data,M,'UnitAveragePower',true); %qam modulation 
%具体含义可以上matlab官网查看用法
noisedata2 = awgn(data3,20);

scatterplot(noisedata);
title('PSKMOD');
grid on;
axis tight;

scatterplot(noisedata2);
title('QAMMOD');
grid on;
axis tight;






syms x y z;
syms t;
N=3;
bits = [0.2,5,6,0.4];
syms list;
list = [];
single = 0;
for i = 1:N+1
    list = [list sin(i*t)*bits(i)];
    single= single + list(i);
end

syms input Recive;
input = [];
Recive = [];
for i = 1:N+1
    input = [input  single*sin(i*t)];
end

for i=1:N+1
    Recive = [Recive int(input(i),0,2*pi)/pi];
end



