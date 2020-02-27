from midiutil.MidiFile import MIDIFile
import matplotlib.pyplot as plt
import math
import numpy as np

#https://stackoverflow.com/questions/11059801/how-can-i-write-a-midi-file-with-python
def extract_data(name):
	#extracts data from a textfile specified in function input and returns a list
	file = open(name, "r")
	lines = file.readlines()
	line_data = []
	for line in lines:
		temp = line.replace("\n", "")
		line_data.append(float(temp))
	file.close()
	return line_data

def scale_pitch_human(data):
	#scales input list
	temp1 = data
	temp2 = data

	min_temp = min(data)
	max_temp = max(data)

	for j in range(0, len(data)):
		temp2[j] = -10 + math.ceil(data[j]/(max_temp - min_temp)*80) # scales data onto midi range and rounds to the nearest integer above the number

	return temp2

def scale_pitch_elnino(data):
	#scales input list
	a = -min(data) #find the most negative number
	temp1 = data
	temp2 = data
	print(a)

	for i in range(0, len(data)):
		temp1[i] = data[i] + a #add offset to the data to get rid of negative numbers

	min_temp = min(temp1)
	max_temp = max(temp1)

	for j in range(0, len(data)):
		temp2[j] = math.ceil(temp1[j]/(max_temp - min_temp)*127) # scales data onto midi range and rounds to the nearest integer above the number

	return temp2

def scale_time(data):
	a = -min(data)
	temp1 = data
	temp2 = data

	for i in range(0, len(data)):
		temp1[i] = data[i] + a

	min_temp = min(temp1)
	max_temp = max(temp1)

	for j in range(0, len(data)):
		temp2[j] = temp1[j]/100

	return temp2



humanpop = extract_data("humanpopgrowth.txt")
elnino =  extract_data("elnino.txt")
plt.figure(1)
plt.plot(elnino)
plt.show()


pitch_human = scale_pitch_human(humanpop) #calls the scaling function to create a list of scaled pitches
pitch_elnino = scale_pitch_elnino(elnino)
#time1 = scale_time(data6) #calls the scaling time function to create a list of scaled times


# create your MIDI object
mf = MIDIFile(2)     # only 1 track
track1 = 0   # the only track
track2 = 1
time1 = 0    # start at the beginning
time2 = 0

mf.addTrackName(track1, time1, "Human Population Growth")
mf.addTempo(track1, time1, 150)
mf.addTrackName(track2, time2, "El Nino")
mf.addTempo(track2, time2, 150)



#set other midi parameters here.
duration1 = 4
duration2 = 0.333
volume1 = 100
volume2 = 70
channel = 0

program1 = 42
program2 = 1
mf.addProgramChange(track1, channel, time1, program1)
mf.addProgramChange(track2, channel, time2, program2)

for j in range(0, len(pitch_human)):
	pitch1 = pitch_human[j]
	mf.addNote(track1, channel, pitch1, time1, duration1, volume1) #adds information for each note
	time1 = time1 + 4

for j in range(0, len(pitch_elnino)):
	pitch2 = pitch_elnino[j]
	mf.addNote(track2, channel, pitch2, time2, duration2, volume2) #adds information for each note
	time2 = time2 + 0.333

# write it to disk
with open("test_humanpop_elnino.mid", 'wb') as outf: #remember to change the name of this midi file every time you create a new one!
    mf.writeFile(outf)

