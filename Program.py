# This is a Python program that allows users to view movie trailers and answer questions about them, then outputs the data to a csv file for analysis
# Author: Dustin Doucette (dustin.doucette@carleton.ca)

# **NOTE** This program must reside in a directory with no spaces in any names
# **NOTE** The Movie Trailer names must not contain any special characters (it also cannot have spaces)

# C:/User/Frank/Program/Files           GOOD
# C:/User/Tim Johns/Progam/Files         BAD **

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from ctypes import *
from tkinter import messagebox

import os
import cv2
import sys
import csv
import glob
import u3
import time

import pyglet

# Centers a tkinter window
def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = win.winfo_screenwidth() // 2 - width // 2
    y = win.winfo_screenheight() // 2 - height // 2

    win.geometry("{}x{}+{}+{}".format(width, height, x, y))
    win.deiconify()


# Create all of the GUI's, so that they are ready for the user to use
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

trailerBlockWindow = Toplevel(mainWindow)
trailerBlockWindow.withdraw()

ThankYouWindow = Toplevel(mainWindow)
ThankYouWindow.withdraw()

# User Details
userID = ""

# Connection to BIOPAC
biopacConnectionPort = u3.U3()

# A list containing all of the movie trailer names
MovieTrailerList = [[], [], [], [], [], []]

currentMovieNumber = 0

# use isFunny.get() to get if it is pressed or not (1 = it is selected, 0 = it is not selected)
isFunny = IntVar()
isScary = IntVar()
isSexy = IntVar()

hasBeenToFunny = False
hasBeenToScary = False
hasBeenToSexy = False

# Global variables
trailerBlock = 1

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

startFrame = 0
endFrame = 0

# When the user presses the "X" on a GUI window, make sure they did not click it accidentally
def on_closing():
    if messagebox.askokcancel("Exiting Program", "Are you sure you want to quit?"):
        RatingsWindow.destroy()
        mainWindow.destroy()


# When this function is called, terminate the entire program
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
trailerBlockWindow.protocol("WM_DELETE_WINDOW", on_closing)

# Get all  of the names of the trailers in the movie trailer block folders
for blockNumber in range(1, 6):
    tempList = glob.glob("./Movie-Trailers/Block_" + str(blockNumber) + "/*.avi")

    for x in tempList:
        x = x.replace("./Movie-Trailers/Block_" + str(blockNumber) + "/", "")
        x = x.replace(".avi", "")
        MovieTrailerList[blockNumber].append(x)

MovieTrailerList[1].sort()
MovieTrailerList[2].sort()
MovieTrailerList[3].sort()
MovieTrailerList[4].sort()
MovieTrailerList[5].sort()

# Generate frames for each section of every trailer (by calling another Python script)
for blockNumber in range(1, 6):
    print(
        "Generating Frames for Block " + str(blockNumber) + " Trailers, Please Wait\n"
    )
    tempList = glob.glob("./Movie-Trailers/Block_" + str(blockNumber) + "/*")
    movies = []

    for x in tempList:
        x = x.replace("./Movie-Trailers/Block_" + str(blockNumber) + "/", "")
        x = x.replace(".avi", "")
        movies.append(x)

    my_dict = {i: movies.count(i) for i in movies}

    movieList = []

    for name, number in my_dict.items():
        if number == 1:
            movieList.append(name)

    for x in movieList:
        os.mkdir("./Movie-Trailers/Block_" + str(blockNumber) + "/" + x)

    for x in movieList:
        os.system("python3 GenerateFrames.py " + "Block_" + str(blockNumber) + "/" + x)

print("All Frames Generated, Program Starting\n\n")

# This function allows for an array of tuples to be passed in, and for all of the values to be modified by a certain amount
# If there are 2 frames per second, divide frame by 2 to get the time that the selected frame is at
def getFrameTimes(inputArray):
    newArray = []
    for x in inputArray:
        tempFirst = (x[0]) / 2
        tempSecond = (x[1]) / 2

        newArray.append([tempFirst, tempSecond])

    return newArray


# This function allows for an array of tuples to be passed in, and for all of the values to be modified by a certain amount
# Record the image that the user clicked on (both the start frame and the end frame)
def getImageNumbers(inputArray):
    newArray = []
    for x in inputArray:
        tempStartImage = "image" + str(x[0]) + ".jpg"
        tempEndImage = "image" + str(x[1]) + ".jpg"

        newArray.append([tempStartImage + " to " + tempEndImage])

    return newArray


