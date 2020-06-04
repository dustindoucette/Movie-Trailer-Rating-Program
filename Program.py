#This is a Python program that allows users to view movie trailers and answer questions about them, then outputs the data to a csv file for analysis
#Author: Dustin Doucette (dustin.doucette@carleton.ca)

#**NOTE** This program must reside in a directory with no spaces in any names
#**NOTE** The Movie Trailer names must not contain any special characters (it also cannot have spaces)
#C:\User\ddouce\Program\Files           GOOD
#C:\User\Tim Johns\Progam\Files         BAD **

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from ctypes import *
from tkinter import messagebox
from os import startfile
from functools import partial
import os
import cv2
import sys
import csv
import glob

import pyglet

#Create all of the GUI's, so that they are ready for the user to use

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

#Global variables 
funnyRating = 0
currentFunny = 1
funnySections = []

allFunnyButtons = []
selectedFunnyButtons = []


scaryRating = 0
currentScary = 1
scarySections = []

allScaryButtons = []
selectedScaryButtons = []


sexyRating = 0
currentSexy = 1
sexySections = []

allSexyButtons = []
selectedSexyButtons = []


currentImportant = 1
importantSections = []

allImportantButtons = []
selectedImportantButtons = []


startFrame = 1
endFrame = 1

#When the user presses the "X" on a GUI window, make sure they did not click it accidentally
def on_closing():
    if messagebox.askokcancel("Exiting Program", "Are you sure you want to quit?"):
        RatingsWindow.destroy()
        mainWindow.destroy()

#When this function is called, terminate the entire program
def endProgram():
    mainWindow.destroy()

RatingsWindow.protocol("WM_DELETE_WINDOW", on_closing)
SpecificRatingsWindow.protocol("WM_DELETE_WINDOW", on_closing)
VideoWindow.protocol("WM_DELETE_WINDOW", on_closing)
SelectVideoWindow.protocol("WM_DELETE_WINDOW", on_closing)    
userIDWindow.protocol("WM_DELETE_WINDOW", on_closing) 
ThankYouWindow.protocol("WM_DELETE_WINDOW", endProgram) 

#Get all  of the names of the trailers in the movie trailer folder
def getTrailers():
    tempList = glob.glob("./Movie-Trailers/*.avi")

    for x in tempList:
        x = x.replace("./Movie-Trailers\\","") 
        x = x.replace(".avi", "")
        MovieTrailerList.append(x)

getTrailers()

#Generate frames for each section for each trailer (by calling another Python script)
def generateFrames():
    print()
    tempList = glob.glob("./Movie-Trailers/*")
    movies = []

    for x in tempList:
        x = x.replace("./Movie-Trailers\\","") 
        x = x.replace(".avi","") 
        movies.append(x)

    my_dict = {i:movies.count(i) for i in movies}

    movieList = []

    for name, number in my_dict.items():
        if number == 1:
            movieList.append(name)

    for x in movieList:
        os.mkdir("./Movie-Trailers/"+x)

    for x in movieList:
        os.system('python GenerateFrames.py ' + x)

generateFrames()

#Take the array, sort it, and find numbers which are right beside each other (put them into a tuple), and single out all of the numbers on their own 
def getGoodData(tempInput1 = []):
    #print("In: " + str(tempInput1))
    tempInput = sorted(tempInput1)
    #print("Sorted: " + str(tempInput))
    newArray = []
    tempNewArray = []
    lastOne = -1

    for x in tempInput:
        if(lastOne == -1):
            lastOne = x
            tempNewArray.append(x)
            if(x == tempInput[len(tempInput) - 1]):
                newArray.append(tempNewArray)
        else:
            if(lastOne == x - 1):
                tempNewArray.append(x)
                lastOne = x
                if(x == tempInput[len(tempInput) - 1]):
                    newArray.append(tempNewArray)
            else:
                newArray.append(tempNewArray)
                tempNewArray = [x]
                lastOne = x
                if(x == tempInput[len(tempInput) - 1]):
                    newArray.append(tempNewArray)

    finalArray = []

    for x in newArray:
        if(len(x) == 1):
            finalArray.append(x[0])
        else:
            finalArray.append([x[0], x[len(x)-1]])

    return(finalArray)

