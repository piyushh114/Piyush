import numpy as np
import cv2
import face_recognition as face_rec
import os
from datetime import datetime
import pyttsx3 as textspeech
from tkinter import *
from PIL import ImageTk, Image
root=Tk()

def AD():

    engine=textspeech.init()

    def resize(img,size):
        width=int(img.shape[1]*size)
        height=int(img.shape[0]*size)
        dimension=(width,height)
        return cv2.resize(img,dimension,interpolation=cv2.INTER_AREA)

    path='C:/Users/Anurag Kumar/Music/images'
    studentimg=[]
    studentname=[]

    myList=os.listdir(path)
    #print(myList)
    for cl in myList:
        currentImg=cv2.imread(f'{path}\{cl}')# student images/ashish.jpg
        studentimg.append(currentImg)
        studentname.append(os.path.splitext(cl)[0])
    #print(studentname)

    def finEncoding(image):
        encodings_list=[]
        for img in image:
            img=resize(img,0.50)
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encoding=face_rec.face_encodings(img)[0]
            encodings_list.append(encoding)
        return encodings_list

    def Markattendance(name):
        with open('C:/Users/Anurag Kumar/Music/att.csv','r+') as f:
            myList=f.readlines()
            nameList=[]
            for line in myList:
                entry=line.split(',')
                nameList.append(entry[0])
            if name not in nameList: # to add the name in csv file if not prsent in list
                now=datetime.now()
                timestr=now.strftime('%H:%M')
                f.writelines(f'\n{name},{timestr}')

                # textspeech 
                statment=str('Welcome to class'+name)
                engine.say(statment)
                engine.runAndWait()


    encodings_list=finEncoding(studentimg)

    vid=cv2.VideoCapture(0) # start video from webcam

    while True:
        sucess,frame=vid.read()
        frames=cv2.resize(frame,(0,0),None,0.25,0.25)
        frames=cv2.cvtColor(frames,cv2.COLOR_RGB2BGR)

        faces_in_frame=face_rec.face_locations(frames)
        encode_in_frame=face_rec.face_encodings(frames,faces_in_frame)

        for encodeFace,faceloc in zip(encode_in_frame,faces_in_frame):
            matches=face_rec.compare_faces(encodings_list, encodeFace)
            facedis=face_rec.face_distance(encodings_list,encodeFace)
            print(facedis)
            matchIndex=np.argmin(facedis)

            if matches[matchIndex]:
                name=studentname[matchIndex].upper()
                y1,x2,y2,x1=faceloc
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)            
                cv2.rectangle(frame,(x1,y2-25),(x2,y2),(0,255,0),cv2.FILLED)   
                cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                Markattendance(name)
        cv2.imshow('video',frame)
        cv2.waitKey(1)      
root.title("Smart Attendance System")
root.geometry('2060x860')
root.config(bg='green') 

lb=Label(root,text="Smart Attendance Using AI",font=("Times New Roman",30,"bold"),border=5,bg='blue').pack()
But=Button(root,text="Press Me for Attendance",font=("Time New Roman",25),border=5,command=lambda:AD())
But.pack()

frame = Frame(root, width=600, height=400)
frame.pack()
frame.place(anchor='e', relx=0.5, rely=0.5)
img = ImageTk.PhotoImage(Image.open("ag.jpeg"))
label = Label(frame, image = img)
label.pack()

lb2=Label(root,text='''Group 7 Final Project
1.Ashish Kumar   -00915608220
2.Piyush         -02515608220
3.Lalit Kishore  -00196207420
4.Md. Anas Ali   -04215602820''',font=("Times New Roman",30,'bold')).pack(side=RIGHT)

root.mainloop()