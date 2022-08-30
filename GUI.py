from tkinter import *
from tkinter import messagebox
import os
import os.path
from os.path import isfile
import time

def checkpwd():
    pwd = e.get()
    if(len(pwd)==0):
        f=0
        messagebox.showinfo("Warning", "Empty password is not accepted")
    print(pwd)
    f = open("D:\Drowsiness detection\ptext.txt", "r")
    p = f.read()
    f.close()
    if(p == pwd):
        frame.destroy()
        exec(open("D:\Drowsiness detection\drowsinessdetection.py").read())
    else:
        if f==1:
            messagebox.showinfo("Warning", "Password mismatch!")

def savepwd():
    pwd = e.get()
    if(len(pwd)==0):
        messagebox.showinfo("Warning", "Empty password is not accepted")
    print(pwd)
    f = open("D:\Drowsiness detection\ptext.txt", "w")
    f.write(pwd)
    f.close()
    frame.destroy()
    
f=1
start=time.time()
os.chdir('D:\Drowsiness Detection')

if os.path.isfile('ptext.txt'):
    frame = Tk()
    frame.geometry('450x400')
    frame.title("Login")
    l = Label(text="Enter your password").place(x=167,y=75)
    e = Entry(frame,show='*',font=('Arial', 14))
    e.pack(padx=112.5,pady=120)
    b = Button(frame,text="Submit",bg="light blue",height=1,width=10,command=checkpwd).place(x=179,y=165)
else:
    frame = Tk()
    frame.geometry('450x400')
    frame.title("Set password")
    l = Label(text="Enter new password").place(x=167,y=75)
    e = Entry(frame,show='*',font=('Arial', 14))
    e.pack(padx=112.5,pady=120)
    b = Button(frame,text="Submit",bg="light blue",height=1,width=10,command=savepwd).place(x=179,y=165)

frame.mainloop()