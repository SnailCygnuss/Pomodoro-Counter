import time
import datetime
from threading import Timer


class ResumableTimer:

    def __init__(self, timer_length_sec, callback):
        self.timer_length_sec = datetime.timedelta(seconds=timer_length_sec)
        self.timer_remaining = self.timer_length_sec
        self.target = None
        self.status = 'Not Started'
        self.callback = callback
        self.proc = None

    def start(self):
        if self.status is not "Running":
            self.target = datetime.datetime.now() + self.timer_remaining
            self.proc = Timer(self.timer_remaining.total_seconds(), self.callback)
            self.status = 'Running'
            self.proc.start()

    def pause(self):
        if self.status is "Running":
            self.timer_remaining = self.target - datetime.datetime.now()
            self.target = None
            self.status = 'Paused'
            if self.proc is not None:
                self.proc.cancel()

    def time_remaining(self):
        # Return a string of format HH:MM:SS
        if self.target is None:
            hh_mm_ss = str(self.timer_remaining).split(".")[0]
            return display_time_string(hh_mm_ss)
        else:
            hh_mm_ss = str(self.target - datetime.datetime.now()).split(".")[0]
            return display_time_string(hh_mm_ss)


def display_time_string(hh_mm_ss):
    if hh_mm_ss.startswith("0"):
        hh_mm_ss = hh_mm_ss.split(":")
        time_str = hh_mm_ss[1] + ":" + hh_mm_ss[2]
    else:
        time_str = hh_mm_ss
    return time_str


def finish_func():
    print('Timer Finished')


def test_func():
    p = ResumableTimer(5, finish_func)
    print(p.status, p.time_remaining())
    #start = datetime.datetime.now()
    p.start()
    time.sleep(2)
    p.pause()
    time.sleep(2)
    p.start()
    p.proc.join()
    #print('Time up')
    #print(datetime.datetime.now() - start)


if __name__ == '__main__':
    import timeit
    print(timeit.timeit("test_func()", setup="from __main__ import test_func", number=1))
