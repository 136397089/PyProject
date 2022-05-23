%BPSK 调制解调
clear all;clc;
N=30;%比特数
T=1;%比特周期
fc=2;%载波频率
Fs=30;%抽样频率
snr=10;%信躁比
bitstream=randi([0,1],1,N);%随机产生的比特数0、1
bitstream=2*bitstream-1;%单极性变为双极性（0到-1；1到1）
I=[];Q=[];
%奇数进I路,偶数进Q路

for i=1:N
    if bitstream(i)>0
        I=[I,sqrt(2)/2];
        Q=[Q,sqrt(2)/2];
    else
        I=[I,-sqrt(2)/2];
        Q=[Q,-sqrt(2)/2];
    end
end



%采用绘图比较I、Q比特流
bit_data=[];
for i=1:N
    bit_data=[bit_data,bitstream(i)*ones(1,T*Fs)];%在一个比特周期里面有T*Fs个1和采样点一模一样
end
I_data=[];Q_data=[];
for i=1:N
    %I路和Q路是原来比特周期的两倍,2Tb=Ts(码元周期)，因此采样点个数为T*Fs*2
    I_data=[I_data,I(i)*ones(1,T*Fs)];
    Q_data=[Q_data,Q(i)*ones(1,T*Fs)];
end
%绘图
figure();
%时间轴
t=0:1/Fs:N*T-1/Fs;
subplot(3,1,1)
plot(t,bit_data);legend('Bitstream')%比特信息
subplot(3,1,2)
plot(t,I_data);legend('I Bitstream')%I路信息
subplot(3,1,3)
plot(t,Q_data);legend('Q Bitstream')%Q路信息
%载波信号
bit_t=0:1/Fs:2*T-1/Fs;%载波周期为2倍比特周期,定义时间轴
%定义I路和Q路的载波
I_carrier=[];Q_carrier=[];
for i=1:N
    I_carrier=[I_carrier,I(i)*cos(2*pi*fc*bit_t)];%I路载波信号
    Q_carrier=[Q_carrier,Q(i)*cos(2*pi*fc*bit_t+pi/2)];%Q路载波信号
end
%传输信号
BPSK_signal=I_carrier+Q_carrier;
%绘图
figure();%产生一个新图
subplot(4,1,1)
plot(t,I_carrier);legend('I signal')%I路信号
subplot(4,1,2)
plot(t,Q_carrier);legend('Q signal')%Q路信号
subplot(4,1,3)
plot(t,BPSK_signal);legend('BPSK signal')%I路、Q路和的信号
%接收信号
BPSK_receive=awgn(BPSK_signal,snr);%awgn()添加噪声

subplot(4,1,4)
plot(t,BPSK_receive);legend(strcat('BPSK signal=',num2str (snr))) %添加噪声后的信号

%解调
I_RevocerRes = []
Q_recoverRes = []
for i=1:N
    I_output=BPSK_receive(1,(i-1)*length(bit_t)+1:i*length(bit_t)).*cos(2*pi*fc*bit_t);
    I_RevocerRes(i) = mean(I_output);
    if I_RevocerRes(i) >0 %积分器求和，大于0为1，否则为-1
        I_recover(i)=sqrt(2);
    else
        I_recover(i)=-sqrt(2);
    end
    Q_output=BPSK_receive(1,(i-1)*length(bit_t)+1:i*length(bit_t)).*cos(2*pi*fc*bit_t+ pi/2);
    Q_recoverRes(i) = mean(Q_output);
    if Q_recoverRes(i)>0
        Q_recover(i)=1;
    else
        Q_recover(i)=-1;
    end
end
res = I_RevocerRes + Q_recoverRes*1i;
%并/串变换
bit_recover=[];
for i=1:N
    if mod(i,2)~=0
        bit_recover=[bit_recover,I_recover((i-1)/2+1)];%奇数取I路信息
    else
        bit_recover=[bit_recover,Q_recover(i/2)];%偶数取Q路信息
    end
