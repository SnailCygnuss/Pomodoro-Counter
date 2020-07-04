import tkinter
import tkinter.ttk
from resumabletimer import ResumableTimer
from threading import Event, Thread
import configparser
from common import screen_notification, icon_path


class PomodoroApplication(tkinter.ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # Configure the root frame
        self.master.configure(bg="#121212")
        self.master.iconbitmap(icon_path())
        # Define the style for the GUI
        self.style = tkinter.ttk.Style()
        self.set_style()
        self.pack(padx=5, pady=5)
        master.protocol("WM_DELETE_WINDOW", self.on_exit)
        test = False
        if test:
            settings_file = 'test-settings.txt'
        else:
            settings_file = 'settings.txt'
        config_settings = readconfig(settings_file)

        def default_config():
            # TODO: Create a new config file with default values
            self.length["Pomodoro"] = 5
            self.length["Short Break"] = 5
            self.length["Long Break"] = 5
            self.length["Num of Pomos"] = 2

        # Length of timer in seconds
        self.length = {}
        try:
            self.length["Pomodoro"] = int(config_settings['pomodoro interval'])
            self.length["Short Break"] = int(config_settings['short break'])
            self.length["Long Break"] = int(config_settings['long break'])
            self.length["Num of Pomos"] = int(config_settings['number of pomodoro'])
        except ValueError:
            default_config()

        # Variables for storing number of pomodoros and time completed
        self.nums_completed = {"Pomodoro": 0,
                               "Short Break": 0,
                               "Long Break": 0}
        self.mins_completed = {"Pomodoro": 0,
                               "Short Break": 0,
                               "Long Break": 0}
        self.current_activity = "Pomodoro"

        # Variables for running the program
        self.timer_obj = None
        self.cancel_timer_refresh = None

        # Function to build all widgets
        self.buildwindow()

    def buildwindow(self):
        self.master.title("Pomodoro Timer")

        # Function to run after timer finishes
        def timer_finish():
            # Reset timer obj
            self.timer_obj = ResumableTimer(0, timer_finish)
            # Stop thread to update timer
            if self.cancel_timer_refresh is not None:
                self.cancel_timer_refresh()
            print("Time up")
            # Display notification
            screen_notification(self.current_activity)
            # Enable start button and disable pause button
            toggle_run_buttons()

            # Find next activity
            self.nums_completed[self.current_activity] = self.nums_completed[self.current_activity] + 1
            self.mins_completed[self.current_activity] = self.mins_completed[self.current_activity] + \
                self.length[self.current_activity]
            if self.current_activity == "Pomodoro":
                if self.nums_completed["Pomodoro"] % self.length["Num of Pomos"] == 0:
                    self.current_activity = "Long Break"
                else:
                    self.current_activity = "Short Break"
            elif (self.current_activity == "Short Break" or
                  self.current_activity == "Long Break"):
                self.current_activity = "Pomodoro"
            # Update labels
            label_timer_update()

        # Timer object with zero minutes left. Only for initial display and during startup
        self.timer_obj = ResumableTimer(0, timer_finish)
        self.cancel_timer_refresh = None

        # TODO: Make timer and status in different frames
        config_frame = tkinter.ttk.Frame(self)
        config_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

        status_frame = tkinter.ttk.Frame(self)
        status_frame.grid(row=0, column=0, pady=10, padx=10)

        button_frame = tkinter.ttk.Frame(self)
        button_frame.grid(row=0, column=1, pady=10, padx=10)

        def finish_time():
            if self.timer_obj.status == "Running":
                end_time = str(self.timer_obj.target).split()[1].split(".")[0].split(":")
                end_time = end_time[0] + ":" + end_time[1]
                return f'{self.timer_obj.status} - Ends at {end_time}'
            elif (self.timer_obj.status == "Not Started") or (self.timer_obj.status is None):
                return self.timer_obj.status
        # Display the Timer
        label_timer = tkinter.ttk.Label(status_frame, text=self.timer_obj.time_remaining(), style="Timer.TLabel")
        label_timer.pack()

        # Display the Status
        label_status = tkinter.ttk.Label(status_frame, text=finish_time())
        label_status.pack(side=tkinter.TOP)

        # Display Timer end time
        # TODO: Create label to display timer end

        # TODO: Display the Pomodoro and Break counter

        # Display current activity
        def get_activity_text():
            if self.timer_obj.status == "Not Started":
                activity_text = f'Up Next: {self.current_activity}'
            elif self.timer_obj.status == "Paused" or self.timer_obj.status == "Running":
                activity_text = f'On going: {self.current_activity}'
            return activity_text

        label_activity = tkinter.ttk.Label(status_frame, text=get_activity_text())
        label_activity.pack(side=tkinter.TOP)

        # Timer starting function of any length
        def start_timer(timer_length):
            # Stop existing timer
            if self.timer_obj.status == "Running":
                self.timer_obj.pause()
                if self.cancel_timer_refresh is not None:
                    self.cancel_timer_refresh()
            self.timer_obj = ResumableTimer(timer_length, timer_finish)
            self.timer_obj.start()
            # Update timer and status label
            label_timer_update()
            # Disable start button and enable pause button
            toggle_run_buttons()
            # Start thread to update timer every 1 second
            self.cancel_timer_refresh = timer_refresh()

        def toggle_run_buttons():
            if self.timer_obj.status == "Running":
                button_pause['state'] = tkinter.NORMAL
            elif self.timer_obj.status == "Not Started" or self.timer_obj.status == "Paused":
                button_pause['state'] = tkinter.DISABLED

        # TODO: Make option of auto start between pomodoros and breaks
        # Start activity button
        def start_activity():
            start_timer(self.length[self.current_activity])

        # button_start = tkinter.ttk.Button(self, text="Start Next Activity", command=start_activity)
        # button_start.pack(padx=5, pady=0)

        # Start pomodoro button
        def start_pomo():
            self.current_activity = "Pomodoro"
            start_timer(self.length["Pomodoro"])

        button_start_pomo = tkinter.ttk.Button(button_frame, text="Start Pomodoro", command=start_pomo)
        button_start_pomo.pack(fill=tkinter.X, padx=5, pady=0)

        # Start short break button
        def start_sbreak():
            self.current_activity = "Short Break"
            start_timer(self.length["Short Break"])

        button_start_sbreak = tkinter.ttk.Button(button_frame, text="Start Short Break", command=start_sbreak)
        button_start_sbreak.pack(fill=tkinter.X, padx=5, pady=0)

        # Start long break button
        def start_lbreak():
            self.current_activity = "Long Break"
            start_timer(self.length["Long Break"])

        button_start_lbreak = tkinter.ttk.Button(button_frame, text="Start Long Break", command=start_lbreak)
        button_start_lbreak.pack(fill=tkinter.X, padx=5, pady=0)

        # Pause / Resume Button
        def pause_timer():
            if self.timer_obj.status is "Running":
                self.timer_obj.pause()
                # Stop thread to update timer
                if self.cancel_timer_refresh is not None:
                    label_timer_update()
                    self.cancel_timer_refresh()
                # Change pause button label to "resume"
                button_pause['text'] = "Resume"
            elif self.timer_obj.status is "Paused":
                self.timer_obj.start()
                # Update timer and status label
                label_timer_update()
                # Change pause button label to "pause"
                button_pause['text'] = "Pause"
                # Start thread to update timer every 1 second
                self.cancel_timer_refresh = timer_refresh()

        button_pause = tkinter.ttk.Button(button_frame, text="Pause", command=pause_timer, state=tkinter.DISABLED)
        button_pause.pack(fill=tkinter.X, padx=5, pady=0)

        # Statistics Button
        # TODO: Add statistics window
        def display_stats():
            pass

        button_stats = tkinter.ttk.Button(config_frame, text="Statistics", command=display_stats)
        button_stats.grid(column=0, row=0, padx=5)

        # Settings Button
        # TODO: Add settings window
        def display_settings():
            pass
        button_settings = tkinter.ttk.Button(config_frame, text="Settings", command=display_settings)
        button_settings.grid(column=1, row=0, padx=5)

        # Help Button
        # TODO: Add help window
        def help_menu():
            pass
        button_help = tkinter.ttk.Button(config_frame, text="Help", command=help_menu)
        button_help.grid(column=2, row=0, padx=5)

        button_exit = tkinter.ttk.Button(config_frame, text="Exit", command=self.on_exit)
        button_exit.grid(column=3, row=0, padx=5)

        # TODO: Add keyboard shoertcuts

        # Function to update timer label
        def label_timer_update():
            label_timer.configure(text=self.timer_obj.time_remaining())
            label_status.configure(text=finish_time())
            label_activity['text'] = get_activity_text()

        # Function to call timer label update every second
        def timer_refresh(interval=1, func=label_timer_update):
            stopped = Event()

            def loop():
                while not stopped.wait(interval):
                    func()
            Thread(target=loop).start()
            return stopped.set

    def on_exit(self):
        # Function to execute on closing the program
        if self.cancel_timer_refresh is not None:
            self.cancel_timer_refresh()
        if self.timer_obj.status is "Running":
            self.timer_obj.pause()
        self.master.destroy()

    def set_style(self, theme_option=None):
        # TODO: Fix button colours
        self.style.configure("TButton",
                             foreground="black",
                             background="#90CAF9")
        self.style.map("TButton", foreground=[],
                       background=[("disabled","#2196F3")])
        self.style.configure("TLabel", background="#121212", foreground="#FFFFFF",
                             font="Verdana 10", anchor=tkinter.CENTER)
        self.style.configure("Timer.TLabel", justify=tkinter.CENTER, font="Verdana 40")
        self.style.configure("TFrame", background="#121212")


def readconfig(file):
    # TODO: Create config file if not available
    config = configparser.ConfigParser()
    config.read(file)
    config_dict = dict(config.items("Pomodoro Settings"))
    return config_dict


def main():
    root = tkinter.Tk()
    # root.geometry("400x400+500+500")
    screen = PomodoroApplication(root)

    screen.mainloop()
    print("Program Closed")


if __name__ == "__main__":
    main()
