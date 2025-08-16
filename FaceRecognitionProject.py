from datetime import datetime
import mysql.connector as sqltor

connection_object = sqltor.connect(host='localhost', user='root', password='08289', database='facerecognition')

if connection_object.is_connected():
    print("Connection established successfully...")
else:
    print("Error while connecting the database...")
    
import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime
 
video_capture = cv2.VideoCapture(0)
 
jobs_image = face_recognition.load_image_file("jobs.jpg")
jobs_encoding = face_recognition.face_encodings(jobs_image)[0]
 
ratan_tata_image = face_recognition.load_image_file("ratan.jpg")
ratan_tata_encoding = face_recognition.face_encodings(ratan_tata_image)[0]
 
sadmona_image = face_recognition.load_image_file("sadmona.jpg")
sadmona_encoding = face_recognition.face_encodings(sadmona_image)[0]
 
tesla_image = face_recognition.load_image_file("tesla.jpg")
tesla_encoding = face_recognition.face_encodings(tesla_image)[0]
 
known_face_encoding = [
jobs_encoding,
ratan_tata_encoding,
sadmona_encoding,
tesla_encoding
]
 
known_faces_names = [
"jobs",
"ratan",
"sadmona",
"tesla"
]
 
students = known_faces_names.copy()
 
face_locations = []
face_encodings = []
face_names = []
s=True
 
 
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
 
cursor_object = connection_object.cursor()
query="DROP TABLE IF EXISTS `facerecognition`.`{}`".format(current_date)
cursor_object.execute(query)
query="create table `facerecognition`.`{}` (name char(20), time TIME)".format(current_date)
cursor_object.execute(query)



while True:
    _,frame = video_capture.read()
    small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    rgb_small_frame = small_frame[:,:,::-1]
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding,face_encoding)
            name=""
            face_distance = face_recognition.face_distance(known_face_encoding,face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]
 
            face_names.append(name)
            if name in known_faces_names:
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (10,100)
                fontScale              = 1.5
                fontColor              = (255,0,0)
                thickness              = 3
                lineType               = 2
 
                cv2.putText(frame,name+' Present', 
                    bottomLeftCornerOfText, 
                    font, 
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)
 
                if name in students:
                    students.remove(name)
                    print(students)
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    query="insert into `facerecognition`.`{}` values (%s,%s)".format(current_date)
                    cursor_object.execute(query,(name,current_time))
                    connection_object.commit()
    cv2.imshow("attendence system",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
video_capture.release()
cv2.destroyAllWindows()

