from asciimatics.screen import Screen
from time import sleep
from playsound import playsound
import os

# TODO: Option to change timing limits
p_counter = 0
p_mins = 25     # Pomodoro minutes
b_mins = 5      # Short Break minutes
l_mins = 15     # Long Break minutes
alarm_file = os.path.join(os.path.dirname(__file__), 'alarm1.mp3')

def main_screen(screen):
    global p_counter
    global p_mins
    global b_mins
    global l_mins
    while True:
        screen.print_at('Pomodoro Counter', 0, 0)
        screen.print_at('Number of Pomodoros - ' + str(p_counter), 0, 4)
        screen.print_at('(S) - Start Pomodoro', 0, 6)
        screen.print_at('(B) - Start Short Break', 0, 7)
        screen.print_at('(L) - Start Long Break', 0, 8)
        screen.print_at('(Q) - Quit', 0, 9)
        screen.refresh()
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return
        elif ev in (ord('S'), ord('s')):
            Screen.wrapper(starttimer, arguments=[p_mins, 0, 1])
        elif ev in (ord('B'), ord('b')):
            Screen.wrapper(starttimer, arguments=[b_mins, 0, 0])
        elif ev in (ord('L'), ord('l')):
            Screen.wrapper(starttimer, arguments=[l_mins, 0, 0])
        screen.refresh()


def starttimer(screen, tmins, tsecs, flag):
    # flag - indicate work (1) or break (0)
    # TODO: Add different coloured text for work or break
    # TODO: Play sound at end of timer
    global p_counter
    if flag == 1:
        screen.print_at('Time to Work !!!', 0, 0)
    elif flag == 0:
        screen.print_at('Time for Break !!!', 0, 0)
    screen.print_at('Number of Pomodoros - ' + str(p_counter), 0, 4)
    screen.print_at('(P) - Pause timer !!!', 0, 6)
    screen.print_at('(M) - Back to main menu', 0, 7)
    while True:
        rem_time = timestring(tmins, tsecs)
        screen.print_at(rem_time, 0, 2)
        screen.refresh()
        ev = screen.get_key()
        if ev in (ord('P'), ord('p')):
            Screen.wrapper(pausescreen, arguments=[tmins, tsecs])
        if ev in (ord('m'), ord('M')):
            return
        sleep(1)
        tsecs = tsecs - 1
        if tsecs < 0:
            tmins = tmins - 1
            tsecs = 59
        if tmins < 0:
            # Increment counter if work (1)
            if flag == 1:
                p_counter = p_counter + 1
            playsound(alarm_file)
            return


def pausescreen(screen, tmins, tsecs):
    rem_time = timestring(tmins, tsecs)
    # TODO: Make remaining time blink and add colour
    while True:
        screen.print_at('Timer Paused...', 0, 0)
        screen.print_at(rem_time, 0, 2)
        screen.print_at('(P) - Resume timer', 0, 6)
        screen.refresh()
        ev = screen.get_key()
        if ev in (ord('P'), ord('p')):
            return


def timestring(minute, second):
    # Display time as MM:SS
    minute = f'{minute:02d}'
    second = f'{second:02d}'
    tstring = minute + ':' + second
    return tstring


Screen.wrapper(main_screen)
