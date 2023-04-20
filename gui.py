# Importing tkinter module
import tkinter as tk
import datetime
now=datetime.datetime.now()
now.isoformat()
# current date and time


# creating Tk window
root = tk.Tk()
root.geometry("500x500")
root.title("My First GUI")

root.configure(bg='blue')
label = tk.Button(root, text=now)
label.pack()

root.mainloop() 
