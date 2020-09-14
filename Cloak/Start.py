import numpy as np
import cv2
import time

count = 0
cap = cv2.VideoCapture(0)
time.sleep(2)

background = 0

for i in range(30):
    ret, background = cap.read()
background = np.flip(background, axis = 1)

while(cap.isOpened()):
    ret,image = cap.read()

    if not ret:
        break
    count += 1
    image = np.flip(image, axis=1)

    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    lower_red = np.array([0,120,70])
    upper_red = np.array([10,255,255])
    mask1 = cv2.inRange(hsv,lower_red, upper_red)

    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask2 = cv2.inRange(hsv,lower_red, upper_red)

    mask1 = mask1 + mask2

    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations=1)
    mask2 = cv2.bitwise_not(mask1)

    final1 = cv2.bitwise_and(background,background,mask = mask1)
    final2 = cv2.bitwise_and(image,image,mask = mask2)


    final_output = cv2.addWeighted(final1,1,final2,1,0)

    cv2.imshow("Camera", final_output)
    if cv2.waitKey(10) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()