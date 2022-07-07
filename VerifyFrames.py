import glob
import os
import subprocess

failCount = 0

# Get the length (in seconds) of a passed in movie trailer
def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

# Go through each trailer and make sure that the number of generated frames is correct
# This script will remove the manual step of making sure that frames were generated
# correctly for each trailer
for blockNumber in range(1, 6):
    print("\n")
    print(
        "Verifying Frames for Block " + str(blockNumber) + " Trailers, Please Wait"
    )
    print("--------------------------------------------------\n")
    tempList = glob.glob("./Movie-Trailers/Block_" + str(blockNumber) + "/*.avi")
    movies = []

    for x in tempList:
        x = x.replace("./Movie-Trailers/Block_" + str(blockNumber) + "/", "")
        x = x.replace(".avi", "")
        movies.append(x)

    for x in movies:
        print("Trailer Name: " + x)
        trailerLength = get_length("./Movie-Trailers/Block_" + str(blockNumber) + "/" + x + ".avi")
        imageCount = glob.glob("./Movie-Trailers/" + "Block_" + str(blockNumber) + "/" + x + "/image*")

        passFlag = ''

        if (-2 <= len(imageCount) - round(trailerLength*2, 0) <= 2):
            passFlag = "[PASS]"
        else:
            passFlag = "***[FAIL]***"
            failCount += 1

        print("Trailer Length: " + str(trailerLength))
        print("Image Count: " + str(len(imageCount)))
        print("Estimated Image Count: " + str(round(trailerLength*2, 0)) + " " + passFlag + "\n")

if (failCount > 0):
    if (failCount == 1):
        print("\nFrame Verification Completed, 1 error was detected, please check output above to view the error\n\n")
    else:
        print("\nFrame Verification Completed, " + str(failCount) + " errors were detected, please check output above to view the errors\n\n")
else:
    print("\nFrame Verification Completed, All Images Were Generated Correctly\n\n")
