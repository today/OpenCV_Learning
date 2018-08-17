# coding=utf-8
#OpenCV 相关
import cv2
import numpy as np

#网络相关
import urllib2
import json

videos = ["E:\\aa.mp4","E:\\cctv.mp4","E:\\hz.mp4","E:\\tw.mp4","E:\\180.mkv","E:\\ghost.webm"]
path = videos[1]

#cap = cv2.VideoCapture(path)
cap = cv2.VideoCapture(0)
if not cap :
    exit()

# 新建一个MOG背景减除对象
fgbg = cv2.createBackgroundSubtractorMOG2()

# 新建一个卷积核用于开运算
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

while 1:
    ret, frame = cap.read()
    cv2.imshow('frame2', frame)

    # print type(frame)
    # print frame.dtype
    (width, height, dimensional) = frame.shape

    if frame is None:
        cv2.waitKey(0)
        break
    else:
        # 应用MOG到每一帧，返回结果是动目标的掩膜
        fgmask = fgbg.apply(frame)
        # 利用开运算进行噪声去除
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        
        # 对图像进行二值化，只保留灰色的部分，并且把灰色部分置为白色；其他黑色和白色的部分都变为黑色。
        #th = cv2.inRange(fgmask, 100, 200)  
        th = fgmask
        
        # 寻找图中轮廓
        cnts = cv2.findContours(th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        # 如果存在至少一个轮廓则进行如下操作
        if len(cnts) > 0:
            # 找到面积最大的轮廓
            c = max(cnts, key=cv2.contourArea)
            # 使用最小外接圆圈出面积最大的轮廓
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            # 计算轮廓的矩
            M = cv2.moments(c)
            # 计算轮廓的重心
            center = (0,0)
            if M["m00"] != 0 :
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            
            #print center
            # 只处理尺寸足够大的轮廓
            if radius > 40:
                # 画出最小外接圆
                cv2.circle(th, (int(x), int(y)), int(radius), (255, 255, 255), 5)
                # 画出重心
                cv2.circle(th, center, 5, (0, 0, 255), -1) 

                # 在这里把座标数据发送到服务器。
                data = {
                    'x': (y/width),    #640
                    'y': (x/height),     #480
                    'p': int(radius)
                }
                print width
                print height
                print data
                headers = {'Content-Type': 'application/json'}
                # req_url = "http://192.168.6.97:8000/step/"
                req_url = "http://127.0.0.1:8000/step/"
                request = urllib2.Request(url=req_url, headers=headers, data=json.dumps(data))
                response = urllib2.urlopen(request)


        # output video
        cv2.imshow('frame', th)
        
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

cap.release()
cv2.destroyAllWindows()