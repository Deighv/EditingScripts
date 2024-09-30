import subprocess
import itertools
import datetime
import math
from os import walk, system, remove
import ffmpeg
#So I'm dumb and 'recorded' for 20 hours with all my audio channels turned on in OBS which is messing up the other script as its not expecting multiple audio channels
#and my other audio channels somehow don't have audio for the first few seconds lmao
#supposedly -map -0:a shouldn't match the previously defined -0:a:1 but lol documentation 
#(or as implicated above and in other scripts, I am regarded)
#Adding this to the repo in case anyone else makes the same mistake, or I do twice.. which is more likely
#if you have multiple audio channels and you do need them, you can tweak the below to compress them into one (see ffmpeg map docs)

folderWithRecordings = "C:\\Temp\\" #Folder with your clips and this script
filenamesToStart = next(walk(folderWithRecordings), (None, None, []))[2]  
filenamesToStart = [fi for fi in filenamesToStart if fi.endswith(".mkv")] #just our videos (it runs through them alphabetically)
filenamesToStart = [fi for fi in filenamesToStart if not fi.startswith("output")] #Ignore the outputs in our folder
runInBatchesOf = int(len(filenamesToStart)) 
#runInBatchesOf = int(1) #do one
NumberOfClips =  len(filenamesToStart) #do em all
NumberOfRuns = math.floor(NumberOfClips/runInBatchesOf)

print(NumberOfRuns)
index = 0
while index <= NumberOfRuns-1: #This can overflow and I know
    
    fromThis = int((runInBatchesOf*index)) #The number file in the group we want to start at
    toThis = int(fromThis+runInBatchesOf) #The number file in the group we want to end at
    ourFiles = []
    for x in range(fromThis, toThis):
        file = folderWithRecordings+filenamesToStart[x]
        internal_videoLength = ffmpeg.probe(file)["format"]["duration"]
        internal_videoLength = float(internal_videoLength)
        newVideoLength = internal_videoLength
        newName = "trimmed_and_clean_" + filenamesToStart[x]
        system("ffmpeg -i " + filenamesToStart[x] +" -ss 00:00:0 -t "+ str(newVideoLength) + " -map 0:v:0 -map 0:a:1 -map -0:a:2 -map -0:a:3 -map -0:a:4 -map -0:a:5 -map -0:a:6 -y "+ newName)
        #remove(filenamesToStart[x]) #live dangerously, be efficient
    exit()