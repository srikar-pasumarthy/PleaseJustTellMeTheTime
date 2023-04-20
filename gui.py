
import tkinter as tk
import time

class DigitalClock(tk.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        # Configure the label
        self.configure(font=('Courier', 150), background='black', foreground='green')
     
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
root.geometry("800x480")
# Create the digital clock label
digital_clock = DigitalClock(root)

# Add the digital clock label to the window
digital_clock.pack()

# Start the main event loop
root.mainloop()

