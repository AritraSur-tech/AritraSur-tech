import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime

video_capture =cv2.VideoCapture(0)

me = face_recognition.load_image_file("face/pic.jpg")
e = face_recognition.face_encodings(me)[0]


kfencode = [e]
knames = ["Aritra"]

stu = knames.copy()


face_locations = []
face_encodings = []

now = datetime.now()
curr_date = now.strftime("%y-%m-%d")
f = open(f"{curr_date}", "w+", newline="")
w = csv.writer(f)


while True:
    _, frame = video_capture.read()
    smol = cv2.resize(frame,(0,0), fx = 0.25, fy = 0.25)
    rgb_smol = cv2.cvtColor(smol,cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_smol)
    face_encodings = face_recognition.face_encodings(rgb_smol,face_locations)

    for face_encodings in face_encodings:
        matches = face_recognition.compare_faces(kfencode, face_encodings)
        face_d = face_recognition.face_distance(kfencode, face_encodings)
        best = np.argmin(face_d)

        if matches[best]:
            name = knames[best]

        if name in knames:
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerofText = (10,100)
            fontScale = 1.5
            fontColor = (255,0,0)
            thickness = 3
            lineType = 2
            cv2.putText(frame, name + " Present", bottomLeftCornerofText, font, fontScale, fontColor,thickness,lineType)

            if name in stu:
                stu.remove(name)
                curr_time = now.strftime("%h-%M-%S")
                w.writerow([name,curr_time])



    cv2.imshow("attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()













