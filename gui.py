# # Importing tkinter module
# import tkinter as tk
# import datetime
# now=datetime.datetime.now()
# now.isoformat()
# # current date and time


# # creating Tk window
# root = tk.Tk()
# root.geometry("500x500")
# root.title("My First GUI")

# root.configure(bg='blue')
# label = tk.Button(root, text=now)
# label.pack()

# root.mainloop() 

import tkinter as tk
import datetime
import math

# Create the main window
root = tk.Tk()
root.title("Clock")

# Create the canvas to draw the clock on
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Draw the clock face
canvas.create_oval(50, 50, 350, 350, width=4)

# Draw the numbers on the clock face
for i in range(1, 13):
    angle = i * 30 * 3.14159 / 180
    x = 200 + 140 * math.sin(angle)
    y = 200 - 140 * math.cos(angle)
    canvas.create_text(x, y, text=str(i), font=("Helvetica", 20))

# Draw the clock hands
hour_hand = canvas.create_line(200, 200, 200, 100, width=8, fill="red")
minute_hand = canvas.create_line(200, 200, 200, 50, width=4)
second_hand = canvas.create_line(200, 200, 200, 50, width=2, fill="red")

# Define the function to update the clock
def update_clock():
    now = datetime.datetime.now()
    hour = now.hour % 12
    minute = now.minute
    second = now.second
    hour_angle = (hour + minute / 60) * 30 * 3.14159 / 180
    minute_angle = minute * 6 * 3.14159 / 180
    second_angle = second * 6 * 3.14159 / 180
    canvas.coords(hour_hand, 200, 200, 200 + 80 * math.sin(hour_angle), 200 - 80 * math.cos(hour_angle))
    canvas.coords(minute_hand, 200, 200, 200 + 120 * math.sin(minute_angle), 200 - 120 * math.cos(minute_angle))
    canvas.coords(second_hand, 200, 200, 200 + 120 * math.sin(second_angle), 200 - 120 * math.cos(second_angle))
    root.after(1000, update_clock)

# Start the clock
update_clock()

# Run the main loop
root.mainloop()
