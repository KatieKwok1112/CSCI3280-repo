from tkinter import*

win = Tk()
win.title("Sound Recorder")

win.geometry("400x200") #width * Height
#win.minsize(width=400,height=200)
#win.maxsize(width=1024,height=768)
win.resizable(False,False)

#icon
#win.iconbitmap("") #.ico
win.config(bg="skyblue") #colour
win.attributes("-alpha", 1 ) #transparency 1-0 1-100% 0=0%
win.attributes("-topmost", True)

#image
img = PhotoImage(file="")

#button
btn = Button(text="Click me")
btn.config(bg="skyblue")
btn.config(width=10,height=5)
btn.pack()


win.mainloop()