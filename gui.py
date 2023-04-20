
import tkinter as tk
import time
import main


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

class LoadingSpinner(tk.Canvas):
    def __init__(self, master=None, size=50, **kwargs):
        super().__init__(master, width=size, height=size, **kwargs)
        self.config(highlightthickness=0)
        self._arc = self.create_arc(
            (5, 5, size-5, size-5),
            start=0, extent=60,
            width=3, style=tk.ARC,
            outline="#007bff"
        )
        self._job = None
        self._speed = 20
    
    def start(self):
        if self._job is None:
            self._job = self.after(self._speed, self._animate)
    
    def stop(self):
        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None
            self.itemconfigure(self._arc, extent=60)
    
    def _animate(self):
        extent = int(float(self.itemcget(self._arc, "extent")) + 10) % 360
        self.itemconfigure(self._arc, extent=extent)
        self._job = self.after(self._speed, self._animate)



class gui:
    def create(self):
        # Create the main window
        root = tk.Tk()

        if(main.training):
            spinner = LoadingSpinner(root)
            spinner.pack(padx=20, pady=20)
        else:
        # Create the digital clock label
            digital_clock = DigitalClock(root)

            # Add the digital clock label to the window
            digital_clock.pack()

        # Start the main event loop
        root.mainloop()


# Example usage of spinner

# root = tk.Tk()
# spinner = LoadingSpinner(root)
# spinner.pack(padx=20, pady=20)
# spinner.start()
# root.mainloop()