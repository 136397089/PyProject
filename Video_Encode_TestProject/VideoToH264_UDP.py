import av
import cv2
import socket
import numpy as np

# 创建一个VideoCapture对象
cap = cv2.VideoCapture(0)

# 创建一个UDP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 定义目标地址和端口
address = ('192.168.1.102', 12345)

# 创建一个AVStream对象
output = av.open('output_stream.mp4', mode='w')
stream = output.add_stream('libx264', rate=15)

# 定义每个UDP数据包的大小
packet_size = 1024

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 将OpenCV的BGR图像转换为RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 创建一个AVFrame对象并将图像数据复制到其中
    av_frame = av.VideoFrame.from_ndarray(frame, format='rgb24')

    # 编码视频帧
    for packet in stream.encode(av_frame):
        # 将编码后的数据包转换为字节
        data = packet.to_bytes()

        # 计算总包数
        total_packets = len(data) // packet_size
        if len(data) % packet_size != 0:
            total_packets += 1

        # 分包发送
        for i in range(total_packets):
            start = i * packet_size
            end = (i+1) * packet_size
            # 添加序号和总包数
            packet_data = bytes([i, total_packets]) + data[start:end]
            sock.sendto(packet_data, address)

# 编码剩余的帧
for packet in stream.encode():
    data = packet.to_bytes()
    total_packets = len(data) // packet_size
    if len(data) % packet_size != 0:
        total_packets += 1

    for i in range(total_packets):
        start = i * packet_size
        end = (i+1) * packet_size
        packet_data = bytes([i, total_packets]) + data[start:end]
        sock.sendto(packet_data, address)

# 释放VideoCapture
cap.release()

# 关闭所有窗口
cv2.destroyAllWindows()

# 关闭套接字
sock.close()