# Open the results csv file and enter all of the data generated from the program
def SaveData():
    allRows = []
    print("User: " + userID)
    print("Movie Trailer: " + MovieTrailerList[trailerBlock][currentMovieNumber])

    funnyString = ""
    funny2 = ""
    funny3 = ""
    funny4 = ""

    scaryString = ""
    scary2 = ""
    scary3 = ""
    scary4 = ""

    sexyString = ""
    sexy2 = ""
    sexy3 = ""
    sexy4 = ""

    print("Trailer Block: " + str(trailerBlock))
    trailerBlockString = str(trailerBlock)

    if isFunny.get() == 1:
        print("Funny: YES, " + " " + str(funnyRating) + " out of 10")
        print("Funny Section(s): " + str(getFrameTimes(funnySections)))
        print("Funny Section(s): " + str(getImageNumbers(funnySections)))
        funnyString = "YES"
        funny2 = str(funnyRating)
        funny3 = str(getFrameTimes(funnySections))
        funny4 = str(getImageNumbers(funnySections))
    else:
        print("Funny: NO")
        funnyString = "NO"
        funny2 = "N/A"
        funny3 = "N/A"
        funny4 = "N/A"

    if isScary.get() == 1:
        print("Scary: YES, " + str(scaryRating) + " out of 10")
        print("Scary Section(s): " + str(getFrameTimes(scarySections)))
        print("Scary Section(s): " + str(getImageNumbers(scarySections)))
        scaryString = "YES"
        scary2 = str(scaryRating)
        scary3 = str(getFrameTimes(scarySections))
        scary4 = str(getImageNumbers(scarySections))
    else:
        print("Scary: NO")
        scaryString = "NO"
        scary2 = "N/A"
        scary3 = "N/A"
        scary4 = "N/A"

    if isSexy.get() == 1:
        print("Sexy: YES, " + str(sexyRating) + " out of 10")
        print("Sexy Section(s): " + str(getFrameTimes(sexySections)))
        print("Sexy Section(s): " + str(getImageNumbers(sexySections)))
        sexyString = "YES"
        sexy2 = str(sexyRating)
        sexy3 = str(getFrameTimes(sexySections))
        sexy4 = str(getImageNumbers(sexySections))
    else:
        print("Sexy: NO")
        sexyString = "NO"
        sexy2 = "N/A"
        sexy3 = "N/A"
        sexy4 = "N/A"

    print("")
    allRows.append(
        [
            userID,
            MovieTrailerList[trailerBlock][currentMovieNumber],
            trailerBlockString,
            funnyString,
            funny2,
            funny3,
            funny4,
            scaryString,
            scary2,
            scary3,
            scary4,
            sexyString,
            sexy2,
            sexy3,
            sexy4,
        ]
    )

    with open("./Output-Logs/Results.csv", "a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(allRows)


def SayThankYou():
    # Another window will popup at the end thanking the user for their participation
    # RatingsWindow.withdraw()
    ThankYouWindow.update()
    ThankYouWindow.deiconify()

    ThankYouWindow.title("Movie Trailer Rating Program")
    ThankYouWindow.geometry("500x100")
    ThankYouWindow.minsize(500, 100)

    lbl = Label(
        ThankYouWindow,
        text="\nThank you for your participation in \nthe experiment, your results are greatly appreciated.\n You may now exit the program.",
        font=(25),
    )
    lbl.config(anchor=CENTER)
    lbl.pack(padx=0, pady=0)

    center(ThankYouWindow)


# Get all of the GUI's ready for the next trailer (i.e. change the images/frames), and reset all of the variables so old data is not passed forward unintentionally
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

    global startFrame
    global endFrame

    # This is where the output data for the last trailer will be saved to the excel file ******
    SaveData()

    if len(MovieTrailerList[trailerBlock]) == (currentMovieNumber + 1):
        # print("No More Trailers")
        SayThankYou()
    else:
        # print("More Trailers")
        currentMovieNumber = currentMovieNumber + 1

        # Reset all of the variables and GUI's
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

        isFunny.set(0)
        isScary.set(0)
        isSexy.set(0)

        s1.set(1)
        s2.set(1)
        s3.set(1)

        startFrame = 0
        endFrame = 0

        lbl7.config(state=NORMAL)
        s1.config(state=NORMAL)

        lbl8.config(state=NORMAL)
        s2.config(state=NORMAL)

        lbl9.config(state=NORMAL)
        s3.config(state=NORMAL)

        # Funny Frames
        im = Image.open(
            "./Movie-Trailers/"
            + "Block_"
            + str(trailerBlock)
            + "/"
            + MovieTrailerList[trailerBlock][currentMovieNumber]
            + "/image0.jpg"
        )
        resized = im.resize((400, 225), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)
        myvar = Label(FrameSelectionWindowFunny, image=tkimage)
        myvar.image = tkimage
        myvar.grid(row=1, column=0, columnspan=2)

        scaleFunny.set(0)

        tempNumber = glob.glob(
            "./Movie-Trailers/"
            + "Block_"
            + str(trailerBlock)
            + "/"
            + MovieTrailerList[trailerBlock][currentMovieNumber]
            + "/image*"
        )
        scaleFunny.config(to=len(tempNumber) - 1)

        funnyListBox.delete(0, "end")

        # Scary Frames
        im = Image.open(
            "./Movie-Trailers/"
            + "Block_"
            + str(trailerBlock)
            + "/"
            + MovieTrailerList[trailerBlock][currentMovieNumber]
            + "/image0.jpg"
        )
        resized = im.resize((400, 225), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)
        myvar = Label(FrameSelectionWindowScary, image=tkimage)
        myvar.image = tkimage
        myvar.grid(row=1, column=0, columnspan=2)

        scaleScary.set(0)

        tempNumber = glob.glob(
            "./Movie-Trailers/"
            + "Block_"
            + str(trailerBlock)
            + "/"
            + MovieTrailerList[trailerBlock][currentMovieNumber]
            + "/image*"
        )
        scaleScary.config(to=len(tempNumber) - 1)

        scaryListBox.delete(0, "end")

        # Sexy Frames
        im = Image.open(
            "./Movie-Trailers/"
            + "Block_"
            + str(trailerBlock)
            + "/"
            + MovieTrailerList[trailerBlock][currentMovieNumber]
            + "/image0.jpg"
        )
        resized = im.resize((400, 225), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)
        myvar = Label(FrameSelectionWindowSexy, image=tkimage)
        myvar.image = tkimage
        myvar.grid(row=1, column=0, columnspan=2)

        scaleSexy.set(0)

        tempNumber = glob.glob(
            "./Movie-Trailers/"
            + "Block_"
            + str(trailerBlock)
            + "/"
            + MovieTrailerList[trailerBlock][currentMovieNumber]
            + "/image*"
        )
        scaleSexy.config(to=len(tempNumber) - 1)

        sexyListBox.delete(0, "end")

        CreateSelectVideoWindow()


def funnyClick():
    FrameSelectionWindowFunny.withdraw()
    ShowIndividualFrames()


def scaryClick():
    FrameSelectionWindowScary.withdraw()
    ShowIndividualFrames()


def sexyClick():
    FrameSelectionWindowSexy.withdraw()
    ShowIndividualFrames()


# Show each of the windows based on prior user input
def ShowIndividualFrames():
    global hasBeenToFunny
    global hasBeenToScary
    global hasBeenToSexy

    if (isFunny.get() == 1) and (hasBeenToFunny == False):
        FrameSelectionWindowFunny.update()
        FrameSelectionWindowFunny.deiconify()
        hasBeenToFunny = True
        center(FrameSelectionWindowFunny)
    elif (isScary.get() == 1) and (hasBeenToScary == False):
        FrameSelectionWindowScary.update()
        FrameSelectionWindowScary.deiconify()
        hasBeenToScary = True
        center(FrameSelectionWindowScary)
    elif (isSexy.get() == 1) and (hasBeenToSexy == False):
        FrameSelectionWindowSexy.update()
        FrameSelectionWindowSexy.deiconify()
        hasBeenToSexy = True
        center(FrameSelectionWindowSexy)
    else:
        GetNextTrailer()


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


def setTrailerBlock(val):
    global trailerBlock
    trailerBlock = int(val)


def CreateSpecificRatingsWindow():
    if (isFunny.get() == 0) and (isScary.get() == 0) and (isSexy.get() == 0):
        # Skip to the next trailer
        RatingsWindow.withdraw()
        GetNextTrailer()
    else:
        RatingsWindow.withdraw()
        SpecificRatingsWindow.update()
        SpecificRatingsWindow.deiconify()

        center(SpecificRatingsWindow)

        if isFunny.get() == 0:
            lbl7.config(state=DISABLED)
            s1.config(state=DISABLED)

        if isScary.get() == 0:
            lbl8.config(state=DISABLED)
            s2.config(state=DISABLED)

        if isSexy.get() == 0:
            lbl9.config(state=DISABLED)
            s3.config(state=DISABLED)


def CreateRatingsWindow():
    # Send a signal to the BIOPAC so it knows when the movie trailer has finished (over port FIO1)
    biopacConnectionPort.setFIOState(1, 1)
    time.sleep(0.2)
    biopacConnectionPort.setFIOState(1, 0)
    time.sleep(0.2)
    biopacConnectionPort.setFIOState(1, 1)

    VideoWindow.withdraw()
    RatingsWindow.update()
    RatingsWindow.deiconify()
    center(RatingsWindow)


def CreateTrailerBlockWindow():
    global userID
    userIDWindow.withdraw()
    trailerBlockWindow.update()
    trailerBlockWindow.deiconify()
    center(trailerBlockWindow)

    userID = userIDInput.get()


def CreateVideoWindow():
    SelectVideoWindow.withdraw()
    VideoWindow.update()
    VideoWindow.deiconify()
    center(VideoWindow)

    # Send a signal to the BIOPAC so it knows when the movie trailer has begun (over port FIO0)
    biopacConnectionPort.setFIOState(0, 1)
    time.sleep(0.2)
    biopacConnectionPort.setFIOState(0, 0)
    time.sleep(0.2)
    biopacConnectionPort.setFIOState(0, 1)

    # Movie titles cannot have any spaces and/or special characters
    movieLocation = (
        "vlc "
        + os.getcwd()
        + "/Movie-Trailers/"
        + "Block_"
        + str(trailerBlock)
        + "/"
        + MovieTrailerList[trailerBlock][currentMovieNumber]
        + ".avi vlc://quit > /dev/null 2>&1"
    )

    os.system(movieLocation)


def CreateSelectVideoWindow():
    trailerBlockWindow.withdraw()
    SelectVideoWindow.update()
    SelectVideoWindow.deiconify()
    center(SelectVideoWindow)

    # Set Funny Frames
    im = Image.open(
        "./Movie-Trailers/"
        + "Block_"
        + str(trailerBlock)
        + "/"
        + MovieTrailerList[trailerBlock][currentMovieNumber]
        + "/image0.jpg"
    )
    resized = im.resize((400, 225), Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(resized)
    myvar = Label(FrameSelectionWindowFunny, image=tkimage)
    myvar.image = tkimage
    myvar.grid(row=1, column=0, columnspan=2)

    # Set Scary Frames
    im = Image.open(
        "./Movie-Trailers/"
        + "Block_"
        + str(trailerBlock)
        + "/"
        + MovieTrailerList[trailerBlock][currentMovieNumber]
        + "/image0.jpg"
    )
    resized = im.resize((400, 225), Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(resized)
    myvar = Label(FrameSelectionWindowScary, image=tkimage)
    myvar.image = tkimage
    myvar.grid(row=1, column=0, columnspan=2)

    # Set Sexy Frames
    im = Image.open(
        "./Movie-Trailers/"
        + "Block_"
        + str(trailerBlock)
        + "/"
        + MovieTrailerList[trailerBlock][currentMovieNumber]
        + "/image0.jpg"
    )
    resized = im.resize((400, 225), Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(resized)
    myvar = Label(FrameSelectionWindowSexy, image=tkimage)
    myvar.image = tkimage
    myvar.grid(row=1, column=0, columnspan=2)

    nextMovieTrailerlbl.config(text=MovieTrailerList[trailerBlock][currentMovieNumber])


def CreateuserIDWindow():
    mainWindow.withdraw()
    userIDWindow.update()
    userIDWindow.deiconify()
    center(userIDWindow)


# Main Menu Window -----------------------------
# This window states the program name and allows the user to begin the experiment

mainWindow.title("Movie Trailer Rating Program")
mainWindow.geometry("425x250")
mainWindow.minsize(375, 250)
mainWindow.resizable(False, False)

# Add UOttawa Logo to login screen
img = Image.open("./Images/uottawa_ver_black.png")
img = img.resize((100, 100), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
panel = Label(mainWindow, image=img)
panel.pack(padx=0, pady=15)

lbl = Label(
    mainWindow, text="Welcome to the Movie Trailer Rating Experiment!", font=(25)
)
lbl.config(anchor=CENTER)
lbl.pack(padx=0, pady=0)

center(mainWindow)

# -----------------------------------------


# UserID Entry Window -----------------------------
# This window allows the user to enter their user ID for statistical purposes

userIDWindow.title("Movie Trailer Rating Program")
userIDWindow.geometry("300x100")
userIDWindow.minsize(275, 100)
userIDWindow.resizable(False, False)

userIDlbl = Label(userIDWindow, text="User ID: ", font=(20))
userIDlbl.grid(column=0, row=0)

userIDInput = Entry(userIDWindow, width=20, font=(20))
userIDInput.grid(column=1, row=0)

btn = Button(
    userIDWindow, text="Begin Testing", command=CreateTrailerBlockWindow, font=(25)
)
btn.grid(column=0, row=2, columnspan=2, pady=10)

userIDWindow.grid_rowconfigure(0, weight=1)
userIDWindow.grid_rowconfigure(1, weight=1)
userIDWindow.grid_rowconfigure(2, weight=1)
userIDWindow.grid_columnconfigure(0, weight=1)
userIDWindow.grid_columnconfigure(1, weight=1)

# -----------------------------------------


# Preview Name of Video Trailer Window ----------------------------
# This window allows the user to view what the title of the next movie trailer is, and allows them to take a break before playing the next trailer

SelectVideoWindow.title("Movie Trailer Rating Program")
SelectVideoWindow.geometry("350x175")
SelectVideoWindow.minsize(350, 175)
SelectVideoWindow.resizable(False, False)

firstNamelbl = Label(SelectVideoWindow, text="Next Movie Trailer:", font=(20))
firstNamelbl.config(anchor=CENTER)
firstNamelbl.pack(padx=0, pady=10)

nextMovieTrailerlbl = Label(SelectVideoWindow, text="...", font=(20))
nextMovieTrailerlbl.config(anchor=CENTER)
nextMovieTrailerlbl.pack(padx=0, pady=10)

btn3 = Button(
    SelectVideoWindow, text="Start Trailer", command=CreateVideoWindow, font=(25)
)
btn3.pack(padx=0, pady=10)

# -----------------------------------------


# Video Player Window ----------------------------
# This window allows the user to press continue once the movie trailer is finished

VideoWindow.title("Movie Trailer Rating Program")
VideoWindow.geometry("450x100")
VideoWindow.minsize(450, 100)
VideoWindow.resizable(False, False)

lbl4 = Label(
    VideoWindow, text="When trailer is finished, please press continue", font=(25)
)
lbl4.config(anchor=CENTER)
lbl4.pack(padx=0, pady=10)

btn4 = Button(VideoWindow, text="Continue", command=CreateRatingsWindow, font=(25))
btn4.config(anchor=CENTER)
btn4.pack(padx=0, pady=15)

# -----------------------------------------

# Trailer Rating Window ----------------------------
# This window allows the user to select if the trailer contained any funny, scary or sexy content

RatingsWindow.title("Movie Trailer Rating Program")
RatingsWindow.geometry("300x275")
RatingsWindow.minsize(300, 275)
RatingsWindow.resizable(False, False)

lbl5 = Label(
    RatingsWindow,
    text="Did the video content contain any\n of the following?",
    font=(25),
)
lbl5.grid(column=0, row=0, pady=10)

c1 = Checkbutton(RatingsWindow, text="Funny Content", variable=isFunny, font=(25))
c1.grid(column=0, row=1)

c2 = Checkbutton(RatingsWindow, text="Scary Content", variable=isScary, font=(25))
c2.grid(column=0, row=2)

c3 = Checkbutton(RatingsWindow, text="Sexy Content", variable=isSexy, font=(25))
c3.grid(column=0, row=3)

btn5 = Button(
    RatingsWindow, text="Next", command=CreateSpecificRatingsWindow, font=(25)
)
btn5.grid(column=0, row=4, pady=10)

RatingsWindow.grid_rowconfigure(0, weight=1)
RatingsWindow.grid_rowconfigure(1, weight=1)
RatingsWindow.grid_rowconfigure(2, weight=1)
RatingsWindow.grid_rowconfigure(3, weight=1)
RatingsWindow.grid_rowconfigure(4, weight=1)
RatingsWindow.grid_columnconfigure(0, weight=1)

# -----------------------------------------

# Specific Ratings Window ----------------------------
# This window will allow for the user to rate (on a scale of 1-10), how much of each selected content there was in the Movie Trailer

SpecificRatingsWindow.title("Movie Trailer Rating Program")
SpecificRatingsWindow.geometry("300x275")
SpecificRatingsWindow.minsize(300, 275)
SpecificRatingsWindow.resizable(False, False)

lbl6 = Label(
    SpecificRatingsWindow,
    text="Please rate the content presence\n on a scale of 1-10?",
    font=(25),
)
lbl6.grid(column=0, row=0, columnspan=2, pady=10)

lbl7 = Label(SpecificRatingsWindow, text="Funny", font=(25))
lbl7.grid(column=0, row=1)

s1 = Scale(
    SpecificRatingsWindow, from_=1, to=10, orient=HORIZONTAL, command=setFunnyRating
)
s1.grid(column=1, row=1)

seperator10 = ttk.Separator(SpecificRatingsWindow, orient=HORIZONTAL).grid(
    row=2, columnspan=2, sticky="ew"
)

lbl8 = Label(SpecificRatingsWindow, text="Scary", font=(25))
lbl8.grid(column=0, row=3)

s2 = Scale(
    SpecificRatingsWindow, from_=1, to=10, orient=HORIZONTAL, command=setScaryRating
)
s2.grid(column=1, row=3)

seperator11 = ttk.Separator(SpecificRatingsWindow, orient=HORIZONTAL).grid(
    row=4, columnspan=2, sticky="ew"
)

lbl9 = Label(SpecificRatingsWindow, text="Sexy", font=(25))
lbl9.grid(column=0, row=5)

s3 = Scale(
    SpecificRatingsWindow, from_=1, to=10, orient=HORIZONTAL, command=setSexyRating
)
s3.grid(column=1, row=5)

btn5 = Button(
    SpecificRatingsWindow, text="Next", command=GetIndividualFrames, font=(25)
)
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

# -----------------------------------------


def funnySpecificFrame(val):
    global currentFunny
    currentFunny = int(val)
    im = Image.open(
        "./Movie-Trailers/"
        + "Block_"
        + str(trailerBlock)
        + "/"
        + MovieTrailerList[trailerBlock][currentMovieNumber]
        + "/image"
        + str(val)
        + ".jpg"
    )
    resized = im.resize((400, 225), Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(resized)
    myvar = Label(FrameSelectionWindowFunny, image=tkimage)
    myvar.image = tkimage
    myvar.grid(row=1, column=0, columnspan=2)

    FrameSelectionWindowFunny.update()
    FrameSelectionWindowFunny.deiconify()


def funnyClickBegin(event=None):
    global currentFunny
    global startFrame
    startFrame = currentFunny
    FrameSelectionWindowFunnybutton2.config(state=NORMAL)


def funnyClickEnd(event=None):
    global startFrame
    global currentFunny
    global endFrame
    global funnyListBoxCount
    endFrame = currentFunny

    if (startFrame > -1) and (startFrame is not endFrame) and (startFrame < endFrame):
        funnySections.append([startFrame, endFrame])

        funnyListBoxCount = funnyListBoxCount + 1
        funnyListBox.insert(
            funnyListBoxCount,
            "Frame: " + str(startFrame) + ", to Frame: " + str(endFrame),
        )

        startFrame = 0
        endFrame = 0
        FrameSelectionWindowFunnybutton2.config(state=DISABLED)


def funnyRemove():
    # Add Try Catch Statment
    try:
        text = funnyListBox.get(funnyListBox.curselection())
        funnyListBox.delete(funnyListBox.curselection())
        first = text

        temp = first.split(", to Frame")

        first = temp[0].replace("Frame: ", "")
        second = temp[1].replace(": ", "")

        tempList = [int(first), int(second)]
        funnySections.remove(tempList)

    except:
        messagebox.showerror("Error", "Please select a valid frame selection to delete")


def funnyNextFrame(event=None):
    global currentFunny
    global currentMovieNumber

    tempNumber = glob.glob(
        "./Movie-Trailers/"
        + "Block_"
        + str(trailerBlock)
        + "/"
        + MovieTrailerList[trailerBlock][currentMovieNumber]
        + "/image*"
    )

    if currentFunny + 1 <= (len(tempNumber) - 1):
        funnySpecificFrame(currentFunny + 1)
        scaleFunny.set(currentFunny)


def funnyPreviousFrame(event=None):
    global currentFunny

    if currentFunny - 1 >= 0:
        funnySpecificFrame(currentFunny - 1)
        scaleFunny.set(currentFunny)


# -----------------------------------------

# Frame Selection Window Funny ----------------------------
# This window will allow for the user to select which frame(s) contain the specified content

FrameSelectionWindowFunny.title("Movie Trailer Rating Program")
FrameSelectionWindowFunny.geometry("500x700")
FrameSelectionWindowFunny.resizable(False, False)

FrameSelectionWindowTitleFunnylbl = Label(
    FrameSelectionWindowFunny,
    text="Please select the frames that contain funny content",
    font=(25),
)
FrameSelectionWindowTitleFunnylbl.grid(column=0, row=0, columnspan=2, pady=10)

# Add image section here (bookmarked page on web)
im = Image.open(
    "./Movie-Trailers/"
    + "Block_"
    + str(trailerBlock)
    + "/"
    + MovieTrailerList[trailerBlock][currentMovieNumber]
    + "/image0.jpg"
)
resized = im.resize((400, 225), Image.ANTIALIAS)
tkimage = ImageTk.PhotoImage(resized)
myvar = Label(FrameSelectionWindowFunny, image=tkimage)
myvar.image = tkimage
myvar.grid(row=1, column=0, columnspan=2)

tempNumber = glob.glob(
    "./Movie-Trailers/"
    + "Block_"
    + str(trailerBlock)
    + "/"
    + MovieTrailerList[trailerBlock][currentMovieNumber]
    + "/image*"
)

scaleFunny = Scale(
    FrameSelectionWindowFunny,
    from_=0,
    to=len(tempNumber) - 1,
    orient=HORIZONTAL,
    command=funnySpecificFrame,
    length=450,
)
scaleFunny.grid(column=0, row=2, columnspan=2, pady=10)

FrameSelectionWindowFunny.bind("<Right>", funnyNextFrame)
FrameSelectionWindowFunny.bind("<Left>", funnyPreviousFrame)

FrameSelectionWindowFunnybutton1 = Button(
    FrameSelectionWindowFunny,
    text="Begin Selection",
    command=funnyClickBegin,
    font=(25),
)
FrameSelectionWindowFunnybutton1.grid(column=0, row=3, pady=10)

FrameSelectionWindowFunny.bind("<KeyPress-Shift_L>", funnyClickBegin)

FrameSelectionWindowFunnybutton2 = Button(
    FrameSelectionWindowFunny, text="End Selection", command=funnyClickEnd, font=(25)
)
FrameSelectionWindowFunnybutton2.grid(column=1, row=3, pady=10)

FrameSelectionWindowFunny.bind("<KeyRelease-Shift_L>", funnyClickEnd)

seperator1 = ttk.Separator(FrameSelectionWindowFunny, orient=HORIZONTAL).grid(
    row=4, columnspan=2, sticky="ew"
)

FrameSelectionWindowTitleFunnylbl2 = Label(
    FrameSelectionWindowFunny, text="Selected Frame Sections:", font=(25)
)
FrameSelectionWindowTitleFunnylbl2.grid(column=0, row=5, columnspan=2, pady=10)

funnyListBox = Listbox(FrameSelectionWindowFunny, width=60, selectmode=SINGLE)
funnyListBox.grid(column=0, row=6, columnspan=2, pady=10)

FrameSelectionWindowFunnybutton3 = Button(
    FrameSelectionWindowFunny, text="Remove Selection", command=funnyRemove, font=(25)
)
FrameSelectionWindowFunnybutton3.grid(column=0, row=7, pady=10)

FrameSelectionWindowFunnybutton = Button(
    FrameSelectionWindowFunny, text="Finished", command=funnyClick, font=(25)
)
FrameSelectionWindowFunnybutton.grid(column=1, row=7, pady=10)

FrameSelectionWindowFunny.grid_rowconfigure(0, weight=1)
FrameSelectionWindowFunny.grid_rowconfigure(1, weight=1)
FrameSelectionWindowFunny.grid_rowconfigure(2, weight=1)
FrameSelectionWindowFunny.grid_rowconfigure(3, weight=1)
FrameSelectionWindowFunny.grid_rowconfigure(4, weight=1)
FrameSelectionWindowFunny.grid_rowconfigure(5, weight=1)
FrameSelectionWindowFunny.grid_rowconfigure(6, weight=1)
FrameSelectionWindowFunny.grid_rowconfigure(7, weight=1)
FrameSelectionWindowFunny.grid_columnconfigure(0, weight=1)
FrameSelectionWindowFunny.grid_columnconfigure(1, weight=1)

# -----------------------------------------


def scarySpecificFrame(val):
    global currentScary
    currentScary = int(val)
    im = Image.open(
        "./Movie-Trailers/"
        + "Block_"
        + str(trailerBlock)
        + "/"
        + MovieTrailerList[trailerBlock][currentMovieNumber]
        + "/image"
        + str(val)
        + ".jpg"
    )
    resized = im.resize((400, 225), Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(resized)
    myvar = Label(FrameSelectionWindowScary, image=tkimage)
    myvar.image = tkimage
    myvar.grid(row=1, column=0, columnspan=2)

    FrameSelectionWindowScary.update()
    FrameSelectionWindowScary.deiconify()


def scaryClickBegin(event=None):
    global currentScary
    global startFrame
    startFrame = currentScary
    FrameSelectionWindowScarybutton2.config(state=NORMAL)


def scaryClickEnd(event=None):
    global startFrame
    global currentScary
    global endFrame
    global scaryListBoxCount
    endFrame = currentScary

    if (startFrame > -1) and (startFrame is not endFrame) and (startFrame < endFrame):
        scarySections.append([startFrame, endFrame])

        scaryListBoxCount = scaryListBoxCount + 1
        scaryListBox.insert(
            scaryListBoxCount,
            "Frame: " + str(startFrame) + ", to Frame: " + str(endFrame),
        )

        startFrame = 0
        endFrame = 0
        FrameSelectionWindowScarybutton2.config(state=DISABLED)


def scaryRemove():
    # Add Try Catch Statment
    try:
        text = scaryListBox.get(scaryListBox.curselection())
        scaryListBox.delete(scaryListBox.curselection())
        first = text

        temp = first.split(", to Frame")

        first = temp[0].replace("Frame: ", "")
        second = temp[1].replace(": ", "")

        tempList = [int(first), int(second)]
        scarySections.remove(tempList)
    except:
        messagebox.showerror("Error", "Please select a valid frame selection to delete")


def scaryNextFrame(event=None):
    global currentScary
    global currentMovieNumber

    tempNumber = glob.glob(
        "./Movie-Trailers/"
        + "Block_"
        + str(trailerBlock)
        + "/"
        + MovieTrailerList[trailerBlock][currentMovieNumber]
        + "/image*"
    )

    if currentScary + 1 <= (len(tempNumber) - 1):
        scarySpecificFrame(currentScary + 1)
        scaleScary.set(currentScary)


def scaryPreviousFrame(event=None):
    global currentScary

    if currentScary - 1 >= 0:
        scarySpecificFrame(currentScary - 1)
        scaleScary.set(currentScary)


# -----------------------------------------

# Frame Selection Window Scary ----------------------------
# This window will allow for the user to select which frame(s) contain the specified content

FrameSelectionWindowScary.title("Movie Trailer Rating Program")
FrameSelectionWindowScary.geometry("500x700")
FrameSelectionWindowScary.resizable(False, False)

FrameSelectionWindowTitleScarylbl = Label(
    FrameSelectionWindowScary,
    text="Please select the frames that contain scary content",
    font=(25),
)
FrameSelectionWindowTitleScarylbl.grid(column=0, row=0, columnspan=2, pady=10)

# Add image section here (bookmarked page on web)
im = Image.open(
    "./Movie-Trailers/"
    + "Block_"
    + str(trailerBlock)
    + "/"
    + MovieTrailerList[trailerBlock][currentMovieNumber]
    + "/image0.jpg"
)
resized = im.resize((400, 225), Image.ANTIALIAS)
tkimage = ImageTk.PhotoImage(resized)
myvar = Label(FrameSelectionWindowScary, image=tkimage)
myvar.image = tkimage
myvar.grid(row=1, column=0, columnspan=2)

tempNumber = glob.glob(
    "./Movie-Trailers/"
    + "Block_"
    + str(trailerBlock)
    + "/"
    + MovieTrailerList[trailerBlock][currentMovieNumber]
    + "/image*"
)

scaleScary = Scale(
    FrameSelectionWindowScary,
    from_=0,
    to=len(tempNumber) - 1,
    orient=HORIZONTAL,
    command=scarySpecificFrame,
    length=450,
)
scaleScary.grid(column=0, row=2, columnspan=2, pady=10)

FrameSelectionWindowScary.bind("<Right>", scaryNextFrame)
FrameSelectionWindowScary.bind("<Left>", scaryPreviousFrame)

FrameSelectionWindowScarybutton1 = Button(
    FrameSelectionWindowScary,
    text="Begin Selection",
    command=scaryClickBegin,
    font=(25),
)
FrameSelectionWindowScarybutton1.grid(column=0, row=3, pady=10)

FrameSelectionWindowScary.bind("<KeyPress-Shift_L>", scaryClickBegin)

FrameSelectionWindowScarybutton2 = Button(
    FrameSelectionWindowScary, text="End Selection", command=scaryClickEnd, font=(25)
)
FrameSelectionWindowScarybutton2.grid(column=1, row=3, pady=10)

FrameSelectionWindowScary.bind("<KeyRelease-Shift_L>", scaryClickEnd)

seperator1 = ttk.Separator(FrameSelectionWindowScary, orient=HORIZONTAL).grid(
    row=4, columnspan=2, sticky="ew"
)

FrameSelectionWindowTitleScarylbl2 = Label(
    FrameSelectionWindowScary, text="Selected Frame Sections:", font=(25)
)
FrameSelectionWindowTitleScarylbl2.grid(column=0, row=5, columnspan=2, pady=10)

scaryListBox = Listbox(FrameSelectionWindowScary, width=60, selectmode=SINGLE)
scaryListBox.grid(column=0, row=6, columnspan=2, pady=10)

FrameSelectionWindowScarybutton3 = Button(
    FrameSelectionWindowScary, text="Remove Selection", command=scaryRemove, font=(25)
)
FrameSelectionWindowScarybutton3.grid(column=0, row=7, pady=10)

FrameSelectionWindowScarybutton = Button(
    FrameSelectionWindowScary, text="Finished", command=scaryClick, font=(25)
)
FrameSelectionWindowScarybutton.grid(column=1, row=7, pady=10)

FrameSelectionWindowScary.grid_rowconfigure(0, weight=1)
FrameSelectionWindowScary.grid_rowconfigure(1, weight=1)
FrameSelectionWindowScary.grid_rowconfigure(2, weight=1)
FrameSelectionWindowScary.grid_rowconfigure(3, weight=1)
FrameSelectionWindowScary.grid_rowconfigure(4, weight=1)
FrameSelectionWindowScary.grid_rowconfigure(5, weight=1)
FrameSelectionWindowScary.grid_rowconfigure(6, weight=1)
FrameSelectionWindowScary.grid_rowconfigure(7, weight=1)
FrameSelectionWindowScary.grid_columnconfigure(0, weight=1)
FrameSelectionWindowScary.grid_columnconfigure(1, weight=1)

# -----------------------------------------


def sexySpecificFrame(val):
    global currentSexy
    currentSexy = int(val)
    im = Image.open(
        "./Movie-Trailers/"
        + "Block_"
        + str(trailerBlock)
        + "/"
        + MovieTrailerList[trailerBlock][currentMovieNumber]
        + "/image"
        + str(val)
        + ".jpg"
    )
    resized = im.resize((400, 225), Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(resized)
    myvar = Label(FrameSelectionWindowSexy, image=tkimage)
    myvar.image = tkimage
    myvar.grid(row=1, column=0, columnspan=2)

    FrameSelectionWindowSexy.update()
    FrameSelectionWindowSexy.deiconify()


def sexyClickBegin(event=None):
    global currentSexy
    global startFrame
    startFrame = currentSexy
    FrameSelectionWindowSexybutton2.config(state=NORMAL)


def sexyClickEnd(event=None):
    global startFrame
    global currentSexy
    global endFrame
    global sexyListBoxCount
    endFrame = currentSexy

    if (startFrame > -1) and (startFrame is not endFrame) and (startFrame < endFrame):
        sexySections.append([startFrame, endFrame])

        sexyListBoxCount = sexyListBoxCount + 1
        sexyListBox.insert(
            sexyListBoxCount,
            "Frame: " + str(startFrame) + ", to Frame: " + str(endFrame),
        )

        startFrame = 0
        endFrame = 0
        FrameSelectionWindowSexybutton2.config(state=DISABLED)


def sexyRemove():
    # Add Try Catch Statment
    try:
        text = sexyListBox.get(sexyListBox.curselection())
        sexyListBox.delete(sexyListBox.curselection())
        first = text

        temp = first.split(", to Frame")

        first = temp[0].replace("Frame: ", "")
        second = temp[1].replace(": ", "")

        tempList = [int(first), int(second)]
        sexySections.remove(tempList)
    except:
        messagebox.showerror("Error", "Please select a valid frame selection to delete")


def sexyNextFrame(event=None):
    global currentSexy
    global currentMovieNumber

    tempNumber = glob.glob(
        "./Movie-Trailers/"
        + "Block_"
        + str(trailerBlock)
        + "/"
        + MovieTrailerList[trailerBlock][currentMovieNumber]
        + "/image*"
    )

    if currentSexy + 1 <= (len(tempNumber) - 1):
        sexySpecificFrame(currentSexy + 1)
        scaleSexy.set(currentSexy)


def sexyPreviousFrame(event=None):
    global currentSexy

    if currentSexy - 1 >= 0:
        sexySpecificFrame(currentSexy - 1)
        scaleSexy.set(currentSexy)


# -----------------------------------------

# Frame Selection Window Sexy ----------------------------
# This window will allow for the user to select which frame(s) contain the specified content

FrameSelectionWindowSexy.title("Movie Trailer Rating Program")
FrameSelectionWindowSexy.geometry("500x700")
FrameSelectionWindowSexy.resizable(False, False)

FrameSelectionWindowTitleSexylbl = Label(
    FrameSelectionWindowSexy,
    text="Please select the frames that contain sexy content",
    font=(25),
)
FrameSelectionWindowTitleSexylbl.grid(column=0, row=0, columnspan=2, pady=10)

# Add image section here (bookmarked page on web)
im = Image.open(
    "./Movie-Trailers/"
    + "Block_"
    + str(trailerBlock)
    + "/"
    + MovieTrailerList[trailerBlock][currentMovieNumber]
    + "/image0.jpg"
)
resized = im.resize((400, 225), Image.ANTIALIAS)
tkimage = ImageTk.PhotoImage(resized)
myvar = Label(FrameSelectionWindowSexy, image=tkimage)
myvar.image = tkimage
myvar.grid(row=1, column=0, columnspan=2)

tempNumber = glob.glob(
    "./Movie-Trailers/"
    + "Block_"
    + str(trailerBlock)
    + "/"
    + MovieTrailerList[trailerBlock][currentMovieNumber]
    + "/image*"
)

scaleSexy = Scale(
    FrameSelectionWindowSexy,
    from_=0,
    to=len(tempNumber) - 1,
    orient=HORIZONTAL,
    command=sexySpecificFrame,
    length=450,
)
scaleSexy.grid(column=0, row=2, columnspan=2, pady=10)

FrameSelectionWindowSexy.bind("<Right>", sexyNextFrame)
FrameSelectionWindowSexy.bind("<Left>", sexyPreviousFrame)

FrameSelectionWindowSexybutton1 = Button(
    FrameSelectionWindowSexy, text="Begin Selection", command=sexyClickBegin, font=(25)
)
FrameSelectionWindowSexybutton1.grid(column=0, row=3, pady=10)

FrameSelectionWindowSexy.bind("<KeyPress-Shift_L>", sexyClickBegin)

FrameSelectionWindowSexybutton2 = Button(
    FrameSelectionWindowSexy, text="End Selection", command=sexyClickEnd, font=(25)
)
FrameSelectionWindowSexybutton2.grid(column=1, row=3, pady=10)

FrameSelectionWindowSexy.bind("<KeyRelease-Shift_L>", sexyClickEnd)

seperator1 = ttk.Separator(FrameSelectionWindowSexy, orient=HORIZONTAL).grid(
    row=4, columnspan=2, sticky="ew"
)

FrameSelectionWindowTitleSexylbl2 = Label(
    FrameSelectionWindowSexy, text="Selected Frame Sections:", font=(25)
)
FrameSelectionWindowTitleSexylbl2.grid(column=0, row=5, columnspan=2, pady=10)

sexyListBox = Listbox(FrameSelectionWindowSexy, width=60, selectmode=SINGLE)
sexyListBox.grid(column=0, row=6, columnspan=2, pady=10)

FrameSelectionWindowSexybutton3 = Button(
    FrameSelectionWindowSexy, text="Remove Selection", command=sexyRemove, font=(25)
)
FrameSelectionWindowSexybutton3.grid(column=0, row=7, pady=10)

FrameSelectionWindowSexybutton = Button(
    FrameSelectionWindowSexy, text="Finished", command=sexyClick, font=(25)
)
FrameSelectionWindowSexybutton.grid(column=1, row=7, pady=10)

FrameSelectionWindowSexy.grid_rowconfigure(0, weight=1)
FrameSelectionWindowSexy.grid_rowconfigure(1, weight=1)
FrameSelectionWindowSexy.grid_rowconfigure(2, weight=1)
FrameSelectionWindowSexy.grid_rowconfigure(3, weight=1)
FrameSelectionWindowSexy.grid_rowconfigure(4, weight=1)
FrameSelectionWindowSexy.grid_rowconfigure(5, weight=1)
FrameSelectionWindowSexy.grid_rowconfigure(6, weight=1)
FrameSelectionWindowSexy.grid_rowconfigure(7, weight=1)
FrameSelectionWindowSexy.grid_columnconfigure(0, weight=1)
FrameSelectionWindowSexy.grid_columnconfigure(1, weight=1)

# -----------------------------------------

# Trailer Block Window ----------------------------
# This window will allow for the user to select (from 1 to 5 inclusive) which trailer block they want to view trailers from

trailerBlockWindow.title("Movie Trailer Rating Program")
trailerBlockWindow.geometry("300x200")
trailerBlockWindow.resizable(False, False)

trailerBlockWindowlbl1 = Label(
    trailerBlockWindow,
    text="Which Movie Trailer Block would\n you like to select?",
    font=(25),
)
trailerBlockWindowlbl1.grid(column=0, row=0, pady=10)

trailerBlockWindowSlider = Scale(
    trailerBlockWindow,
    from_=1,
    to=5,
    length=250,
    tickinterval=1,
    orient=HORIZONTAL,
    command=setTrailerBlock,
)
trailerBlockWindowSlider.set(1)
trailerBlockWindowSlider.grid(column=0, row=1, pady=10)

trailerBlockWindowbtn = Button(
    trailerBlockWindow, text="Continue", command=CreateSelectVideoWindow, font=(25)
)
trailerBlockWindowbtn.grid(column=0, row=2, pady=10)

trailerBlockWindow.grid_rowconfigure(0, weight=1)
trailerBlockWindow.grid_rowconfigure(1, weight=1)
trailerBlockWindow.grid_rowconfigure(2, weight=1)
trailerBlockWindow.grid_columnconfigure(0, weight=1)

# -----------------------------------------

btn2 = Button(mainWindow, text="Start", command=CreateuserIDWindow, font=(25))
btn2.config(anchor=CENTER)
btn2.pack(padx=0, pady=15)

# Start the program
mainWindow.mainloop()
