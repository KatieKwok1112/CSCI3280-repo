import pyaudio
from tkinter import *
import queue
import wave
import threading
from tkinter import messagebox
from pydub import AudioSegment
import tkinter as tk
import time
import matplotlib as plt
import numpy as np
import pandas as pd

CHUNK_SIZE = 1024 #1024 audio frames will be read or processed at a time
FORMAT = pyaudio.paInt16 #correspond to 16-bit signed integer PCM encoding
CHANNELS = 1 #1 audio channels
SAMPLE_RATE = 44100 #number of samples per second in the audio stream
RECORD_SECONDS = 5 #duration of recording
WAVE_OUTPUT_FILENAME = "trial.wav"

# Functions to play, stop, and record audio in Python voice recorder
# The recording is done as a thread to prevent it from being the main process
def threading_rec(x): #record
    if x == 1:
        # If recording is selected, then the thread is activated
        t1 = threading.Thread(target=record_audio)
        t1.start()
    elif x == 2: #stop
        # To stop, set the flag to false
        global recording
        recording = False
        messagebox.showinfo(message="Recording finished")
    elif x >= 3:
        # To play a recording, it must exist
        if file_exists:
            speed = 1
            if x == 4:
                speed = 2
            elif x == 5:
                speed = 0.5
            # Read the recording if it exists and play it
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
            p = pyaudio.PyAudio() #initialize PyAudio Library
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=int (wf.getframerate()/speed),
                            output=True)
            data = wf.readframes(CHUNK_SIZE)
            while data:
                stream.write(data)
                data = wf.readframes(CHUNK_SIZE)
            stream.stop_stream()
            stream.close()
            p.terminate()
        else:
            # Display an error if none is found
            messagebox.showerror(message="Record something to play")

# Recording function
def record_audio():
    # Declare global variables
    global recording
    # Set to True to record
    recording = True
    global file_exists
    # Create a file to save the audio
    messagebox.showinfo(message="Recording Audio. Speak into the mic")
    frames = []
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE)
    while recording:
        data = stream.read(CHUNK_SIZE)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    file_exists = True

# Define the user interface for Voice Recorder using Python
voice_rec = Tk()
voice_rec.geometry("500x200")
voice_rec.title("Recorder")
# Create a queue to contain the audio data
q = queue.Queue()
# Declare variables and initialize them
recording = False
file_exists = False

# Label to display app title in Python Voice Recorder Project
title_lbl = Label(voice_rec, text="Start Recording Now")
title_lbl.grid(row=0, column=0, columnspan=3)

# Button to record audio
record_btn = Button(voice_rec, text="Record Audio", command=lambda m=1: threading_rec(m))
# Stop button
stop_btn = Button(voice_rec, text="Stop Recording", command=lambda m=2: threading_rec(m))
# Play button
play_btn = Button(voice_rec, text="Play Recording", command=lambda m=3: threading_rec(m))
# Natalie part
# x0.5 speed button
halfSpeed_btn = tk.Button(voice_rec, text="Speed x0.5", command=lambda m=4: threading_rec(m))
# x2 speed button
doubleSpeed_btn = tk.Button(voice_rec, text="Speed x2", command=lambda m=5: threading_rec(m))
# Position buttons
record_btn.grid(row=1, column=1)
stop_btn.grid(row=1, column=0)
play_btn.grid(row=1, column=2)
halfSpeed_btn.grid(row=2, column=0)
doubleSpeed_btn.grid(row=2, column=1)
voice_rec.mainloop()

#Katie part
root = tk.Tk()
audio = AudioSegment.from_file(WAVE_OUTPUT_FILENAME)
color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]
def plotRawAudio():
    raw_audio = np.array(audio.get_array_of_samples())
    pd.Series(raw_audio).plot(figsize=(10,5), lw=1, title="Raw Audio",
    color = color_pal[0])
    plt.show()

plot_button = tk.Button(root, text="Plot Raw Audio", command = plotRawAudio)
plot_button.pack(pady= 10)

root.mainloop()

'''
audio_length = len(audio) / 1000 #convert to milisecond
seekbar_scale = Scale(root ,from_= 0, to= audio_length,resolution=0.1, orient = HORIZONTAL)
# Function to update the seekbar position based on the current playback position
def update_seekbar_position():
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
    total_duration = wf.getnframes() / wf.getframerate()
    current_position = 0.0
    while current_position < total_duration:
        seekbar_scale.set(current_position)
        current_position += 0,1
        if current_position <= audio_length:
            root.after(100, update_seekbar_position, current_position)

root.mainloop
'''
