import cv2

video_file = "./tmp_img/depth.mov"
v = cv2.VideoCapture(video_file)

while True:
    _, frame = v.read()
    w = frame.shape[1]
    h = frame.shape[0]
    #print(w, h)
    image = cv2.GaussianBlur(cv2.pyrDown(frame, (w/2, h/2)), (51, 51), 20)
    
    try:
        cv2.imshow("disply", frame)
    except:
        break
    cv2.waitKey(20)

