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


def scale_pitch(data):
	#scales input list
	a = min(data)
	temp1 = data
	temp2 = data

	for i in range(0, len(data)):
		temp1[i] = data[i] - a #add offset to the data to get rid of negative numbers

	min_temp = min(temp1)
	max_temp = max(temp1)

	for j in range(0, len(data)):
		temp2[j] = math.ceil(temp1[j]/(max_temp - min_temp)*80) + 20 # scales data onto midi range and rounds to the nearest integer above the number
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
		#I tried three different scaling methods. Listen to the result of each! Remember to change the 
		#name of the output file on the second last line of code
		#temp2[j] = (temp1[j]/(max_temp - min_temp)*2)/100 #THIS WORKS USE THIS IN WORST CASE
		temp2[j] = temp1[j]/100
		#temp2[j] = math.ceil(temp1[j]/(max_temp - min_temp)*2)
		#temp2[j] = round(temp1[j]/(max_temp - min_temp)*2, 1) + 0.5
	return temp2
def moving_average(data, n):
#moving average used from https://stackoverflow.com/questions/14313510/how-to-calculate-moving-average-using-numpy/54628145
    ret = np.cumsum(data, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def sampling(data, n):
	sampled = []
	for i in range(0,len(data)):
		if i % n == 0:
			sampled.append(data[i])
	return sampled

data1 = extract_data("annually_GCAG.txt")
data2 = extract_data("annually_GCAG.txt")

plt.figure(1)
plt.plot(data1)
plt.show()

pitch1 = scale_pitch(data1) #calls the scaling function to create a list of scaled pitches for sealevel change
time1 = scale_time(data2) #calls the scaling time function to create a list of scaled times for sealevel change


plt.figure(2)
plt.plot(pitch1)
plt.show()


# create your MIDI object
mf = MIDIFile(1)     # only 1 track
track = 0   # the only track

time = 0    # start at the beginning
mf.addTrackName(track, time, "Global Temperature Anomalies")
mf.addTempo(track, time, 5)

#set other midi parameters here. Try experimenting with these!
time = 0
duration = 0.2
volume = 100
channel = 0

pitch1.reverse()
time1.reverse()
for j in range(0, len(pitch1)):
	pitch = pitch1[j]
	mf.addNote(track, channel, pitch, time, duration, volume) #adds information for each note
	time = time + time1[j] #increments the time to add the note based on the scaled time list
	duration = 0.1 + time1[j] #increments the duration of the note based on the scaled time list

# write it to disk
with open("globaltempanomaly_GCAG.mid", 'wb') as outf: #remember to change the name of this midi file every time you create a new one!
    mf.writeFile(outf)
