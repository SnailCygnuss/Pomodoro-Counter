import tkinter
from resumabletimer import ResumableTimer
from threading import Event, Thread
import configparser


class PomodoroApplication(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        test = True
        if test:
            settings_file = 'test-settings.txt'
        else:
            settings_file = 'settings.txt'
        config_settings = readconfig(settings_file)
        # Length of timer in seconds
        self.length = {}
        try:
            self.length["Pomodoro"] = int(config_settings['pomodoro interval'])
            self.length["Short Break"] = int(config_settings['short break'])
            self.length["Long Break"] = int(config_settings['long break'])
            self.length["Num of Pomos"] = int(config_settings['number of pomodoro'])
        except:
            # TODO: Add condition for config file error
            self.length["Pomodoro"] = 5
            self.length["Short Break"] = 5
            self.length["Long Break"] = 5
            self.length["Num of Pomos"] = 2

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
            # Enable start button and disable pause button
            button_pause['state'] = tkinter.DISABLED
            button_start['state'] = tkinter.NORMAL

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

        self.timer_obj = ResumableTimer(0, timer_finish)
        self.cancel_timer_refresh = None

        # TODO: Make timer and status in different frames
        # Display the Timer
        label_timer = tkinter.Label(self, text=self.timer_obj.time_remaining())
        label_timer.pack()

        # Display the Status
        label_status = tkinter.Label(self, text=self.timer_obj.status)
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

        label_activity = tkinter.Label(self, text=get_activity_text())
        label_activity.pack(side=tkinter.TOP)

        # Timer starting function of any length
        def start_timer(timer_length):
            self.timer_obj = ResumableTimer(timer_length, timer_finish)
            self.timer_obj.start()
            # Update timer and status label
            label_timer_update()
            # Disable start button and enable pause button
            button_pause['state'] = tkinter.NORMAL
            button_start['state'] = tkinter.DISABLED
            # Start thread to update timer every 1 second
            self.cancel_timer_refresh = timer_refresh()

        # Start activity button
        def start_activity():
            start_timer(self.length[self.current_activity])

        button_start = tkinter.Button(self, text="Start Next Activity", command=start_activity)
        button_start.pack()

        # Start pomodoro button
        def start_pomo():
            self.current_activity = "Pomodoro"
            start_timer(self.length["Pomodoro"])

        button_start_pomo = tkinter.Button(self, text="Start Pomodoro", command=start_pomo)
        button_start_pomo.pack()

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

        button_pause = tkinter.Button(self, text="Pause", command=pause_timer, state=tkinter.DISABLED)
        button_pause.pack()

        # Reset Button
        def reset_timer():
            pass
        button_reset = tkinter.Button(self, text="Reset", command=reset_timer)
        button_reset.pack()

        def help_menu():
            pass
        button_help = tkinter.Button(self, text="Help", command=help_menu)
        button_help.pack()

        # Function to update timer label
        def label_timer_update():
            label_timer.configure(text=self.timer_obj.time_remaining())
            label_status.configure(text=self.timer_obj.status)
            label_activity['text'] = get_activity_text()

        # Function to call timer label update every second
        def timer_refresh(interval=1, func=label_timer_update):
            stopped = Event()

            def loop():
                while not stopped.wait(interval):
                    func()
            Thread(target=loop).start()
            return stopped.set


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