end
%适用绘图比较I、Q比特流
recover_data=[];
for i=1:N
    recover_data=[recover_data,bit_recover(i)*ones(1,T*Fs)];
end
I_recover_data=[];Q_recover_data=[];
for i=1:N/2
    I_recover_data=[I_recover_data,I_recover(i)*ones(1,T*Fs*2)];
    Q_recover_data=[Q_recover_data,Q_recover(i)*ones(1,T*Fs*2)];
end
%绘图
figure();
t=0:1/Fs:N*T-1/Fs;
subplot(3,1,1)
plot(t,recover_data);legend('Bitstream')%恢复的比特信息
subplot(3,1,2)
plot(t,I_recover_data);legend('I Bitstream')%恢复的I路信息
subplot(3,1,3)
plot(t,Q_recover_data);legend('Q Bitstream')%恢复的Q路信息

scatterplot(res)
axis([-1 1 -1 1])
hold on;
recmiddlex = 0; recmiddley = 0;recw=sqrt(2); rech=sqrt(2);
recxb = recmiddlex - recw/2;
recyb = recmiddley - rech/2;
rectangle('Position',[recxb, recyb, recw, rech],'Curvature',[1, 1]);axis equal; % 画圆


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



clc;

close all;

clear;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%

%  假定：

%     2倍载波频率采样的bpsk信号

%     调制速率为在波频率的 N/2m

%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

m=128;
N=512;
n=1:1:N;
N0=0.5*randn(1,N) %噪声
h0=zeros(1,N);
%     30阶低通滤波器 h0
f = [0 0.3 0.3 1]; w0 = [1 1 0 0];
b = fir2(30,f,w0);
[h,w] = freqz(b,1,N/2);
h0(1,1:N/2)=abs('h');
for i=1:N/2
    h0(1,N-i+1)=h0(1,i);
end;

%%%%%%%%%   随机序列 %%%%%%%%%%%%

a=rand(1,m);

for i=1:m
    if(a(1,i)>0.5)
        a(1,i)=1;
    else
        a(1,i)=-1;
    end;
end;

a
%%% 生成BPSK信号    
bpsk_m=zeros(1,N);
j=1;k=1;
for i=1:N
    if(j==(N/m+1))
        j=1;
        k=k+1;
    end;    % 0.05*pi 为初始相位，可以任意改变
    bpsk_m(1,i)=a(1,k)*sin(2*pi*0.5*i+0.05*pi)+a(1,k)*cos(2*pi*0.5*i+0.05*pi);
    j=j+1;
end;
bpsk_m=bpsk_m+N0;% 信号加噪声，模拟过信道
% 接收处理  用正交本振与信号相乘，变频
bpsk_m1=bpsk_m.*sin(2*pi*0.5*n);
bpsk_m2=bpsk_m.*cos(2*pi*0.5*n);
%滤波

tempx=fft(bpsk_m1);
tempx=tempx.*h0;     %低通滤波
tempx=ifft(tempx);
real_x=real(tempx);
tempx=h0.*fft(bpsk_m2);
tempx=tempx.*h0;     %低通滤波
tempx=ifft(tempx);
real_x1=real(tempx);
subplot(2,1,1);
plot(real_x1+real_x,'b');

axis([1  N -2.5 2.5]);
grid on;
hold on;
In=real_x1+real_x;      % 可只取一路，这里取了两路之和
for i=1:N               % 滤波后整形
    if(In(1,i)>0)       % 判决，得到解调结果
        In(1,i)=1;
    else
        In(1,i)=-1;
    end;
end;

plot(In,'r');
an=zeros(1,m);

for i=1:m
    an(1,i)=In(1,(i-1)*N/m+N/(2*m));
end;
subplot(2,1,2);  %  比较误码
plot(an,'r*');hold on;
axis([1  m -2 2]);
plot(a,'b^');