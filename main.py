import cv2
import numpy as np  
from color_detection import get_limits          # get_orange_limits, detect_orange_ball

def reset():
    global location_old
    location_old = None
    trajectory.clear()
    print("NOT DETECTED")


color=[78,65,150]  # màu đỏ
camera = cv2.VideoCapture(1)  # nguồn camera

ret = True  # đọc camera thành công trả true >< false
location_new = None
location_old = None  # ví trí cũ của vật
trajectory   = [] # list quỹ đạo
while ret :
    ret , frame = camera.read()
    if ret == False :
        print("Đọc camera lỗi")
        break

    # XỬ LÍ ẢNH 

    frame_hsv = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)   # chuyển về màu hssv

    low_color , high_color = get_limits(color)           # lấy ngưỡng màu từ hàm get_limits

    frame_thres = cv2.inRange(frame_hsv , low_color , high_color )   # đưa các  điểm có trong ngưỡng màu low high lên 1 (sáng), còn lại về 0 (tối) 

    contours , abc = cv2.findContours(frame_thres , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)   # tìm tọa độ các contours

    if (len(contours)>0):
        biggest = max (contours , key = cv2.contourArea)   # tìm max
        if cv2.contourArea(biggest)>300:  
            x1,y1,w,h = cv2.boundingRect(biggest)       # tìm hình chữ nhật bao quanh vật thể lớn nhất

            #tọa độ tâm:
            x=x1+(w//2)
            y=y1+(h//2)
            location_new=(x,y)     # tọa độ tâm mới

            trajectory.append((x,y))

            # tính độ dịch chuyển 
            if location_old is not None:   # từ lần thứ 2 đọc tâm trở đi
               d1=location_new[0]-location_old[0]
               d2=location_new[1]-location_old[1]
               dx=(d1**2 + d2**2)**0.5     # độ dịch chuyển
               cv2.putText(frame , f"Độ dịch chuyển {dx:.2f}" , (30,30) ,cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0) , 1)
            location_old=location_new

            # vẽ chữ tọa độ vật
            cv2.putText(frame,f"x={ x } y={ y }", (x+w//2+10,y),cv2.FONT_HERSHEY_COMPLEX , 0.5 ,(0,0,0),1) 

            # hình chữ nhật bao quanh
            cv2.rectangle(frame , (x1,y1) , (x1+w,y1+h) , (255,0,0) , 2)  

            # vẽ tâm
            cv2.circle(frame,(x,y),5,(255,0,0),-1)

            for i in range(len(trajectory)-1):
                cv2.line(frame,trajectory[i],trajectory[i+1],(255,0,0),1)

        else : reset() # nếu contours max bé hơn 300
    else : reset()   # nếu ko tìm thấy contours

    cv2.imshow("thres",frame_thres)
    cv2.imshow("main",frame)
    if cv2.waitKey(40) & 0xFF == ord('q') : break

camera.release()
cv2.destroyAllWindows()