#Open the results csv file and enter all of the data generated from the program
def SaveData():
    allRows = []
    

    #print("User: " + userID)
    #print("Movie Trailer: " + MovieTrailerList[currentMovieNumber])

    funnyString = ""
    funny2 = ""
    funny3 = ""

    scaryString = ""
    scary2 = ""
    scary3 = ""

    sexyString = ""
    sexy2 = ""
    sexy3 = ""

    if(isFunny.get() == 1):
        funnySections = getGoodData(selectedFunnyButtons)
        #print("Funny: YES, " + " " + str(funnyRating) + " out of 10")
        #print("Funny Sections: " + str(funnySections))
        funnyString = "YES"
        funny2 = str(funnyRating)
        funny3 = str(funnySections)
    else:
        #print("Funny: NO")
        funnyString = "NO"
        funny2 = "N/A"
        funny3 = "N/A"

    if(isScary.get() == 1):
        scarySections = getGoodData(selectedScaryButtons)
        #print("Scary: YES, " + str(scaryRating) + " out of 10")
        #print("Scary Sections: " + str(scarySections))
        scaryString = "YES"
        scary2 = str(scaryRating)
        scary3 = str(scarySections)
    else:
        #print("Scary: NO")
        scaryString = "NO"
        scary2 = "N/A"
        scary3 = "N/A"

    if(isSexy.get() == 1):
        sexySections = getGoodData(selectedSexyButtons)
        #print("Sexy: YES, " + str(sexyRating) + " out of 10")
        #print("Sexy Sections: " + str(sexySections))
        sexyString = "YES"
        sexy2 = str(sexyRating)
        sexy3 = str(sexySections)
    else:
        #print("Sexy: NO")
        sexyString = "NO"
        sexy2 = "N/A"
        sexy3 = "N/A"

    importantSections = getGoodData(selectedImportantButtons)
    #print("Important Sections: " + str(importantSections))
    #print("")

    allRows.append([userID, MovieTrailerList[currentMovieNumber], funnyString, funny2, funny3, scaryString, scary2, scary3, sexyString, sexy2, sexy3, str(importantSections)])

    with open('.\Output-Logs\Results.csv','a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(allRows)
    

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

#Get all of the GUI's ready for the next trailer (i.e. change the images/frames), and reset all of the variables so old data is not passed forward unintentionally 
def GetNextTrailer():
    global currentMovieNumber
    global hasBeenToFunny
    global hasBeenToScary
    global hasBeenToSexy

    global funnyRating
    global currentFunny
    global funnySections
    global funnyListBoxCount

    global scaryRating
    global currentScary
    global scarySections
    global scaryListBoxCount

    global sexyRating
    global currentSexy
    global sexySections
    global sexyListBoxCount

    global currentImportant
    global importantSections
    global importantListBoxCount

    global allFunnyButtons
    global selectedFunnyButtons
    global FrameSelectionWindowFunny

    global allScaryButtons
    global selectedScaryButtons
    global FrameSelectionWindowScary

    global allSexyButtons
    global selectedSexyButtons
    global FrameSelectionWindowSexy

    global allImportantButtons
    global selectedImportantButtons
    global FrameSelectionWindowImportant

    FrameSelectionWindowImportant.withdraw()

    global startFrame
    global endFrame

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
        currentFunny = 0
        funnySections = []
        funnyListBoxCount = 1

        scaryRating = 0
        currentScary = 0
        scarySections = []
        scaryListBoxCount = 1

        sexyRating = 0
        currentSexy = 0
        sexySections = []
        sexyListBoxCount = 1

        currentImportant = 0
        importantSections = []
        importantListBoxCount = 1

        isFunny.set(0) 
        isScary.set(0) 
        isSexy.set(0)  

        s1.set(1)
        s2.set(1)
        s3.set(1)

        startFrame = 1
        endFrame = 1
        
        lbl7.config(state=NORMAL)
        s1.config(state=NORMAL)

        lbl8.config(state=NORMAL)
        s2.config(state=NORMAL)
        
        lbl9.config(state=NORMAL)
        s3.config(state=NORMAL)

        allFunnyButtons = []
        selectedFunnyButtons = []

        FrameSelectionWindowFunny.destroy()
        FrameSelectionWindowFunny = Toplevel(mainWindow)
        FrameSelectionWindowFunny.withdraw()
        createFunnyWindow()

        allScaryButtons = []
        selectedScaryButtons = []

        FrameSelectionWindowScary.destroy()
        FrameSelectionWindowScary = Toplevel(mainWindow)
        FrameSelectionWindowScary.withdraw()
        createScaryWindow()

        allSexyButtons = []
        selectedSexyButtons = []

        FrameSelectionWindowSexy.destroy()
        FrameSelectionWindowSexy = Toplevel(mainWindow)
        FrameSelectionWindowSexy.withdraw()
        createSexyWindow()

        allImportantButtons = []
        selectedImportantButtons = []

        FrameSelectionWindowImportant.destroy()
        FrameSelectionWindowImportant = Toplevel(mainWindow)
        FrameSelectionWindowImportant.withdraw()
        createImportantWindow()

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

#Show each of the windows based on prior user input
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
    movieLocation = os.getcwd() + "\\Movie-Trailers\\" + MovieTrailerList[currentMovieNumber] + ".avi"

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
userIDWindow.geometry('275x100')
userIDWindow.minsize(275, 100)
userIDWindow.iconbitmap('./Images/uottawa_ver_black.ico')
userIDWindow.resizable(False, False)

userIDlbl = Label(userIDWindow, text="User ID: ", font=(20))
userIDlbl.grid(column=0, row=0)

userIDInput = Entry(userIDWindow, width=20, font=(20))
userIDInput.grid(column=1, row=0)

btn = Button(userIDWindow, text="Begin Testing", command=CreateSelectVideoWindow, font=(25))
btn.grid(column=0, row=2, columnspan=2, pady=10)

userIDWindow.grid_rowconfigure(0, weight=1)
userIDWindow.grid_rowconfigure(1, weight=1)
userIDWindow.grid_rowconfigure(2, weight=1)
userIDWindow.grid_columnconfigure(0, weight=1)
userIDWindow.grid_columnconfigure(1, weight=1)

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
c1.grid(column=0, row=1)

c2 = Checkbutton(RatingsWindow, text='Scary Content', variable=isScary, font=(25))
c2.grid(column=0, row=2)

c3 = Checkbutton(RatingsWindow, text='Sexy Content', variable=isSexy, font=(25))
c3.grid(column=0, row=3)

btn5 = Button(RatingsWindow, text="Next", command=CreateSpecificRatingsWindow, font=(25))
btn5.grid(column=0, row=4, pady=10)

RatingsWindow.grid_rowconfigure(0, weight=1)
RatingsWindow.grid_rowconfigure(1, weight=1)
RatingsWindow.grid_rowconfigure(2, weight=1)
RatingsWindow.grid_rowconfigure(3, weight=1)
RatingsWindow.grid_rowconfigure(4, weight=1)
RatingsWindow.grid_columnconfigure(0, weight=1)

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
lbl7.grid(column=0, row=1)

s1 = Scale(SpecificRatingsWindow, from_=1, to=10, orient=HORIZONTAL, command=setFunnyRating)
s1.grid(column=1, row=1)

seperator10 = ttk.Separator(SpecificRatingsWindow, orient=HORIZONTAL).grid(row=2, columnspan=2, sticky="ew")

lbl8 = Label(SpecificRatingsWindow, text="Scary", font=(25))
lbl8.grid(column=0, row=3)

s2 = Scale(SpecificRatingsWindow, from_=1, to=10, orient=HORIZONTAL, command=setScaryRating)
s2.grid(column=1, row=3)

seperator11 = ttk.Separator(SpecificRatingsWindow, orient=HORIZONTAL).grid(row=4, columnspan=2, sticky="ew")

lbl9 = Label(SpecificRatingsWindow, text="Sexy", font=(25))
lbl9.grid(column=0, row=5)

s3 = Scale(SpecificRatingsWindow, from_=1, to=10, orient=HORIZONTAL, command=setSexyRating)
s3.grid(column=1, row=5)

btn5 = Button(SpecificRatingsWindow, text="Next", command=GetIndividualFrames, font=(25))
btn5.grid(column=0, row=6, columnspan=2, pady=10)

SpecificRatingsWindow.grid_rowconfigure(0, weight=1)
SpecificRatingsWindow.grid_rowconfigure(1, weight=1)
SpecificRatingsWindow.grid_rowconfigure(2, weight=1)
SpecificRatingsWindow.grid_rowconfigure(3, weight=1)
SpecificRatingsWindow.grid_rowconfigure(4, weight=1)
SpecificRatingsWindow.grid_rowconfigure(5, weight=1)
SpecificRatingsWindow.grid_rowconfigure(6, weight=1)
SpecificRatingsWindow.grid_columnconfigure(0, weight=1)
SpecificRatingsWindow.grid_columnconfigure(1, weight=1)

#-----------------------------------------

def printFunnyNumber(inputFromUser):
    global allFunnyButtons
    global selectedFunnyButtons
    #print(inputFromUser)

    if inputFromUser not in selectedFunnyButtons:
        selectedFunnyButtons.append(inputFromUser)
        allFunnyButtons[int(inputFromUser)-1].config(bg = "red")
    else:
        selectedFunnyButtons.remove(inputFromUser)
        allFunnyButtons[int(inputFromUser)-1].config(bg = "white")
    
    #print("Currently selected Funny Buttons: " + str(selectedFunnyButtons))

#Frame Selection Window Funny ----------------------------
#This window will allow for the user to select which frame(s) contain the specified content 
def createFunnyWindow():
    FrameSelectionWindowFunny.title("Trailer Viewer Program")
    FrameSelectionWindowFunny.geometry('500x775')
    FrameSelectionWindowFunny.minsize(500, 775)
    FrameSelectionWindowFunny.iconbitmap('./Images/uottawa_ver_black.ico')
    #FrameSelectionWindowFunny.resizable(False, False)
    FrameSelectionWindowFunny.protocol("WM_DELETE_WINDOW", on_closing) 

    FrameSelectionWindowTitleFunnylbl = Label(FrameSelectionWindowFunny, text="Please select the frames that contain funny content", font=(25))
    FrameSelectionWindowTitleFunnylbl.grid(column=0, row=0, columnspan=2, pady=10)

    photoFrameFunny = Frame(FrameSelectionWindowFunny)
    photoFrameFunny.grid(column=0, row=1, columnspan=2, pady=10)

    photoFrameFunny.grid_rowconfigure(0, weight=1)
    photoFrameFunny.grid_columnconfigure(0, weight=1)

    rowCount = 0
    columnCount = 0

    tempNumber = glob.glob("./Movie-Trailers/"+ MovieTrailerList[currentMovieNumber] + "/image*")

    for x in range(1, len(tempNumber) + 1):
        if(columnCount == 10):
            columnCount = 0
            rowCount = rowCount + 1

        im = Image.open("./Movie-Trailers/"+ MovieTrailerList[currentMovieNumber] + "/image" + str(x) + ".jpg")
        resized = im.resize((160, 90), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)

        action_with_arg = partial(printFunnyNumber, x)
        myvar = Button(photoFrameFunny, bd=2, bg = "white", image=tkimage, command=action_with_arg)

        myvar.image = tkimage
        myvar.grid(row=rowCount, column=columnCount)

        allFunnyButtons.append(myvar)

        columnCount = columnCount + 1

    FrameSelectionWindowFunnybutton = Button(FrameSelectionWindowFunny, text="Finished", command=funnyClick, font=(25))
    FrameSelectionWindowFunnybutton.grid(column=0, row=2, pady=10)

    FrameSelectionWindowFunny.grid_rowconfigure(0, weight=1)
    FrameSelectionWindowFunny.grid_rowconfigure(1, weight=1)
    FrameSelectionWindowFunny.grid_rowconfigure(2, weight=1)
    FrameSelectionWindowFunny.grid_columnconfigure(0, weight=1)

#-----------------------------------------

#-----------------------------------------

def printScaryNumber(inputFromUser):
    global allScaryButtons
    global selectedScaryButtons
    #print(inputFromUser)

    if inputFromUser not in selectedScaryButtons:
        selectedScaryButtons.append(inputFromUser)
        allScaryButtons[int(inputFromUser)-1].config(bg = "red")
    else:
        selectedScaryButtons.remove(inputFromUser)
        allScaryButtons[int(inputFromUser)-1].config(bg = "white")
    
    #print("Currently selected Scary Buttons: " + str(selectedScaryButtons))

#Frame Selection Window Scary ----------------------------
#This window will allow for the user to select which frame(s) contain the specified content 
def createScaryWindow():
    FrameSelectionWindowScary.title("Trailer Viewer Program")
    FrameSelectionWindowScary.geometry('500x775')
    FrameSelectionWindowScary.minsize(500, 775)
    FrameSelectionWindowScary.iconbitmap('./Images/uottawa_ver_black.ico')
    #FrameSelectionWindowScary.resizable(False, False)
    FrameSelectionWindowScary.protocol("WM_DELETE_WINDOW", on_closing) 

    FrameSelectionWindowTitleScarylbl = Label(FrameSelectionWindowScary, text="Please select the frames that contain scary content", font=(25))
    FrameSelectionWindowTitleScarylbl.grid(column=0, row=0, columnspan=2, pady=10)

    photoFrameScary = Frame(FrameSelectionWindowScary)
    photoFrameScary.grid(column=0, row=1, columnspan=2, pady=10)

    photoFrameScary.grid_rowconfigure(0, weight=1)
    photoFrameScary.grid_columnconfigure(0, weight=1)

    rowCount = 0
    columnCount = 0

    tempNumber = glob.glob("./Movie-Trailers/"+ MovieTrailerList[currentMovieNumber] + "/image*")

    for x in range(1, len(tempNumber) + 1):
        if(columnCount == 10):
            columnCount = 0
            rowCount = rowCount + 1

        im = Image.open("./Movie-Trailers/"+ MovieTrailerList[currentMovieNumber] + "/image" + str(x) + ".jpg")
        resized = im.resize((160, 90), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)

        action_with_arg = partial(printScaryNumber, x)
        myvar = Button(photoFrameScary, bd=2, bg = "white", image=tkimage, command=action_with_arg)

        myvar.image = tkimage
        myvar.grid(row=rowCount, column=columnCount)

        allScaryButtons.append(myvar)

        columnCount = columnCount + 1

    FrameSelectionWindowScarybutton = Button(FrameSelectionWindowScary, text="Finished", command=scaryClick, font=(25))
    FrameSelectionWindowScarybutton.grid(column=0, row=2, pady=10)

    FrameSelectionWindowScary.grid_rowconfigure(0, weight=1)
    FrameSelectionWindowScary.grid_rowconfigure(1, weight=1)
    FrameSelectionWindowScary.grid_rowconfigure(2, weight=1)
    FrameSelectionWindowScary.grid_columnconfigure(0, weight=1)

#-----------------------------------------

#-----------------------------------------

def printSexyNumber(inputFromUser):
    global allSexyButtons
    global selectedSexyButtons
    #print(inputFromUser)

    if inputFromUser not in selectedSexyButtons:
        selectedSexyButtons.append(inputFromUser)
        allSexyButtons[int(inputFromUser)-1].config(bg = "red")
    else:
        selectedSexyButtons.remove(inputFromUser)
        allSexyButtons[int(inputFromUser)-1].config(bg = "white")
    
    #print("Currently selected Sexy Buttons: " + str(selectedSexyButtons))

#Frame Selection Window Sexy ----------------------------
#This window will allow for the user to select which frame(s) contain the specified content 
def createSexyWindow():
    FrameSelectionWindowSexy.title("Trailer Viewer Program")
    FrameSelectionWindowSexy.geometry('500x775')
    FrameSelectionWindowSexy.minsize(500, 775)
    FrameSelectionWindowSexy.iconbitmap('./Images/uottawa_ver_black.ico')
    #FrameSelectionWindowSexy.resizable(False, False)
    FrameSelectionWindowSexy.protocol("WM_DELETE_WINDOW", on_closing) 

    FrameSelectionWindowTitleSexylbl = Label(FrameSelectionWindowSexy, text="Please select the frames that contain sexy content", font=(25))
    FrameSelectionWindowTitleSexylbl.grid(column=0, row=0, columnspan=2, pady=10)

    photoFrameSexy = Frame(FrameSelectionWindowSexy)
    photoFrameSexy.grid(column=0, row=1, columnspan=2, pady=10)

    photoFrameSexy.grid_rowconfigure(0, weight=1)
    photoFrameSexy.grid_columnconfigure(0, weight=1)

    rowCount = 0
    columnCount = 0

    tempNumber = glob.glob("./Movie-Trailers/"+ MovieTrailerList[currentMovieNumber] + "/image*")

    for x in range(1, len(tempNumber) + 1):
        if(columnCount == 10):
            columnCount = 0
            rowCount = rowCount + 1

        im = Image.open("./Movie-Trailers/"+ MovieTrailerList[currentMovieNumber] + "/image" + str(x) + ".jpg")
        resized = im.resize((160, 90), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)

        action_with_arg = partial(printSexyNumber, x)
        myvar = Button(photoFrameSexy, bd=2, bg = "white", image=tkimage, command=action_with_arg)

        myvar.image = tkimage
        myvar.grid(row=rowCount, column=columnCount)

        allSexyButtons.append(myvar)

        columnCount = columnCount + 1

    FrameSelectionWindowSexybutton = Button(FrameSelectionWindowSexy, text="Finished", command=sexyClick, font=(25))
    FrameSelectionWindowSexybutton.grid(column=0, row=2, pady=10)

    FrameSelectionWindowSexy.grid_rowconfigure(0, weight=1)
    FrameSelectionWindowSexy.grid_rowconfigure(1, weight=1)
    FrameSelectionWindowSexy.grid_rowconfigure(2, weight=1)
    FrameSelectionWindowSexy.grid_columnconfigure(0, weight=1)

#-----------------------------------------

#-----------------------------------------

def printImportantNumber(inputFromUser):
    global allImportantButtons
    global selectedImportantButtons
    #print(inputFromUser)

    if inputFromUser not in selectedImportantButtons:
        selectedImportantButtons.append(inputFromUser)
        allImportantButtons[int(inputFromUser)-1].config(bg = "red")
    else:
        selectedImportantButtons.remove(inputFromUser)
        allImportantButtons[int(inputFromUser)-1].config(bg = "white")
    
    #print("Currently selected Important Buttons: " + str(selectedImportantButtons))

#Frame Selection Window Important ----------------------------
#This window will allow for the user to select which frame(s) contain the specified content 
def createImportantWindow():
    FrameSelectionWindowImportant.title("Trailer Viewer Program")
    FrameSelectionWindowImportant.geometry('500x775')
    FrameSelectionWindowImportant.minsize(500, 775)
    FrameSelectionWindowImportant.iconbitmap('./Images/uottawa_ver_black.ico')
    #FrameSelectionWindowImportant.resizable(False, False)
    FrameSelectionWindowImportant.protocol("WM_DELETE_WINDOW", on_closing) 

    FrameSelectionWindowTitleImportantlbl = Label(FrameSelectionWindowImportant, text="Please select the frames that contain important content", font=(25))
    FrameSelectionWindowTitleImportantlbl.grid(column=0, row=0, columnspan=2, pady=10)

    photoFrameImportant = Frame(FrameSelectionWindowImportant)
    photoFrameImportant.grid(column=0, row=1, columnspan=2, pady=10)

    photoFrameImportant.grid_rowconfigure(0, weight=1)
    photoFrameImportant.grid_columnconfigure(0, weight=1)

    rowCount = 0
    columnCount = 0

    tempNumber = glob.glob("./Movie-Trailers/"+ MovieTrailerList[currentMovieNumber] + "/image*")

    for x in range(1, len(tempNumber) + 1):
        if(columnCount == 10):
            columnCount = 0
            rowCount = rowCount + 1

        im = Image.open("./Movie-Trailers/"+ MovieTrailerList[currentMovieNumber] + "/image" + str(x) + ".jpg")
        resized = im.resize((160, 90), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)

        action_with_arg = partial(printImportantNumber, x)
        myvar = Button(photoFrameImportant, bd=2, bg = "white", image=tkimage, command=action_with_arg)

        myvar.image = tkimage
        myvar.grid(row=rowCount, column=columnCount)

        allImportantButtons.append(myvar)

        columnCount = columnCount + 1

    FrameSelectionWindowImportantbutton = Button(FrameSelectionWindowImportant, text="Finished", command=GetNextTrailer, font=(25))
    FrameSelectionWindowImportantbutton.grid(column=0, row=2, pady=10)

    FrameSelectionWindowImportant.grid_rowconfigure(0, weight=1)
    FrameSelectionWindowImportant.grid_rowconfigure(1, weight=1)
    FrameSelectionWindowImportant.grid_rowconfigure(2, weight=1)
    FrameSelectionWindowImportant.grid_columnconfigure(0, weight=1)

#-----------------------------------------

btn2 = Button(mainWindow, text="Start", command=CreateuserIDWindow, font=(25))
btn2.config(anchor=CENTER)
btn2.pack(padx=0, pady=15)

createFunnyWindow()
createScaryWindow()
createSexyWindow()
createImportantWindow()

#Start the program
mainWindow.mainloop()