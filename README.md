# Movie-Trailer-Program

This project is intended to be used within the Cassidy Lab (The Royal’s Institute of Mental Health Research, affiliated with uOttawa) for experiments conducted to study users interpretations of Movie Trailers.

This Python program was created by Dustin Doucette, a 4th year undergraduate Computer Science student at Carleton University.

## Program Requirements

Python 3 ([download](https://www.python.org/downloads/))

    **Note:** For ease of use, ensure Python gets added to the PATH environment variable during installation

External Python Modules:

    -Pillow
    
    -OpenCV-Python
    
    -Pyglet

## Installation

1. Click `Clone or download` then `Download ZIP` on the main repository page.

2. Unzip the downloaded file into a directory which contains no spaces. 
    
    `C:\User\JohnDoe\Projects`    ~**GOOD**    
    
    `C:\User\John Doe\Projects`   ~**BAD**
    
2. Open a command prompt (cmd.exe) and enter the following commands to install the required Python modules:

    `pip install pillow`
    
    `pip install opencv-python`
    
    `pip install pyglet`

## Program Set-Up

Place pre-downloaded AVI Movie Trailers into the folder `./Movie-Trailers`.

## Program Use Instructions

1. Open a command prompt (cmd.exe) and traverse to the directory which contains the downloaded program (e.g. `C:\MovieTrailerProgram\`).

2. Execute the command `python .\Program.py`.

    **Note:** The first startup after placing new trailers in the movie trailer program will take longer to start the first GUI. This is because the program is taking individual frames out of the trailers for later use in the program.

3. Click `Start` in the main menu to begin the experiment.

4. Enter your user ID and press `Begin Testing`.

5. Select `Start Trailer` to begin viewing the next trailer.

6. After the movie trailer has finished, close the video aplication and press `Continue` on the program window.

7. Select all of the relevant boxes (if the movie trailer had funny, scary and/or sexy content), then press `Next`.

8. Adjust the sliders to reflect your ratings (scale of 1-10), then press `Next`.

9. Select all of the relevant movie trailer frames which encompass the specified content. You will be given a new window for each box you selected in step 6 (if no boxes were selected, skip to step 10). Press `Finished`.

10. Select all of the relevant movie trailer frames which encompass the important scenes. Press `Finished`.

11. If there are more movie trailers to be reviewed, the name of the next movie trailer will be displayed. Press `Start Trailer`. This will bring the user back to step 6.

12. If there are no more movie trailers to be reviewed, a thank you message is displayed, and you can now close the window (terminating the program).

## Program Considerations

The program needs to have at least one movie trailer placed inside the folder `Movie-Trailers` to function properly.

## Program Output

After step 10 (for each movie trailer) is completed, a new line is added to the excel output file named `Results.xlsx` located within the `Output-Logs` folder.

The `Results.xlsx` file will have the following columns (one new line added after every inidividual test):

| User ID | Movie Trailer | Funny | Funny Rating | Funny Sections | Scary | Scary Rating | Scary Sections | Sexy | Sexy Rating |  Sexy Sections  |  Important Sections  |
|---------|---------------|-------|--------------|----------------|-------|--------------|----------------|------|-------------|-----------------|----------------------|
|123456789|     1917      |  NO   |     N/A      |       N/A      |  YES  |     8/10     |    (14,19)     |  NO  |    N/A      |       N/A       |         N/A          |
|987654321| The Thinning  |  NO   |     N/A      |       N/A      |  YES  |     5/10     |    (34,38)     |  YES |    3/10     |(12,21), (26,35) |   (12,21), (26,35)   |
|187462945|   Peter Pan   |  YES  |     6/10     | (0,5), (23,30) |  NO   |     N/A      |      N/A       |  NO  |    N/A      |       N/A       |         N/A          |

|         User ID       | Displays the User ID of the participant                                                                                                                      |
|:---------------------:|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  **Movie Trailer**    | Displays the name of the movie trailer that the participant is reviewing                                                                                     |
|       **Funny**       | Displays whether or not the participant thinks the movie trailer contains funny content                                                                      |
|   **Funny Rating**    | Displays a number between 1-10, where the participant decides how funny the movie trailer content was                                                        |
|  **Funny Sections**   | Displays comma seperated tuples, where the first value is the start time (in seconds) and the second value is the end time (in seconds) of the funy content  |
|       **Scary**       | Displays whether or not the participant thinks the movie trailer contains Scary content                                                                      |
|   **Scary Rating**    | Displays a number between 1-10, where the participant decides how Scary the movie trailer content was                                                        |
|  **Scary Sections**   | Displays comma seperated tuples, where the first value is the start time (in seconds) and the second value is the end time (in seconds) of the Scary content |
|       **Sexy**        | Displays whether or not the participant thinks the movie trailer contains Sexy content                                                                       |
|    **Sexy Rating**    | Displays a number between 1-10, where the participant decides how Sexy the movie trailer content was                                                         |
|   **Sexy Sections**   | Displays comma seperated tuples, where the first value is the start time (in seconds) and the second value is the end time (in seconds) of the Sexy content  |
|**Important Sections** | Displays comma seperated tuples, where the first value is the start time (in seconds) and the second value is the end time (in seconds) of the Sexy content  |




## Project Files

By default, the project contains the following file and folder layout:

    ```
    Movie_Trailer_Program
    │   Program.py (Main Python Program)
    |   GenerateFrames.py (Generates individual frames for each movie trailer)
    |   README.md (This guide)
    │
    └───Images
    │   │   uottawa_ver_black.ico (UOttawa icon used as the favicon for each window)
    │   │   uottawa_ver_black.png (UOttawa icon used in the main menu)
    │
    └───Movie-Trailers
    │
    └───Output-Logs
        |   Results.xlsx (Contains the results from testing)
    ```


