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
userIDWindow = Toplevel(mainWindow)
userIDWindow.withdraw()
SelectVideoWindow = Toplevel(mainWindow)
SelectVideoWindow.withdraw()
RatingsWindow = Toplevel(mainWindow)
RatingsWindow.withdraw()
SpecificRatingsWindow = Toplevel(mainWindow)
SpecificRatingsWindow.withdraw()
FrameSelectionWindowFunny = Toplevel(mainWindow)
FrameSelectionWindowFunny.withdraw()
FrameSelectionWindowScary = Toplevel(mainWindow)
FrameSelectionWindowScary.withdraw()
FrameSelectionWindowSexy = Toplevel(mainWindow)
FrameSelectionWindowSexy.withdraw()
FrameSelectionWindowImportant = Toplevel(mainWindow)
FrameSelectionWindowImportant.withdraw()
ThankYouWindow = Toplevel(mainWindow)
ThankYouWindow.withdraw()

#User Details
userID = ''

#A list containing all of the movie trailer names
MovieTrailerList = []
currentMovieNumber = 0

#use isFunny.get() to get if it is pressed or not (1 = it is selected, 0 = it is not selected)
isFunny = IntVar()
isScary = IntVar() 
isSexy = IntVar() 

hasBeenToFunny = False
hasBeenToScary = False
hasBeenToSexy = False

#Set 0 by default
funnyRating = 0
scaryRating = 0
sexyRating = 0

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
userIDWindow.protocol("WM_DELETE_WINDOW", on_closing) 
ThankYouWindow.protocol("WM_DELETE_WINDOW", endProgram) 
FrameSelectionWindowFunny.protocol("WM_DELETE_WINDOW", on_closing) 
FrameSelectionWindowScary.protocol("WM_DELETE_WINDOW", on_closing) 
FrameSelectionWindowSexy.protocol("WM_DELETE_WINDOW", on_closing) 
FrameSelectionWindowImportant.protocol("WM_DELETE_WINDOW", on_closing) 

def SaveData():
    print("User: " + userID)
    print("Movie Trailer: " + MovieTrailerList[currentMovieNumber])

    if(isFunny.get() == 1):
        print("Funny: YES, " + " " + str(funnyRating) + " out of 10")
    else:
        print("Funny: NO")

    if(isScary.get() == 1):
        print("Scary: YES, " + str(scaryRating) + " out of 10")
    else:
        print("Scary: NO")

    if(isSexy.get() == 1):
        print("Sexy: YES, " + str(sexyRating) + " out of 10")
    else:
        print("Sexy: NO")
    print("")
    

def SayThankYou():
    #Another window will popup at the end thanking the user for their participation
    #RatingsWindow.withdraw()
    ThankYouWindow.update()
    ThankYouWindow.deiconify()

    ThankYouWindow.title("Trailer Viewer Program")
    ThankYouWindow.geometry('500x100')
    ThankYouWindow.minsize(500, 100)
    location = os.getcwd() + "\\Images\\uottawa_ver_black.ico"
    ThankYouWindow.iconbitmap(location)

    lbl = Label(ThankYouWindow, text="Thank you for your participation in \nthe ... experiment, your results are greatly appreciated.\n You may now exit the program.", font=(25))
    lbl.config(anchor=CENTER)
    lbl.pack(padx=0, pady=0)

def GetNextTrailer():
    FrameSelectionWindowImportant.withdraw()
    global currentMovieNumber
    global hasBeenToFunny
    global hasBeenToScary
    global hasBeenToSexy
    global funnyRating
    global scaryRating
    global sexyRating

    #This is where the output data for the last trailer will be saved to the excel file ******
    SaveData()

    if (len(MovieTrailerList) == (currentMovieNumber + 1)):
        #print("No More Trailers")
        SayThankYou()
    else:
        #print("More Trailers")
        currentMovieNumber = currentMovieNumber + 1

        #Reset all of the variables and GUI's
        hasBeenToFunny = False
        hasBeenToScary = False
        hasBeenToSexy = False

        funnyRating = 0
        scaryRating = 0
        sexyRating = 0

        isFunny.set(0) 
        isScary.set(0) 
        isSexy.set(0)  

        s1.set(1)
        s2.set(1)
        s3.set(1)
        
        lbl7.config(state=NORMAL)
        s1.config(state=NORMAL)

        lbl8.config(state=NORMAL)
        s2.config(state=NORMAL)
        
        lbl9.config(state=NORMAL)
        s3.config(state=NORMAL)

        CreateSelectVideoWindow()


def GetImportantParts():
    #This is where another window will pop up, which will ask which part(s) of the movie trailer was the user's favourite
    FrameSelectionWindowImportant.update()
    FrameSelectionWindowImportant.deiconify()

def funnyClick():
    FrameSelectionWindowFunny.withdraw()
    ShowIndividualFrames()

def scaryClick():
    FrameSelectionWindowScary.withdraw()
    ShowIndividualFrames()

