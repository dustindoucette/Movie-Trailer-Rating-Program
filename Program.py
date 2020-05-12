#This is a Python program that allows users to view movie trailers and answer questions about them
#Author: Dustin Doucette (dustin.doucette@carleton.ca)

#**NOTE** This program must reside in a directory with no spaces in any names
#C:\User\ddouce\Program\Files           GOOD
#C:\User\Tim Johns\Progam\Files         BAD **

from tkinter import *
from PIL import ImageTk, Image
from ctypes import *
from tkinter import messagebox
from os import startfile
import os
import sys
import glob

import pyglet

#windll.shcore.SetProcessDpiAwareness(1)

mainWindow = Tk()
VideoWindow = Toplevel(mainWindow)
VideoWindow.withdraw()
NameWindow = Toplevel(mainWindow)
NameWindow.withdraw()
SelectVideoWindow = Toplevel(mainWindow)
SelectVideoWindow.withdraw()
RatingsWindow = Toplevel(mainWindow)
RatingsWindow.withdraw()
SpecificRatingsWindow = Toplevel(mainWindow)
SpecificRatingsWindow.withdraw()
ThankYouWindow = Toplevel(mainWindow)
ThankYouWindow.withdraw()

#User Details
userFirstName = ''
userLastName = ''

#A list containing all of the movie trailer names
MovieTrailerList = []

#use isFunny.get() to get if it is pressed or not (1 = it is selected, 0 = it is not selected)
isFunny = IntVar()
isScary = IntVar() 
isSexy = IntVar() 

#Set 0 by default
funnyRating = 0
scaryRating = 0
secyRating = 0

def on_closing():
    if messagebox.askokcancel("Exiting Program", "Are you sure you want to quit?"):
        RatingsWindow.destroy()
        mainWindow.destroy()

def endProgram():
    mainWindow.destroy()

RatingsWindow.protocol("WM_DELETE_WINDOW", on_closing)
SpecificRatingsWindow.protocol("WM_DELETE_WINDOW", on_closing)
VideoWindow.protocol("WM_DELETE_WINDOW", on_closing)
SelectVideoWindow.protocol("WM_DELETE_WINDOW", on_closing)    
NameWindow.protocol("WM_DELETE_WINDOW", on_closing) 
ThankYouWindow.protocol("WM_DELETE_WINDOW", endProgram) 

def SayThankYou():
    #Another window will popup at the end thanking the user for their participation
    #RatingsWindow.withdraw()
    ThankYouWindow.update()
    ThankYouWindow.deiconify()

    ThankYouWindow.title("Trailer Viewer Program")
    ThankYouWindow.geometry('500x150')
    ThankYouWindow.minsize(500, 150)
    location = os.getcwd() + "\\Images\\uottawa_ver_black.ico"
    ThankYouWindow.iconbitmap(location)

    lbl = Label(ThankYouWindow, text="Thank you for your participation in \nthe ... experiment, your results are greatly appreciated.\n You may now exit the program. If you would like to \ncomplete another movie trailer, please \nclose and restart the program.", font=(25))
    lbl.config(anchor=CENTER)
    lbl.pack(padx=0, pady=0)

def GetFavouriteParts():
    #This is where another window will pop up, which will ask which part(s) of the movie trailer was the user's favourite
    print("temp")

def GetIndividualFrames():
    #This is where the user will select which parts of the movie trailer were funny
    if(isFunny.get() == 1):
        print("temp")

    #This is where the user will select which parts of the movie trailer were scary
    if(isScary.get() == 1):
        print("temp")

    #This is where the user will select which parts of the movie trailer were sexy
    if(isSexy.get() == 1):
        print("temp")

    #Once the relevant sections have been completed, ask the user for their favourite part(s) of the movie trailer

