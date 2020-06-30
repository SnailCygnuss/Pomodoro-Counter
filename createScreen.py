from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, Button, Text, Label
from asciimatics.scene import Scene
from asciimatics.exceptions import NextScene, StopApplication, ResizeScreenError
from asciimatics.effects import Print, Stars
from asciimatics.renderers import BarChart
import sys
from resumabletimer import ResumableTimer
import threading
import time


class DataCacheModel:
    def __init__(self):
        self.p_length = 25 * 60
        self.b_length = 5 * 60
        self.l_length = 15 * 60


class ClockLabel(Label):
    pass


class MainView(Frame):
    #TODO: Fix threads
    #TODO: Connect other timer buttons for break and ling break
    #TODO: Add pause button
    #TODO: Add pomodoro counter
    def __init__(self, screen, dc):
        super(MainView, self).__init__(screen,
                                       screen.height * 9 // 10,
                                       screen.width * 9 // 10,
                                       x=10, y=10,
                                       hover_focus=True,
                                       can_scroll=False,
                                       title='Main Screen')
        self.dc = dc
        # Timer objects
        self._timer = None
        self.is_running = False
        #self.cancel_future_calls = self.call_repeatedly(100, self._pstart)
        #self.timer_length = dc.p_length
        # Create time object
        #self.timer_obj = ResumableTimer(self.timer_length, self.time_up)
        # Info Layout
        layout1 = Layout([1, 1], fill_frame=False)
        self.add_layout(layout1)
        self.timer_label = Label("Timer Not Running")
        #self.timer_label = Label(self.timer_obj.time_remaining())
        layout1.add_widget(self.timer_label, column=1)
        # Control Buttons
        layout2 = Layout([100], fill_frame=False)
        self.add_layout(layout2)
        layout2.add_widget(Button("Start Pomodoro", self.pstart))
        layout2.add_widget(Button("Start Short Break", self._bstart))
        layout2.add_widget(Button("Start Long Break", self._lstart))
        layout2.add_widget(Button("Quit", self._quit))
        self.fix()

    def pstart(self):
        timer_obj = ResumableTimer(self.dc.p_length, self.time_up)
        timer_obj.start()
        if not self.is_running:
            self._timer = threading.Timer(1, self._pstart, args=timer_obj)
            self._timer.start()
            self.is_running = True

    def _pstart(self, timer_obj):
        self.is_running = False
        self.timer_label._text = str(timer_obj.time_remaining())
        self.screen.force_update()
        self.pstart()

    def _bstart(self):
        # raise NextScene("B Screen")
        pass

    def _lstart(self):
        # raise NextScene("L Screen")
        pass

    def time_up(self):
        self.timer_label._text = str("Time Up!!!")

    def _quit(self):
        self.timer_obj.proc.cancel()
        self.cancel_future_calls()
        raise StopApplication("User Pressed Quit")

    @staticmethod
    def call_repeatedly(interval, func, *args):
        stopped = threading.Event()

        def loop():
            while not stopped.wait(interval):
                func(*args)

        threading.Thread(target=loop).start()
        return stopped.set


class TimeView(Frame):
    def __init__(self, screen, dc, type=0):
        super(TimeView, self).__init__(screen,
                                       screen.height * 9 // 10,
                                       screen.width * 9 // 10,
                                       hover_focus=True,
                                       can_scroll=False,
                                       title='Timer Screen')
        self.set_theme("green")
        self.dc = dc
        if type == 0:
            msg = 'Time to Focus'
            self.timer_length = dc.p_length
        elif type == 1:
            msg = 'Time for Short Break'
            self.timer_length = dc.b_length
        elif type == 2:
            msg = 'Time for Long Break'
            self.timer_length = dc.l_length
        self.timer_obj = ResumableTimer(self.timer_length, self.time_up)
        self.timer_obj.start()
        self.timer_label = Label(self.timer_obj.time_remaining())
        # Add layout and buttons
        layout = Layout([100], fill_frame=False)
        self.add_layout(layout)
        layout.add_widget(Label(msg))
        layout.add_widget(self.timer_label)
        layout.add_widget(Button("Pause Timer", self._pause))
        layout.add_widget(Button("Back to Main Screen", self._start))
        self.fix()

    def time_up(self):
        pass

    def _start(self):
        self.timer_obj.proc.cancel()
        raise NextScene("Main Screen")

    def _pause(self):
        self.timer_obj.pause()


def demo(screen, scene):
    # scenes = [Scene([MainView(screen, datacache)], -1, name="Main Screen"),
    #           Scene([TimeView(screen, datacache, 0)], -1, name="P Screen"),
    #           Scene([TimeView(screen, datacache, 1)], -1, name="B Screen"),
    #           Scene([TimeView(screen, datacache, 2)], -1, name="L Screen")
    #           ]
    effect2 = Stars(screen, screen.width)
    effects = [Print(screen,
                     BarChart(10, 40, [10, 10],
                              char="=",
                              gradient=[(20, Screen.COLOUR_GREEN),
                                        (30, Screen.COLOUR_YELLOW),
                                        (40, Screen.COLOUR_RED)]),
                     x=13, y=1, transparent=False, speed=2)]
    scenes2 = [Scene([MainView(screen, datacache)], -1, name="Main Screen")]
    scenes3 = [Scene([effect2], -1)]
    screen.play(scenes2, stop_on_resize=True, start_scene=scene, allow_int=True)


datacache = DataCacheModel()
last_scene = None
if __name__ == '__main__':
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
        except KeyboardInterrupt:
            print(threading.enumerate())
            sys.exit(0)
