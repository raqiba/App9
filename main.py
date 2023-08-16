import time
import cv2
from send_email import email_sent
import glob
import os

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list=[]
count=0


def clean_folder():
    images=glob.glob("images/*.png")
    for image in images:
        os.remove(image)

while True:

    status=0

    check,frame=video.read()
    gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grey_scale_gau = cv2.GaussianBlur(gray_scale,(21,21),0)

    if first_frame is None:
        first_frame = grey_scale_gau

    change = cv2.absdiff(first_frame, grey_scale_gau)
    black_white = cv2.threshold(change,55,255,cv2.THRESH_BINARY)[1]
    dil_image=cv2.dilate(black_white,None, iterations=2)
    cv2.imshow("my video", dil_image)

    contours,check = cv2.findContours(black_white,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour)<5000:
            continue
        x,y,w,h = cv2.boundingRect(contour)
        object = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
        cv2.imwrite(f"images/{count}.png", object)
        count = count + 1

        all_images=glob.glob("images/*.png")
        mid_image=int(len(all_images)/2)
        image=all_images[mid_image]

        if object.any():
            status = 1

    status_list.append(status)
    status_list=status_list[-2:]
    if status_list[0] ==1 and status_list[1]==0:
        email_sent()
        clean_folder()

    cv2.imshow("Video", frame)
    key= cv2.waitKey(1)
    if key == ord("q"):
        break
video.release()
