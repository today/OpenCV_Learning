# coding=utf-8
import cv2

# 新建一个VideoCapture对象，指定第0个相机进行视频捕获
cap = cv2.VideoCapture(0)

# 一直循环捕获，直到手动退出
while 1:
    # 返回两个值，ret表示读取是否成功，frame为读取的帧内容
    ret, frame = cap.read()
    # 判断传入的帧是否为空，为空则退出
    if frame is None:
        break
    else:
        # 调用OpenCV图像显示函数显示每一帧
        cv2.imshow("video", frame)
        # 用于进行退出条件的判断，这里与0xFF进行了与运算，取输入的低八位
        k = cv2.waitKey(1) & 0xFF
        # 27是ESC键，表示如果按ESC键则退出
        if k == 27:
            break

# 释放VideoCapture对象
cap.release()