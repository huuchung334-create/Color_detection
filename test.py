import cv2
import numpy as np

pic = cv2.imread(r'C:\picture\chimse.webp')

pic = pic[100:300,100:600]

pic = cv2.cvtColor( pic , cv2.COLOR_BGR2HSV )

cv2.imshow("main",pic)
cv2.waitKey(0)