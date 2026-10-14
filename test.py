# import cv2
# import numpy as np
# from color_detection import get_limits

# pic = cv2.imread(r'C:\picture\chimse.webp')

# # pic = pic[100:300,100:600]

# pic = cv2.cvtColor( pic , cv2.COLOR_BGR2HSV )



# cv2.imshow("main",pic)
# cv2.waitKey(0)

# import numpy as np
# import cv2

# camera = cv2.VideoCapture(1)
# ret=True
# while ret:
#     ret,frame = camera.read()


#     cv2.imshow("sdgg",frame)
#     cv2.waitKey(40)
c=3
def cong(a , b):
    global c
    c= a+b

def nhan():
    global c
    c+=4

nhan()
print(c)