import cv2
import base64
import numpy as np
import json
import sys

def encodejpg(img):

    retval, buffer = cv2.imencode('.jpg', img)

    jpg_as_text = base64.b64encode(buffer)

    #print("from size: ", sys.getsizeof(buffer), " to: ", sys.getsizeof(jpg_as_text))
    #print("raw json size: ", sys.getsizeof(json.dumps(buffer.tolist())))
    return jpg_as_text

def decodejpg(text):

    jpg = base64.b64decode(text)

    jpg_np = np.frombuffer(jpg, dtype=np.uint8)

    img = cv2.imdecode(jpg_np, flags=1)

    return img

if __name__ == "__main__":

    #img = cv2.imread("../images/sparse_sample_color.png")
    img = cv2.imread("./debug.jpg")

    text = encodejpg(img)

    img_rec = decodejpg(text)

    cv2.imshow("debug", img_rec)

    cv2.waitKey()