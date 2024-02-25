import pyaudio
from tkinter import *
import queue
import wave
import threading
from tkinter import messagebox
from pydub import AudioSegment
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "trial.wav"

# Functions for recording and playing audio
def threading_rec(x):
    if x == 1:
        t1 = threading.Thread(target=record_audio)
        t1.start()
    elif x == 2:
        global recording
        recording = False
        messagebox.showinfo(message="Recording finished")
    elif x == 3:
        if file_exists:
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            data = wf.readframes(CHUNK_SIZE)
            while data:
                stream.write(data)
                data = wf.readframes(CHUNK_SIZE)
            stream.stop_stream()
            stream.close()
            p.terminate()
        else:
            messagebox.showerror(message="Record something to play")

def record_audio():
    global recording
    recording = True
    global file_exists
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

# Create the main window
voice_rec = Tk()
voice_rec.geometry("500x200")
voice_rec.title("Recorder")
q = queue.Queue()
recording = False
file_exists = False

title_lbl = Label(voice_rec, text="Start Recording Now")
title_lbl.grid(row=0, column=0, columnspan=3)

record_btn = Button(voice_rec, text="Record Audio", command=lambda m=1: threading_rec(m))
stop_btn = Button(voice_rec, text="Stop Recording", command=lambda m=2: threading_rec(m))
play_btn = Button(voice_rec, text="Play Recording", command=lambda m=3: threading_rec(m))

record_btn.grid(row=1, column=1)
stop_btn.grid(row=1, column=0)
play_btn.grid(row=1, column=2)

voice_rec.mainloop()

# Plotting the raw audio
root = tk.Tk()
audio = AudioSegment.from_file(WAVE_OUTPUT_FILENAME)
color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]

def plotRawAudio():
    raw_audio = np.array(audio.get_array_of_samples())
    pd.Series(raw_audio).plot(figsize=(10,5), lw=1, title="Raw Audio", color=color_pal[0])
    plt.show()

plot_button = tk.Button(root, text="Plot Raw Audio", command=plotRawAudio)
plot_button.pack(pady=10)

root.mainloop()