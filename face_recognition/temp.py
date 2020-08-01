from face_recognition import db
from face_recognition.models import Student_details, Leaving_details, History,Campus_exit
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,update,column, Integer, String, Table, select, delete
import sqlite3
# from flask_login import login_user, current_user
from numpy import array
import face_recognition
import cv2
import matplotlib.pyplot as plt
import numpy as np
import  time
from datetime import datetime
import os

def register_face(enroll):
    video_capture = cv2.VideoCapture(0)

    flag=0
    count=0
    # face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    name="Unknown"
    string = enroll + ".jpeg"
    while True:
        # print('Entered')
        face_locations = []
        ret, frame = video_capture.read()
        # print('ret-frame', ret, frame)
      # os.chdir("/home/rsvi/Desktop/Mini_Project_sem5/face_recognition-master/examples")
        os.chdir("/home/ravi/Desktop/Mini/face_recognition-master/")
        if ret:
            cv2.imwrite(string, frame)
        else:
            break
        
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            name="Unknown"
            face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # print('I am in for loop.')
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # print('CV2.rectangle')            
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # print('I\'m out')
        cv2.imshow('Video', frame)
        # print('I am out of for loop')
        
        if cv2.waitKey(1) & 0xFF == ord('q') and len(face_locations)==1:
            # print('Time to break 2')
            break


    # print('Capturing video')
    video_capture.release()
    cv2.destroyAllWindows()
    # print('Time to return')
    return True
# if __name__ == "__main__":
#     main()

