% subcarrier_time_domain.m
% 绘制OFDM的Nc个子载波在时域上的波形
% 参考资料：4G: LTE/LTE-Advanced for Mobile Broadband Second Edition – \
% “CHAPTER 3 OFDM Transmission”,理解e^(j * 2 * pi (k / T)t )对应的时域部分
% 最后修改时间2016.07.30
clear
 
Tu = 2 * pi;    % OFDM周期
st = 0.0;       % OFDM符号开始时间
sp = 0.01;      % 从OFDM的开始时间到结束时间的步长
ed = Tu + st;   % OFDM符号的结束时间
 
t = st : sp : ed; % x轴
 
fn = 0;
fn = fn + 1;
figure(fn);
plot(t, cos(0 * t), t, cos(1 * t), t, cos(2 * t), t, cos(3 * t)); % 子载波Nc = 4
grid on;
xlabel('t');ylabel('A');
title(['N_c = 4, T_u= ', num2str(Tu)]);





% subcarrier_frequency_domain.m
% 绘制OFDM子载波的频谱
% 首先理解“频谱”的含义
% 然后理解OFDM子载波时域波形定长周期中的频谱：
% [1] 余弦函数的频谱（率）为一个冲激,定周期的余弦函数相当于在时域乘以一个矩形窗
% [2] 矩形窗的频谱为sinc函数（未用fft变换来求，而是直接写出了周期为2pi或pi的矩形窗函数函数的频谱函数sinc(2pi)和sinc(pi)）
% [3] 时域乘法相当于频域卷积
% 最后修改时间2016.07.31
 
clear
Tu  = pi;           % 2 * pi
fx  = 3 * Tu;       % 用来显示子载波频谱的频率轴的长度
sf  = 0;
sp  = 0.01;           % 频率变化的步长
f   = sf - fx / 2 : sp : fx / 2; % 自动脑补傅里叶变换后的负频率的出现（请教一个真正懂负频率出现的人）
z   = zeros(1, length(f));
 
fn = 0;
fn = fn + 1;    % 当要绘制多图时方便计数
figure(fn);
% 周期为T的矩形窗的频谱函数为sinc(T * x)
plot(f, z,f, sinc(Tu * f + 0), f, sinc(Tu * (f - 1 / Tu)), f, sinc(Tu * (f - 2 / Tu)), f, sinc(Tu * (f - 3 / Tu))); %, f, sinc(Tu * (f + 3 / Tu)), f, sinc(Tu * (f + 2 / Tu)), f, sinc(Tu * (f + 1 / Tu)), 
grid on;
xlabel('f');ylabel('A');
title(['N_s = 4, T_u= ', num2str(Tu)]);




% subcarrier_sample_value.m
% 参考资料：4G: LTE/LTE-Advanced for Mobile Broadband Second Edition –
% “CHAPTER 3 OFDM Transmission”
% 等间隔计算各个子载波上的离散值
% 子载波数Nc = 8,
% 取样点Ns = 8，每隔1取一个样点
% 最后修改时间：2016.07.30
clear
 
Nc  = 8;    % 子载波数目
Nt  = 8;    % OFDM周期，同时以1为单位在子载波上取样点值
ts  = 1;    % 每个子载波开始的时间
myifftmtx = zeros(Nc, Nt);
for m = 1 : Nc          % 第m个子载波
    for t = ts : Nt     % 在周期Nt上以1为单位等间隔取样
        myifftmtx(m, t) = exp( (1i * 2 * pi) * ((m - 1) / Nt) * (t - ts));
    end
end
ifftmtx = conj(dftmtx(8));
 
% isequal(ifftmtx, myifftmtx) %
% 验证子载波取样点是否与对应的ifft矩阵相同（用眼睛看，一一对照两个矩阵中的元素，两个矩阵是相等的；该函数将它们判断为不等，可能是计算精度或其它的原因^_^）





