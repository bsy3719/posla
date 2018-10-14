import cv2

cap = cv2.VideoCapture(0)
i = 1
while True:
    _, img = cap.read()
    cv2.imshow("capturing", img)
    cv2.imwrite('capture/ red_light%d.jpg'%i, img)
    i += 1
    print(i)
    if cv2.waitKey(1) == 27:
        break
    elif i == 1000:
        break
cap.release()
cv2.destroyAllWindows()