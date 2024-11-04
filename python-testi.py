import tkinter as tk

# Timer intervals in seconds
BASELINE_TIME = 10  # Initial wait time 
SQUEEZE_TIME = 5  #  Squeeze duration 
REST_INCREMENT = 2  # Increment of rest time between cycles 
EXTENDED_REST_PERIOD = 30  # Extended rest period after three reps 
MAX_WAIT_TIME = 21  # Maximum wait time between cycles
SQUEEZE_REPS = 3  # Number of squeeze repetitions per set

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer")
        self.root.geometry("400x300")

        # Add introduction text
        self.header = tk.Label(root, text="Start measurement when ready", font=("Arial", 26))
        self.header.pack(pady=20)

        # Initialize timer label
        self.timer_label = tk.Label(root, text="", font=("Arial", 24))
        self.timer_label.pack()

        # Add button to start measurement
        self.start_button = tk.Button(root, text="Start Measurement", font=("Arial", 24), command=self.start_timer)
        self.start_button.pack(pady=20)

        # Initialize state variables
        self.current_rest_time = 1
        self.current_rep = 0


    def start_timer(self):
        self.start_button.pack_forget()  
        self.start_countdown(BASELINE_TIME, self.baseline_phase)

    def start_countdown(self, seconds, callback):
        def countdown():
            if seconds > 0:
                self.timer_label.config(text=f"{seconds}s")
                self.root.after(1000, lambda: self.start_countdown(seconds - 1, callback))
            else:
                self.timer_label.config(text="")
                callback()

        countdown()

    def baseline_phase(self):
        self.root.configure(bg="#e5e043")
        self.header.config(text="Valmistaudu")
        self.start_countdown(BASELINE_TIME, self.measurement_process)

    def measurement_process(self):
        self.current_rep = 0
        self.start_squeeze_cycle()

    def start_squeeze_cycle(self):
        if self.current_rep < SQUEEZE_REPS:
            # Perform squeeze phase
            self.root.configure(bg="#57cc52")
            self.header.config(text=f"Puristus {self.current_rep + 1}")
            self.start_countdown(SQUEEZE_TIME, self.short_rest_or_extended)

    def short_rest_or_extended(self):
        if self.current_rep < SQUEEZE_REPS - 1:
            # Apply short rest if it's not the last squeeze rep
            self.root.configure(bg="#ed5f40")
            self.header.config(text="Lepo")
            self.start_countdown(self.current_rest_time, self.increment_rep)
        else:
            # Apply extended rest after the last rep
            self.start_extended_rest()

    def increment_rep(self):
        self.current_rep += 1
        self.start_squeeze_cycle()

    def start_extended_rest(self):
        self.root.configure(bg="#ed5f40")
        self.header.config(text="Pitkä lepo")
        self.start_countdown(EXTENDED_REST_PERIOD, self.check_cycle_end)

    def check_cycle_end(self):
        if self.current_rest_time < MAX_WAIT_TIME:
            self.current_rest_time += REST_INCREMENT
            self.measurement_process()
        else:
            self.root.quit()

# Run the application
root = tk.Tk()
app = TimerApp(root)
root.mainloop()