def sexyClick():
    FrameSelectionWindowSexy.withdraw()
    ShowIndividualFrames()

def ShowIndividualFrames():
    global hasBeenToFunny
    global hasBeenToScary
    global hasBeenToSexy

    if((isFunny.get() == 1) and (hasBeenToFunny == False)):
        FrameSelectionWindowFunny.update()
        FrameSelectionWindowFunny.deiconify()
        hasBeenToFunny = True
    elif((isScary.get() == 1) and (hasBeenToScary == False)):
        FrameSelectionWindowScary.update()
        FrameSelectionWindowScary.deiconify()
        hasBeenToScary = True
    elif((isSexy.get() == 1) and (hasBeenToSexy == False)):
        FrameSelectionWindowSexy.update()
        FrameSelectionWindowSexy.deiconify()
        hasBeenToSexy = True
    else:
        GetImportantParts()

def GetIndividualFrames():
    SpecificRatingsWindow.withdraw()
    
    ShowIndividualFrames()

def setFunnyRating(val):
    global funnyRating
    funnyRating = val

def setScaryRating(val):
    global scaryRating
    scaryRating = val

def setSexyRating(val):
    global sexyRating
    sexyRating = val

def CreateSpecificRatingsWindow():
    if((isFunny.get() == 0) and (isScary.get() == 0) and (isSexy.get() == 0)):
        #Skip to the window which will allow user to select the important parts of the movie trailer
        RatingsWindow.withdraw()
        GetImportantParts()
    else:
        RatingsWindow.withdraw()
        SpecificRatingsWindow.update()
        SpecificRatingsWindow.deiconify()

        if(isFunny.get() == 0):
            lbl7.config(state=DISABLED)
            s1.config(state=DISABLED)

        if(isScary.get() == 0):
            lbl8.config(state=DISABLED)
            s2.config(state=DISABLED)

        if(isSexy.get() == 0):
            lbl9.config(state=DISABLED)
            s3.config(state=DISABLED)

def CreateRatingsWindow():
    VideoWindow.withdraw()
    RatingsWindow.update()
    RatingsWindow.deiconify()

def CreateVideoWindow():
    SelectVideoWindow.withdraw()
    VideoWindow.update()
    VideoWindow.deiconify()

    #Movie titles cannot have any spaces and/or special characters
    movieLocation = os.getcwd() + "\\Movie-Trailers\\" + MovieTrailerList[currentMovieNumber] + ".mp4"

    os.system(movieLocation)

def CreateSelectVideoWindow():
    global userID
    userIDWindow.withdraw()
    SelectVideoWindow.update()
    SelectVideoWindow.deiconify()

    nextMovieTrailerlbl.config(text=MovieTrailerList[currentMovieNumber])

    userID = userIDInput.get()

def CreateuserIDWindow():
    mainWindow.withdraw()
    userIDWindow.update()
    userIDWindow.deiconify()


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


#UserID Entry Window -----------------------------
#This window allows the user to enter their user ID for statistical purposes

userIDWindow.title("Trailer Viewer Program")
userIDWindow.geometry('325x100')
userIDWindow.minsize(325, 100)
userIDWindow.iconbitmap('./Images/uottawa_ver_black.ico')
userIDWindow.resizable(False, False)

userIDlbl = Label(userIDWindow, text="User ID: ", font=(20))
userIDlbl.grid(column=0, row=0)

userIDInput = Entry(userIDWindow, width=20, font=(20))
userIDInput.grid(column=1, row=0)

btn = Button(userIDWindow, text="Begin Testing", command=CreateSelectVideoWindow, font=(25))
btn.grid(column=0, row=2, columnspan=2, pady=10)

#-----------------------------------------


#Preview Name of Video Trailer Window ----------------------------
#This window allows the user to view what the title of the next movie trailer is, and allows them to take a break before playing the next trailer

SelectVideoWindow.title("Trailer Viewer Program")
SelectVideoWindow.geometry('350x175')
SelectVideoWindow.minsize(350, 175)
SelectVideoWindow.iconbitmap('./Images/uottawa_ver_black.ico')

firstNamelbl = Label(SelectVideoWindow, text="Next Movie Trailer:", font=(20))
firstNamelbl.config(anchor=CENTER)
firstNamelbl.pack(padx=0, pady=10)

nextMovieTrailerlbl = Label(SelectVideoWindow, text="...", font=(20))
nextMovieTrailerlbl.config(anchor=CENTER)
nextMovieTrailerlbl.pack(padx=0, pady=10)

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

lbl7 = Label(SpecificRatingsWindow, text="Funny", font=(25))
lbl7.grid(sticky="W", column=0, row=1)

s1 = Scale(SpecificRatingsWindow, from_=1, to=10, orient=HORIZONTAL, command=setFunnyRating)
s1.grid(sticky="W", column=1, row=1)

lbl8 = Label(SpecificRatingsWindow, text="Scary", font=(25))
lbl8.grid(sticky="W", column=0, row=2)

