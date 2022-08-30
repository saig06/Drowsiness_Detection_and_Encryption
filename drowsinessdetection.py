import cv2
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from keras.models import load_model
import numpy as np
import time
from datetime import datetime

c=0
n=5

face = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_alt.xml')
leye = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_lefteye_2splits.xml')
reye = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_righteye_2splits.xml')

lbl = ['Close', 'Open']

model = load_model('D:\Drowsiness detection\models\cnncat2.h5')
path = os.getcwd()
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
count = 0
score = 0
thicc = 2
rpred = 99.0
lpred = 99.0

while (True):
    ret, frame = cap.read()
    height, width = frame.shape[:2]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face.detectMultiScale(gray, minNeighbors=5, scaleFactor=1.1, minSize=(25, 25))
    left_eye = leye.detectMultiScale(gray)
    right_eye = reye.detectMultiScale(gray)

    cv2.rectangle(frame, (0, height - 50), (200, height), (0, 0, 0), thickness=cv2.FILLED)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 1)

    for (x, y, w, h) in right_eye:
        r_eye = frame[y:y + h, x:x + w]
        count = count + 1
        r_eye = cv2.cvtColor(r_eye, cv2.COLOR_BGR2GRAY)
        r_eye = cv2.resize(r_eye, (24, 24))
        r_eye = r_eye / 255
        r_eye = r_eye.reshape(24, 24, -1)
        r_eye = np.expand_dims(r_eye, axis=0)
        rpred = model.predict(r_eye)
        if (rpred[0][0]<0.3):
            lbl = 'Open'
        if (rpred[0][0]>=0.3):
            lbl = 'Closed'
        break

    for (x, y, w, h) in left_eye:
        l_eye = frame[y:y + h, x:x + w]
        count = count + 1
        l_eye = cv2.cvtColor(l_eye, cv2.COLOR_BGR2GRAY)
        l_eye = cv2.resize(l_eye, (24, 24))
        l_eye = l_eye / 255
        l_eye = l_eye.reshape(24, 24, -1)
        l_eye = np.expand_dims(l_eye, axis=0)
        lpred = model.predict(l_eye)
        if (lpred[0][0]<0.3):
            lbl = 'Open'
        if (lpred[0][0]>=0.3):
            lbl = 'Closed'
        break

    if (rpred[0][0]>=0.3 and lpred[0][0]>=0.3):
            score = score + 1
            eyestate=0
            cv2.putText(frame, "Closed", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
    # if(rpred[0]==1 or lpred[0]==1):
    else:
        score = score - 1
        eyestate=1
        cv2.putText(frame, "Open", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

    if (score < 0):
        score = 0

    cv2.putText(frame, 'Score:' + str(score), (100, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
    t="D:\Drowsiness detection\CapturedImages\image"

    if (score > n):
        cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), thicc)
        if(score==n+1 and eyestate==0):
            ct = datetime.now()
            ctstr = ct.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            c = c+1
            t = t+str(c)
            cv2.putText(frame, ctstr , (10, height-450 ), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.imwrite((t+'.png'),frame)

        # cv2.imwrite(os.path.join(path, 'image.jpg'), frame)
        
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    if cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
f = open("D:\Drowsiness detection\count.txt", "w")
strc=str(c)
f.write(strc)
f.close()
exec(open("D:\Drowsiness detection\AESE.py").read())