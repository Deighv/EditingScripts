import subprocess
import itertools
import datetime
import math
from os import walk
import ffmpeg
#This assumes all your clips are the same fps, resolution, etc 
folderWithRecordings = "C:\\VideosGoHere\\" #Folder with your clips and this script
filenamesToStart = next(walk(folderWithRecordings), (None, None, []))[2]  
filenamesToStart = [fi for fi in filenamesToStart if fi.endswith(".mkv")] #just the videos, change for filetype (it runs through them alphabetically)
filenamesToStart = [fi for fi in filenamesToStart if not fi.startswith("output")] #Ignore the outputs in our folder
#I did this in multiple runs so it'd be faster and I kept compiling the larger clips down 
runInBatchesOf = int(21) #many Filters+Clips uses many RAMs, adjust this until you're using just under your max ram
NumberOfClips =  len(filenamesToStart)
NumberOfRuns = math.floor(NumberOfClips/runInBatchesOf) #If you are doing batches you'll be happy if this is a round number, otherwise you'll have to up your index and override your toThis number

print(NumberOfRuns)
index = 0
while index <= NumberOfRuns -1: 

    fnDT = datetime.datetime.now().strftime("%H-%M-%S")
    fromThis = int((runInBatchesOf*index)) #The number file in the group we want to start at
    toThis = int(fromThis+runInBatchesOf) #The number file in the group we want to end at
    #output_filename = "output-StaticName.mkv"
    output_filename = "output-run_number_"+str(index)+"_at_"+ fnDT +"_from_File_"+str(filenamesToStart[fromThis])+"_to_File_"+str(filenamesToStart[toThis-1])+".mkv" #name our output file so there's no confusion what's in it
    ourFiles = []
    for x in range(fromThis, toThis):
        print(filenamesToStart[x])
        ourFiles += [filenamesToStart[x]] 
    #so we know what files went into what render    
    with open('renderFinal.log', 'a') as f:
        print(output_filename, file=f)
        print(ourFiles, file=f)
        print(datetime.datetime.now(), file=f)
        print("----------------------------------------------------", file=f)
    segments = ourFiles
    print(ourFiles)
    
    # Get the lengths of the videos in seconds
    file_lengths = []
    for x in range(fromThis, toThis):  #good old slow, easy to debug for loops
        file = folderWithRecordings+filenamesToStart[x]
        internal_videoLength = ffmpeg.probe(file)["format"]["duration"]
        internal_videoLength = float(internal_videoLength)
        file_lengths += [internal_videoLength]
    

    #thanks https://gist.github.com/royshil/369e175960718b5a03e40f279b131788
    #There are minor bugs in the OP
    #but thanks to everyone's hard work combined, here we are!
    
    # Prepare the filter graph
    video_fades = ""
    audio_fades = ""
    last_fade_output = "0:v"
    last_audio_output = "0:a"
    video_length = 0
    fade_duration = 1.0
    
    for i in range(len(segments) -1):

        video_length += file_lengths[i]
        video_length = video_length - fade_duration #subract our fade distance each round and keep track of that
        
        next_fade_output = "v%d%d" % (i, i + 1)
        next_audio_output = "a%d%d" % (i, i + 1)

        #Don't generate a graph for the final clip, let ffmpeg handle our mapping because it's better at it than me
        if(i == len(segments)-2):
            video_fades += "[%s][%d:v]xfade=duration=1.0:offset=%.3f; " % \
                (last_fade_output, i + 1, video_length)
            audio_fades += "[%s][%d:a]acrossfade=d=1.0" % \
                (last_audio_output, i + 1)
        else:  
            video_fades += "[%s][%d:v]xfade=duration=0.5:offset=%.3f[%s]; " % \
                (last_fade_output, i + 1, video_length , next_fade_output)
            audio_fades += "[%s][%d:a]acrossfade=d=0.5[%s]%s " % \
                (last_audio_output, i + 1, next_audio_output, ";" if (i+1) < len(segments)-1 else "")
        #having the acrossfade set to a full 1 seems to cause me nothing but heartburn, even with squeeky clean clips that have a/v streams trimmed to the exact same length

        last_fade_output = next_fade_output
        last_audio_output = next_audio_output
    files_input = [['-i', f] for f in segments]
    # ffmpeg, assemble!
    ffmpeg_args = ['ffmpeg', #Linux peeps ['/usr/local/bin/ffmpeg'
                *itertools.chain(*files_input),
                #'-vcodec', 'h264_nvenc ', #well that was a waste of time to set up, gpu encoders blow
                '-filter_complex', video_fades + audio_fades,
                '-y',
                output_filename]
    #Save our command to our log
    with open('render.log', 'a') as f:
        print(datetime.datetime.now(), file=f)
        print(" ".join(ffmpeg_args), file=f)
    print(" ".join(ffmpeg_args))
    #exit() #just check out the ffmpeg command
    subprocess.run(ffmpeg_args) 
    index +=1 #uncomment for running in batches or it won't loop
    exit() #comment this or it definitely won't loop