s2 = Scale(SpecificRatingsWindow, from_=1, to=10, orient=HORIZONTAL, command=setScaryRating)
s2.grid(sticky="W", column=1, row=2)

lbl9 = Label(SpecificRatingsWindow, text="Sexy", font=(25))
lbl9.grid(sticky="W", column=0, row=3)

s3 = Scale(SpecificRatingsWindow, from_=1, to=10, orient=HORIZONTAL, command=setSexyRating)
s3.grid(sticky="W", column=1, row=3)

btn5 = Button(SpecificRatingsWindow, text="Next", command=GetIndividualFrames, font=(25))
btn5.grid(column=0, row=4, columnspan=2, pady=10)

#-----------------------------------------


#-----------------------------------------

#Frame Selection Window Funny ----------------------------
#This window will allow for the user to select which frame(s) contain the specified content 

FrameSelectionWindowFunny.title("Trailer Viewer Program")
FrameSelectionWindowFunny.geometry('1000x1000')
FrameSelectionWindowFunny.minsize(1000, 1000)
FrameSelectionWindowFunny.iconbitmap('./Images/uottawa_ver_black.ico')
#FrameSelectionWindow.resizable(False, False)

FrameSelectionWindowTitleFunnylbl = Label(FrameSelectionWindowFunny, text="Please select the frames that contain funny content", font=(25))
FrameSelectionWindowTitleFunnylbl.grid(column=0, row=0, columnspan=2, pady=10)

FrameSelectionWindowFunnybutton = Button(FrameSelectionWindowFunny, text="Next", command=funnyClick, font=(25))
FrameSelectionWindowFunnybutton.grid(column=0, row=1, pady=10)

#-----------------------------------------


#Frame Selection Window Scary ----------------------------
#This window will allow for the user to select which frame(s) contain the specified content 

FrameSelectionWindowScary.title("Trailer Viewer Program")
FrameSelectionWindowScary.geometry('1000x1000')
FrameSelectionWindowScary.minsize(1000, 1000)
FrameSelectionWindowScary.iconbitmap('./Images/uottawa_ver_black.ico')
#FrameSelectionWindow.resizable(False, False)

FrameSelectionWindowTitleScarylbl = Label(FrameSelectionWindowScary, text="Please select the frames that contain scary content", font=(25))
FrameSelectionWindowTitleScarylbl.grid(column=0, row=0, columnspan=2, pady=10)

FrameSelectionWindowScarybutton = Button(FrameSelectionWindowScary, text="Next", command=scaryClick, font=(25))
FrameSelectionWindowScarybutton.grid(column=0, row=1, pady=10)

#-----------------------------------------


#Frame Selection Window Sexy ----------------------------
#This window will allow for the user to select which frame(s) contain the specified content 

FrameSelectionWindowSexy.title("Trailer Viewer Program")
FrameSelectionWindowSexy.geometry('1000x1000')
FrameSelectionWindowSexy.minsize(1000, 1000)
FrameSelectionWindowSexy.iconbitmap('./Images/uottawa_ver_black.ico')
#FrameSelectionWindow.resizable(False, False)

FrameSelectionWindowTitleSexylbl = Label(FrameSelectionWindowSexy, text="Please select the frames that contain sexy content", font=(25))
FrameSelectionWindowTitleSexylbl.grid(column=0, row=0, columnspan=2, pady=10)

FrameSelectionWindowSexybutton = Button(FrameSelectionWindowSexy, text="Next", command=sexyClick, font=(25))
FrameSelectionWindowSexybutton.grid(column=0, row=1, pady=10)

#-----------------------------------------


#Frame Selection Window Important ----------------------------
#This window will allow for the user to select which frame(s) contain the specified content 

FrameSelectionWindowImportant.title("Trailer Viewer Program")
FrameSelectionWindowImportant.geometry('1000x1000')
FrameSelectionWindowImportant.minsize(1000, 1000)
FrameSelectionWindowImportant.iconbitmap('./Images/uottawa_ver_black.ico')
#FrameSelectionWindow.resizable(False, False)

FrameSelectionWindowTitleImportantlbl = Label(FrameSelectionWindowImportant, text="Please select the frames that contain important content", font=(25))
FrameSelectionWindowTitleImportantlbl.grid(column=0, row=0, columnspan=2, pady=10)

FrameSelectionWindowImportantbutton = Button(FrameSelectionWindowImportant, text="Next", command=GetNextTrailer, font=(25))
FrameSelectionWindowImportantbutton.grid(column=0, row=1, pady=10)

#-----------------------------------------


btn2 = Button(mainWindow, text="Start", command=CreateuserIDWindow, font=(25))
btn2.config(anchor=CENTER)
btn2.pack(padx=0, pady=15)

def getTrailers():
    tempList = glob.glob("./Movie-Trailers/*.mp4")

    for x in tempList:
        x = x.replace("./Movie-Trailers\\","") 
        x = x.replace(".mp4", "")
        MovieTrailerList.append(x)

getTrailers()
mainWindow.mainloop()