def CreateSpecificRatingsWindow():
    RatingsWindow.withdraw()

    if((isFunny.get() is 0) and (isScary.get()) and (isSexy.get())):
        print("None Selected")
    else:
        SpecificRatingsWindow.update()
        SpecificRatingsWindow.deiconify()

        print(isFunny.get()) #Funny
        print(isScary.get()) #Scary
        print(isSexy.get()) #Sexy

        rowCount = 1

        if(isFunny.get() == 1):
            lbl7 = Label(SpecificRatingsWindow, text="Funny", font=(25))
            lbl7.grid(sticky="W", column=0, row=rowCount)

            s1 = Scale(SpecificRatingsWindow, from_=1, to=10, orient=HORIZONTAL)
            s1.grid(sticky="W", column=1, row=rowCount)

            rowCount += 1

        if(isScary.get() == 1):
            lbl8 = Label(SpecificRatingsWindow, text="Scary", font=(25))
            lbl8.grid(sticky="W", column=0, row=rowCount)

            s2 = Scale(SpecificRatingsWindow, from_=1, to=10, orient=HORIZONTAL)
            s2.grid(sticky="W", column=1, row=rowCount)

            rowCount += 1

        if(isSexy.get() == 1):
            lbl9 = Label(SpecificRatingsWindow, text="Sexy", font=(25))
            lbl9.grid(sticky="W", column=0, row=rowCount)

            s3 = Scale(SpecificRatingsWindow, from_=1, to=10, orient=HORIZONTAL)
            s3.grid(sticky="W", column=1, row=rowCount)

            rowCount += 1

        btn5 = Button(SpecificRatingsWindow, text="Next", command=GetIndividualFrames, font=(25))
        btn5.grid(column=0, row=rowCount, columnspan=2, pady=10)

def CreateRatingsWindow():
    VideoWindow.withdraw()
    RatingsWindow.update()
    RatingsWindow.deiconify()

def CreateVideoWindow():
    SelectVideoWindow.withdraw()
    VideoWindow.update()
    VideoWindow.deiconify()

    #Movie titles cannot have any spaces and/or special characters
    movieLocation = os.getcwd() + "\\Movie-Trailers\\" + MovieTrailerList[listbox.curselection()[0]] + ".mp4"

    os.system(movieLocation)

def CreateSelectVideoWindow():
    NameWindow.withdraw()
    SelectVideoWindow.update()
    SelectVideoWindow.deiconify()

    userFirstName = firstName.get()
    userLastName = lastName.get() 

def CreateNameWindow():
    mainWindow.withdraw()
    NameWindow.update()
    NameWindow.deiconify()


#Main Menu Window -----------------------------
#This window states the program name and allows the user to begin the experiment

mainWindow.title("Trailer Viewer Program")
mainWindow.geometry('350x250')
mainWindow.minsize(350, 250)
location = os.getcwd() + "\\Images\\uottawa_ver_black.ico"
mainWindow.iconbitmap(location)

#Add UOttawa Logo to login screen
img = Image.open("./Images/uottawa_ver_black.png")
img = img.resize((100, 100), Image.ANTIALIAS) 
img = ImageTk.PhotoImage(img)
panel = Label(mainWindow, image = img)
panel.pack(padx=0, pady=15)

lbl = Label(mainWindow, text="Welcome to the ... Program!", font=(25))
lbl.config(anchor=CENTER)
lbl.pack(padx=0, pady=0)

#-----------------------------------------


#Name Entry Window -----------------------------
#This window allows the user to enter their first and lastname for statistical purposes

NameWindow.title("Trailer Viewer Program")
NameWindow.geometry('350x150')
NameWindow.minsize(350, 150)
NameWindow.iconbitmap('./Images/uottawa_ver_black.ico')
NameWindow.resizable(False, False)

firstNamelbl = Label(NameWindow, text="First Name: ", font=(20))
firstNamelbl.grid(column=0, row=0)

firstName = Entry(NameWindow, width=20, font=(20))
firstName.grid(column=1, row=0)


lastNamelbl = Label(NameWindow, text="Last Name: ", font=(20))
lastNamelbl.grid(column=0, row=1, pady=10)

lastName = Entry(NameWindow,width=20, font=(20))
lastName.grid(column=1, row=1, pady=10)

btn = Button(NameWindow, text="Begin Testing", command=CreateSelectVideoWindow, font=(25))
btn.grid(column=0, row=2, columnspan=2, pady=10)

#-----------------------------------------