def recognize_face():
    video_capture = cv2.VideoCapture(0)
    connection = sqlite3.connect('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/proj_database.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT enrol FROM student_details""")
    position_query = cursor.fetchall()
    known_face_encodings =[]
    known_face_names = []
    for enroll in position_query:
        string = str(enroll[0] + ".jpeg")
        image = face_recognition.load_image_file(string)
        image_encoding=face_recognition.face_encodings(image)[0]
        known_face_encodings.append(image_encoding)
        known_face_names.append(enroll)
    # Create arrays of known face encodings and their names
    
    print(known_face_names)
    print("\n")
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    name="Unknown"
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            # plt.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            print("in_loop") 
        
        # Display the resulting image
        print("before_inshow")
        cv2.imshow('Video', frame)
        print("after_inshow")
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # if name!="Unknown" :
        if len(face_encodings)!=0:
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    if name=="Unknown":
        return name
    return name[0]

def show_details(enrol):
    connection = sqlite3.connect('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/proj_database.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Student_details WHERE enrol='{}';""".format(enrol))
    student = cursor.fetchall()
    if len(student) == 0:
        return False
    else:
        return student[0]

def check_unique(enrol,contact):
    connection = sqlite3.connect('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/proj_database.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Student_details WHERE enrol='{}';""".format(enrol))
    student_enrol = cursor.fetchall()
    cursor.execute("""SELECT * FROM Student_details WHERE contact='{}';""".format(contact))
    student_contact = cursor.fetchall()
    if len(student_enrol)==0 and len(student_contact)==0:
        return 0
    if len(student_enrol)!=0 and len(student_contact)==0:
        return 1
    if len(student_enrol)==0 and len(student_contact)!=0:
        return 2
    else:
        return 3


 

def update_room(enrol, room):
    student = Student_details.query.filter_by(enrol = enrol).first()
    if (student)==None:
        return False
    student.room_num = room
    db.session.commit()  
    return True

def update_contact(enrol, contact):
    student = Student_details.query.filter_by(enrol = enrol).first()
    if (student)==None:
        return False
    student.contact = contact
    db.session.commit()
    return True

def update_parent_contact(enrol, parent_contact):
    student = Student_details.query.filter_by(enrol = enrol).first()
    if (student)==None:
        return False
    student.parent_contact = parent_contact
    db.session.commit()
    return True

def delete_single(enrol):
    Student_details.query.filter_by(enrol = enrol).delete()
    string = enrol + ".jpeg"
    try:
        os.remove(string)
    except:
        pass
    db.session.commit()
    return True

def delete_batch(year):
    connection = sqlite3.connect('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/proj_database.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT enrol FROM Student_details""")
    students = cursor.fetchall()
    for student in students:
        s = student[0] +".jpeg"
        try:
            os.remove(s)
        except:
            pass
        string = student[0][3:7]
        if string==year:
            Student_details.query.filter_by(enrol = student[0]).delete()
            db.session.commit()
    return True

def search_by_enrol(enrol):
    connection = sqlite3.connect('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/proj_database.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Leaving_details WHERE enrol_num='{}';""".format(enrol))
    student_leave = cursor.fetchall()
    cursor.execute("""SELECT * FROM History WHERE enrol='{}';""".format(enrol))
    student_history = cursor.fetchall()
    if len(student_leave)==0 and len(student_history)==0:
        return False
    final_query_list=[]
    for tups in student_leave:
        l=[]
        i=0
        for item in tups:
            s=""
            t=""
            if i==2:
                s = item[0:10]
                t = item[11:16]
                l.append(s)
                l.append(t)
            else:
                l.append(item)
            i=i+1
        l.append("------")
        l.append("------")
        final_query_list.append(l)
    for tups in student_history:
        l=[]
        flag=0
        i=0
        for item in tups:
            if flag==0:
                flag=1
                continue
            s=""
            t=""
            if i==2 or i==3:
                s = item[0:10]
                t = item[11:16]
                l.append(s)
                l.append(t)
            else:
                l.append(item)
            i=i+1
        final_query_list.append(l)
    return final_query_list

def search_by_date(date):
    connection = sqlite3.connect('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/proj_database.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Leaving_details""")
    student_leave = cursor.fetchall()
    cursor.execute("""SELECT * FROM History""")
    student_history = cursor.fetchall()
    if len(student_leave)==0 and len(student_history)==0:
        return False
    final_query_list=[]
    for tups in student_leave:
        string = tups[2][0:10]
        if(string!=date):
            continue
        l=[]
        i=0
        for item in tups:
            s=""
            t=""
            if i==2:
                s = item[0:10]
                t = item[11:16]
                l.append(s)
                l.append(t)
            else:
                l.append(item)
            i=i+1
        l.append("------")
        l.append("------")
        final_query_list.append(l)
    for tups in student_history:
        string = tups[3][0:10]
        if(string!=date):
            continue
        l=[]
        flag=0
        i=0
        for item in tups:
            if flag==0:
                flag=1
                continue
            s=""
            t=""
            if i==2 or i==3:
                s = item[0:10]
                t = item[11:16]
                l.append(s)
                l.append(t)
            else:
                l.append(item)
            i=i+1
        final_query_list.append(l)
    return final_query_list


def search_outside():
    connection = sqlite3.connect('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/proj_database.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Leaving_details""")
    student_leave = cursor.fetchall()
    if len(student_leave)==0:
        return False
    final_query_list=[]
    for tups in student_leave:
        l=[]
        i=0
        for item in tups:
            s=""
            t=""
            if i==2:
                s = item[0:10]
                t = item[11:16]
                l.append(s)
                l.append(t)
            else:
                l.append(item)
            i=i+1
        l.append("------")
        l.append("------")
        final_query_list.append(l)
    return final_query_list

def check(enrol):
    connection = sqlite3.connect('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/proj_database.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Leaving_details WHERE enrol_num='{}';""".format(enrol))
    student = cursor.fetchall()
    if len(student) == 0:
        return False
    else:
        return True

def make_history(enrol):
    connection = sqlite3.connect('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/proj_database.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Leaving_details WHERE enrol_num='{}';""".format(enrol))
    student = cursor.fetchall()
    l=[]
    for tups in student:
        for item in tups:
            l.append(item)
        date=datetime.today()
        l.append(str(date))
    student = History(enrol=l[0], destination=l[1], dep_date_time=l[2], arr_date_time=l[3])
    db.session.add(student)
    db.session.commit()
    Leaving_details.query.filter_by(enrol_num =enrol).delete()
    db.session.commit()

def main_exit(enrol):
    connection = sqlite3.connect('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/proj_database.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Campus_exit WHERE enrol_num='{}';""".format(enrol))
    student = cursor.fetchall()
    if len(student) == 0:
        return False
    else:
        Campus_exit.query.filter_by(enrol_num =enrol).delete()
        db.session.commit()
        return True