% ofdm_waveform_diagram.m
% @ 仿真ofdm_waveform_diagram_v0.2.viso描述的基本框图
% @ 参考资料：[1] 4G: LTE/LTE-Advanced for Mobile Broadband Second Edition – 
%                   “CHAPTER 3 OFDM Transmission”(3.3)
%             [2] OFDM for Wireless Multimedia Communications - R. van Nee,
%           R. Prasad - Artech House, 2000.pdf（2.2）
%
% @ OFDM符号参数：
%           为OFDM符号分配的带宽 bw  = 10MHz；
%           用于传递信息的子载波数量 Nuc = 600；
%           子载波间隔 Delta_f = 15KHz；
%
% @ 由OFDM符号参数的计算：
%           OFDM符号所占带宽 Nuc * Delta_f = 600 * 15KHz = 9MHz
%           OFDM符号采样频率：采样频率要等于甚至大于OFDM符号频率，以保证对OFDM符号采样的充分（理解采样频率为单位时间采集的数据量），
%           FFT/IFFT点数 Nsp = 1024；如此OFDM的采样频率为Nsp * Delta_f  = 15.36MHz
%           
% @ 文档：ofdm_waveform_diagram_v0.4.docx；（v0.1 - v0.4）
% @ 最后修改时间：2017.07.31
clear
 
% -------------------------------- OFDM参数描述 --------------------------------
Nuc = 600;  % 用于传递数据的子载波数
Nsp = 1024; % 对OFDM符号的采样点，
            %（[1] 大于等于子载波数量；[2] 最好为2^m，方便fft/ifft运算）
% -------------------------------- OFDM参数描述 --------------------------------
 
 
% -------------------------------- 发送端 --------------------------------
% &&&&&&&& generate data source &&&&&&&&
nb  = 2;    % nb-比特数
n   = Nuc;  % nb-比特数的个数
tx_data_source     = generate_data_source( nb, n );
 
% &&&&&&&& generate PSK/QAM symbol &&&&&&&&
mod_type    = 'psk'; % 映射源数据元素的方式
tx_PSKorQAM_symbol  = generate_PSKorQAM_symbol( mod_type, tx_data_source, nb );
 
% &&&&&&&& generate OFDM symbol（IFFT） &&&&&&&&
Nifft    = Nsp;
tx_PSKorQAM_symbol_oversample =      ...
    [tx_PSKorQAM_symbol(1 : Nuc / 2),...
    zeros(1, Nsp - Nuc),             ...
    tx_PSKorQAM_symbol(Nuc / 2 + 1 : end)];                         % 过采样，为何将0加在中间，见[2]
tx_ofdm_symbol     = ifft(tx_PSKorQAM_symbol_oversample, Nifft);    % 将每个数据加载到每个子载波上
% -------------------------------- 发送端 --------------------------------
 
 
% -------------------------------- 信道 --------------------------------
% &&&&&&&& Fading channel &&&&&&&&
rx_ofdm_symbol  = tx_ofdm_symbol;   % 理想信道
% -------------------------------- 信道 --------------------------------
 
 
% -------------------------------- 接收端 --------------------------------
% &&&&&&&& get PSK/QAM symbol（FFT） &&&&&&&&
Nfft    = Nsp;
rx_PSKorQAM_symbol_oversample  = fft(rx_ofdm_symbol, Nfft);
 
% &&&&&&&& get data source &&&&&&&&
rx_PSKorQAM_symbol  = ...
    [rx_PSKorQAM_symbol_oversample(1 : Nuc / 2),...
    rx_PSKorQAM_symbol_oversample(end - Nuc / 2 + 1 : end)];  % 去掉过采样数据
rx_data_source      = demodulate_PSKorQAM_symbol( rx_PSKorQAM_symbol, mod_type, nb );
% -------------------------------- 接收端 --------------------------------
 
% 判断OFDM符号的解析是否成功
isequal(tx_data_source, rx_data_source)
