import numpy as np
import cv2

ind = 1

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 100, 0])
    upper_red = np.array([5, 255,255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame,frame, mask=mask)

    cv2.imshow('red', res)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        status = cv2.imwrite(r"..\mech_python\plansza{}.jpg".format(ind), frame)
        print("zdjecie: {}".format(status))
        ind = ind + 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()q