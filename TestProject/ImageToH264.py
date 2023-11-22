
import cv2

# 创建一个VideoCapture对象
cap = cv2.VideoCapture(0)

# 定义编码器并创建VideoWriter对象
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    type(frame)
    # 写入帧
    out.write(frame)

    # 显示帧
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

# 释放VideoCapture和VideoWriter
cap.release()
out.release()

# 关闭所有窗口
cv2.destroyAllWindows()
