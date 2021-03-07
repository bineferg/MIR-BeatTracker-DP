from beat_tracker import *

file_list="./BallroomData/allBallroomFiles"

def go():
    f = open(file_list, 'r')
    lines = f.readlines()
    for line in lines:
        fline=line.strip("./").strip("\n")
        beats = beatTracker("./BallroomData/"+fline) 
        outf=fline.replace(".wav", ".estimate")
        f = open("./output/"+outf,"w+")
        for beat in beats:
            f.write(str(beat)+"\n")
        f.close()

go()
