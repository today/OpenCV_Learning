# coding=utf-8
import cv2

cap = cv2.VideoCapture(0)

# 指定FourCC编码是XVID，注意cv2和cv里的函数名不太一样，现在用cv2了
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# 指定文件输出路径、编码、帧率以及每一帧的大小，还有最后一个可选参数isColor。
out = cv2.VideoWriter("test.avi", fourcc, 20.0, (640, 480))

while 1:
    ret, frame = cap.read()
    if frame is None:
        break
    else:
        # 在获取每一帧并进行处理后，进行输出
        out.write(frame)
        cv2.imshow("video", frame)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

cap.release()
# 最后别忘了释放掉VideoWriter
out.release()