#Select Video Trailer Window ----------------------------
#This window allows the user to select which Movie Trailer they would like to watch

SelectVideoWindow.title("Trailer Viewer Program")
SelectVideoWindow.geometry('350x300')
SelectVideoWindow.minsize(350, 300)
SelectVideoWindow.iconbitmap('./Images/uottawa_ver_black.ico')

firstNamelbl = Label(SelectVideoWindow, text="Select a movie trailer to watch", font=(20))
firstNamelbl.config(anchor=CENTER)
firstNamelbl.pack(padx=0, pady=10)

listbox = Listbox(SelectVideoWindow, width=40)
listbox.yview()
listbox.xview()

listbox.pack(padx=0, pady=0)

btn3 = Button(SelectVideoWindow, text="Start Trailer", command=CreateVideoWindow, font=(25))
btn3.pack(padx=0, pady=10)

#-----------------------------------------


#Video Player Window ----------------------------
#This window allows the user to press continue once the movie trailer is finished

VideoWindow.title("Trailer Viewer Program")
VideoWindow.geometry('450x100')
VideoWindow.minsize(450, 100)
VideoWindow.iconbitmap('./Images/uottawa_ver_black.ico')
VideoWindow.resizable(False, False)

lbl4 = Label(VideoWindow, text="When trailer is finished, please press continue", font=(25))
lbl4.config(anchor=CENTER)
lbl4.pack(padx=0, pady=10)

btn4 = Button(VideoWindow, text="Continue", command=CreateRatingsWindow, font=(25))
btn4.config(anchor=CENTER)
btn4.pack(padx=0, pady=15)


#-----------------------------------------

#Trailer Rating Window ----------------------------
#This window allows the user to select if the trailer contained any funny, scary or sexy content

RatingsWindow.title("Trailer Viewer Program")
RatingsWindow.geometry('300x275')
RatingsWindow.minsize(300, 275)
RatingsWindow.iconbitmap('./Images/uottawa_ver_black.ico')
#RatingsWindow.resizable(False, False)

lbl5 = Label(RatingsWindow, text="Did the video content contain any\n of the following?", font=(25))
lbl5.grid(column=0, row=0, pady=10)

c1 = Checkbutton(RatingsWindow, text='Funny Content', variable=isFunny, font=(25))
c1.grid(sticky="W", column=0, row=1)

c2 = Checkbutton(RatingsWindow, text='Scary Content', variable=isScary, font=(25))
c2.grid(sticky="W", column=0, row=2)

c3 = Checkbutton(RatingsWindow, text='Sexy Content', variable=isSexy, font=(25))
c3.grid(sticky="W", column=0, row=3)

btn5 = Button(RatingsWindow, text="Next", command=CreateSpecificRatingsWindow, font=(25))
btn5.grid(column=0, row=4, pady=10)

#-----------------------------------------

#Specific Ratings Window ----------------------------
#This window will allow for the user to rate (on a scale of 1-10), how much of each selected content there was in the Movie Trailer

SpecificRatingsWindow.title("Trailer Viewer Program")
SpecificRatingsWindow.geometry('300x275')
SpecificRatingsWindow.minsize(300, 275)
SpecificRatingsWindow.iconbitmap('./Images/uottawa_ver_black.ico')
#SpecificRatingsWindow.resizable(False, False)

lbl6 = Label(SpecificRatingsWindow, text="Please rate the content presence\n on a scale of 1-10?", font=(25))
lbl6.grid(column=0, row=0, columnspan=2, pady=10)

#-----------------------------------------


btn2 = Button(mainWindow, text="Start", command=CreateNameWindow, font=(25))
btn2.config(anchor=CENTER)
btn2.pack(padx=0, pady=15)

def getTrailers():
    tempList = glob.glob("./Movie-Trailers/*.mp4")

    for x in tempList:
        x = x.replace("./Movie-Trailers\\","") 
        x = x.replace(".mp4", "")
        MovieTrailerList.append(x)

    counter = 1
    for x in MovieTrailerList:
        listbox.insert(counter, x)
        counter += 1

getTrailers()
mainWindow.mainloop()