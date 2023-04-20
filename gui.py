
import tkinter as tk
import time

class DigitalClock(tk.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Configure the label
        self.configure(font=('Courier', 40), background='black', foreground='green')

        # Update the time
        self.update_time()

    def update_time(self):
        # Get the current time
        current_time = time.strftime('%H:%M:%S')

        # Update the label text
        self.configure(text=current_time)

        # Schedule the next update in 1000 milliseconds (1 second)
        self.after(1000, self.update_time)

# Create the main window
root = tk.Tk()

# Create the digital clock label
digital_clock = DigitalClock(root)

# Add the digital clock label to the window
digital_clock.pack()

# Start the main event loop
root.mainloop()

In this example, we create a DigitalClock class that inherits from the Label class. The DigitalClock class is responsible for updating the text of the label with the current time.

We set the font of the label to 'Courier' with a size of 40, and set the background to black and foreground (text) to green.

The update_time method gets the current time using time.strftime with the format '%H:%M:%S' (hours, minutes, seconds). It then updates the label text with the current time and schedules the next update in 1000 milliseconds (1 second) using the .after() method.

We then create an instance of the DigitalClock class called digital_clock, add it to the window using .pack(), and start the main event loop.

When you run this code, you should see a digital clock display with the current time in hours, minutes, and seconds. The display will update every second to show the current time.

