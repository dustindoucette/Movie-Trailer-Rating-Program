# Movie-Trailer-Rating-Program

This project is intended to be used within the Cassidy Lab (The Royal’s Institute of Mental Health Research, affiliated with uOttawa) for experiments conducted to study users interpretations of Movie Trailers.

This Python program was created by Dustin Doucette (BCS), a Computer Science graduate from Carleton University.

## Program Requirements

* Latest version of Python 3 ([download](https://www.python.org/downloads/))

    **Note:** For ease of use, ensure Python gets added to the PATH environment variable during installation

* LabJack UD Driver ([download](https://labjack.com/support/software/installers/ud))

* External Python Modules:

      -Pillow

      -OpenCV-Python

      -Pyglet

      -LabJackPython

      -ffmpeg

## Installation

1. Click `Clone or download` then `Download ZIP` on the main repository page (under the **'Main'** branch).

2. Unzip the downloaded file into a directory which contains no spaces.

    `./user/johndoe/Projects`    ~**GOOD**

    `./user/john doe/Projects`   ~**BAD**

3. Open a terminal and traverse to the directory which contains the downloaded program (e.g., `johndoe/Documents/MovieTrailerProgram/`).

4. Enter the following commands to install the required modules and dependencies:

    `sudo chmod +x setup-script.sh`

    `sudo ./setup-script.sh`

## Program Set-Up

* Place pre-downloaded AVI Movie Trailers into the folders `./Movie-Trailers/Block_1`, `./Movie-Trailers/Block_2`,`./Movie-Trailers/Block_3`, `./Movie-Trailers/Block_4`, and `./Movie-Trailers/Block_5`. Place 18 Movie Trailers in each folder so that there is a total of 90.

    **Note:** Movie Trailer filenames cannot have any special characters (including spaces). Instead replace spaces with underscores, and also remove any special characters entirely.

## Program Use Instructions

1. Open a terminal and traverse to the directory which contains the downloaded program (e.g., `johndoe/Documents/MovieTrailerProgram/`).

2. Execute the command `python3 ./Program.py`.

    **Note:** The first startup after placing new trailers in the movie trailer program will take longer to start the first GUI. This is because the program is taking individual frames out of the trailers for later use in the program.

3. Click `Start` in the main menu to begin the experiment.

4. Enter your user ID and press `Begin Testing`.

5. Adjust the slider to select which Movie Trailer Block to use for the current session, then press `Continue`.

6. Select `Start Trailer` to begin viewing the next trailer (a VLC window will pop-up and play the trailer).

7. After the movie trailer has finished, close the video application and press `Continue` on the program window.

9. Select all of the relevant boxes (if the movie trailer had funny, scary and/or sexy content), then press `Next`.

10. Adjust the sliders to reflect your ratings (scale of 1-10), then press `Next`.

10. Select all of the relevant frame sections which contain the specified content.

    **E.g.** If you want to select a scene from frame 10 to 20, first drag the slider to frame 10 and select `Begin Selection`. Then drag the slider to frame 20 and select `End Selection`. This will add that frame selection to a box below. If you made a mistake, simply click the selection and press `Remove Selection`. Once all frame sections are selected, press `Finished`.

    **Note:** You can also create a frame section by holding down the left Shift key and pressing the Left and Right arrow keys to adjust the frame selection. A new frame section will be created when you release the left Shift key.

    **Note:** You will be given a new window for each box you selected in step 8 (if no boxes were selected, skip to step 11).

13. If there are more movie trailers to be reviewed, the name of the next movie trailer will be displayed. Press `Start Trailer`. This will bring the user back to step 6.

14. If there are no more movie trailers to be reviewed, a thank you message is displayed, and you can now close the window (terminating the program).

## Program Considerations

* The program needs to have at least **one** movie trailer placed inside the folder `Movie-Trailers` to function properly.
* When the program is run for the first time after placing new trailers in the `Movie-Trailers` folder, allow the program to generate all of the frames (i.e., wait for the welcome GUI to pop-up) before terminating the program. If the program is terminated before all of the frames are created, the specific rating windows (funny, sexy, scary) will not display entire movie trailer(s), just the portion of which the frames were generated.
  * If the program is terminated before all of the frames are generated, traverse to the `Movie-Trailers` folder and within each block, delete the folders that are named after movie trailers. By deleting these folders, the program will be able to regenerate the frames properly; if the folders are there (but empty), the program will presume that the frames are already in it.

## Program Output

* After each individual completion of step 11 is completed, a new line is added to the excel output file named `Results.csv` located within the `Output-Logs` folder.

* The `Results.csv` file will have the following columns (one new line of data is added after every individual test):

| User ID   | Movie Trailer | Trailer Block | Funny | Funny Rating | Funny Sections (time) | Funny Sections (image #) | Scary | Scary Rating | Scary Sections (time)        | Scary Sections (image #)                                           | Sexy | Sexy Rating | Sexy Sections (time)        | Sexy Sections (image #)                                           |
|-----------|---------------|---------------|-------|--------------|-----------------------|--------------------------|-------|--------------|------------------------------|--------------------------------------------------------------------|------|-------------|-----------------------------|-------------------------------------------------------------------|
| 123456789 | 1917          | 1             | NO    | N/A          | N/A                   | N/A                      | YES   | 7            | [[12.5, 31.0], [54.0, 99.5]] | [['image25.jpg to image62.jpg'], ['image108.jpg to image199.jpg']] | NO   | N/A         | N/A                         | N/A                                                               |
| 987654321 | Annette       | 2             | NO    | N/A          | N/A                   | N/A                      | NO    | N/A          | N/A                          | N/A                                                                | YES  | 8           | [[0.0, 27.0], [57.0, 80.5]] | [[‘image0.jpg to image54.jpg’], [‘image114.jpg to image161.jpg’]] |

| Column             | Description of Data                                          |
| ------------------ | ------------------------------------------------------------ |
| **User ID**        | Displays the User ID of the participant                      |
| **Movie Trailer**  | Displays the name of the movie trailer that the participant is reviewing |
| **Trailer Block**  | Displays a number between 1 and 5, where the number corresponds to the Movie Trailer Block that the user has selected |
| **Funny**          | Displays whether or not the participant thinks the movie trailer contains funny content |
| **Funny Rating**   | Displays a number between 1-10, where the participant decides how funny the movie trailer content was |
| **Funny Sections (time)** | Displays comma separated tuples, where the first value is the start time (in seconds) and the second value is the end time (in seconds) of the funny content |
| **Funny Sections (image #)** | Displays the filenames for the first selected frame and last selected frame of each chosen funny section |
| **Scary**          | Displays whether or not the participant thinks the movie trailer contains Scary content |
| **Scary Rating**   | Displays a number between 1-10, where the participant decides how Scary the movie trailer content was |
| **Scary Sections (time)** | Displays comma separated tuples, where the first value is the start time (in seconds) and the second value is the end time (in seconds) of the Scary content |
| **Scary Sections (image #)** | Displays the filenames for the first selected frame and last selected frame of each chosen scary section |
| **Sexy**           | Displays whether or not the participant thinks the movie trailer contains Sexy content |
| **Sexy Rating**    | Displays a number between 1-10, where the participant decides how Sexy the movie trailer content was |
| **Sexy Sections (time)**  | Displays comma separated tuples, where the first value is the start time (in seconds) and the second value is the end time (in seconds) of the Sexy content |
| **Sexy Sections (image #)** | Displays the filenames for the first selected frame and last selected frame of each chosen sexy section |

  **Note:** Ensure the `Results.csv` file is not open during program execution. If the file is open when the program tries to write new data to it, the write operation will fail and that data will be lost.

## Frame Generation Check

Before now, there was no straightforward way to see to see if the number of frames generated for each movie trailer was correct. You had to manually check the folders which contain the images, and then manually divide the number of images by 2 and see if it matched with the length of the trailer. This was very inefficient and was prone to human error. As such, a 'sanity check' python script was created to verify whether or not the correct number of frames has been generated for each trailer. To run it, complete the following steps:

1. Open a terminal and traverse to the directory which contains the downloaded program (e.g., `johndoe/Documents/MovieTrailerProgram/`).

2. Execute the command `python3 ./VerifyFrames.py`.

Once the script terminates, it will tell you whether there were any 'errors' (i.e., # of frames generated does not match what it should be), or if everything passed.

## Project Files

By default, the project contains the following file and directory layout:

    ```
    Movie_Trailer_Program
    │   Program.py (Main Python Program)
    |   GenerateFrames.py (Generates individual frames for each movie trailer given to it)
    |   VerifyFrames.py (Verifies that the correct number of frames were generated for each movie trailer)
    |   setup-script.sh (Installs required dependencies and modules)
    |   README.md (This guide)
    |   .gitignore (Tells Git what files should be ignored)
    |   .pre-commit-config.yaml (Outlines the settings which should be used by the pre-commit hook)
    │
    └───Images
    │   │   uOttawa_icon.ico (UOttawa icon used as the favicon for each window)
    │   │   uottawa_ver_black.png (UOttawa icon used in the main menu)
    │
    └───Movie-Trailers
    │   |   Block_1
    |   |   Block_2
    │   |   Block_3
    |   |   Block_4
    │   |   Block_5
    |
    └───Output-Logs
        |   Results.csv (Contains the result(s) from the experiment(s))
    ```
