import cv2
import numpy as np  # Không dùng trực tiếp: lọc ảnh chuyển sang detect_orange_ball.
from black_dectection import get_limits          # get_orange_limits, detect_orange_ball

# Truyền ba tham số theo thứ tự B, G, R của mẫu màu cam.
color=[72,66,159]  # màu đỏ
camera = cv2.VideoCapture(0)  # nguồn camera

ret = True  # đọc camera thành công trả true >< false
location_old = None  # ví trí cũ của vật
while ret :
    ret , frame = camera.read()
    if ret == False :
        print("Đọc camera lỗi")
        break


    # XỬ LÍ ẢNH 

    frame_hsv = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)

    low_color , high_color = get_limits(color)  # lấy ngưỡng màu 

    frame_thres = cv2.inRange(frame_hsv , low_color , high_color )   


    contours , abc = cv2.findContours(frame_thres , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)


    for i in contours :
        print(cv2.contourArea(i))     # diện tích các vật nhận diện 
        if cv2.contourArea(i)>=300:  
            if i is not None:
                x1,y1,w,h = cv2.boundingRect(i)       # tìm hình chữ nhật bao quanh vật thể

                #tọa độ tâm:
                x=x1+(w//2)
                y=y1+(h//2)
            location_new=(x,y) # tọa độ tâm mới
            if location_old is not None:   # từ lần thứ 2 đọc tâm trở đi
               d1=location_new[0]-location_old[0]
               d2=location_new[1]-location_old[1]
               dx=(d1**2 + d2**2)**0.5
               cv2.putText(frame , f"Độ dịch chuyển {dx:.2f}" , (30,30) ,cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0) , 1)

            location_old=location_new
            cv2.rectangle(frame , (x1,y1) , (x1+w,y1+h) , (255,0,0) , 2)    # vẽ hình bao quanh

            cv2.circle(frame,(x,y),5,(255,0,0),-1)      # vẽ tâm

           # vẽ chữ
            cv2.putText(frame,f"x={ x } y={ y }", (x+w//2+10,y),cv2.FONT_HERSHEY_COMPLEX , 0.5 ,(0,0,0),1) 

    cv2.imshow("thres",frame_thres)
    cv2.imshow("main",frame)
    if cv2.waitKey(40) & 0xFF == ord('q') : break

camera.release()
cv2.destroyAllWindows()



