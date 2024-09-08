import subprocess
import itertools
import datetime
import math
from os import walk, system, remove
import ffmpeg

folderWithRecordings = "C:\\CleanupClips\\" #Folder with your clips and this script
filenamesToStart = next(walk(folderWithRecordings), (None, None, []))[2]  
filenamesToStart = [fi for fi in filenamesToStart if fi.endswith(".mkv")] #just our videos (it runs through them alphabetically)
filenamesToStart = [fi for fi in filenamesToStart if not fi.startswith("output")] #Ignore the outputs in our folder
runInBatchesOf = int(len(filenamesToStart)) 
NumberOfClips =  len(filenamesToStart) #do em all
NumberOfRuns = math.floor(NumberOfClips/runInBatchesOf)

print(NumberOfRuns)
index = 0
while index <= NumberOfRuns-1: 
    
    fromThis = int((runInBatchesOf*index)) #The number file in the group we want to start at
    toThis = int(fromThis+runInBatchesOf) #The number file in the group we want to end at
    ourFiles = []
    for x in range(fromThis, toThis):
        newName = "trimmed_and_clean_" + filenamesToStart[x]
        system("ffmpeg -i " + filenamesToStart[x] +" -ss 00:00:1 -t 00:00:18 -map 0:v:0 -map 0:a:1 -map -0:a:2 -map -0:a:3 -map -0:a:4 -map -0:a:5 -map -0:a:6 -y "+ newName)
        #remove(filenamesToStart[x]) #live dangerously, be efficient
    exit()