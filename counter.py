from asciimatics.screen import Screen
from time import sleep
import os
import simpleaudio as sa
from plyer import notification

# TODO: Option to change timing limits
p_counter = 0
p_mins = 25  # Pomodoro minutes
b_mins = 5  # Short Break minutes
l_mins = 15  # Long Break minutes
alarm_file = os.path.join(os.path.dirname(__file__), 'bell.wav')
icon_file = os.path.join(os.path.dirname(__file__), 'tomato.ico')


def main_screen(screen):
    global p_counter
    global p_mins
    global b_mins
    global l_mins
    while True:
        screen.print_at('Pomodoro Counter', 0, 0)
        screen.print_at('Number of Pomodoros - ' + str(p_counter), 0, 4)
        screen.print_at(f'(S) - Start Pomodoro - {p_mins} mins', 0, 6)
        screen.print_at(f'(B) - Start Short Break - {b_mins} mins', 0, 7)
        screen.print_at(f'(L) - Start Long Break - {l_mins} mins', 0, 8)
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
    global p_counter
    screen.clear()
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
            #playsound()
            notify(flag)
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


def playsound():
    # Play sound at the end of timer
    wave_obj = sa.WaveObject.from_wave_file(alarm_file)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    return True


def notify(flag):
    # Function to add notification
    title_str = 'Pomodoro Timer'
    next_obj = 'work' if flag == 0 else 'break'
    message_str = 'End of timer. Time for ' + next_obj + '!!!'
    notification.notify(
        title=title_str,
        message=message_str,
        app_icon=icon_file,
        timeout=5,
    )
    return True


Screen.wrapper(main_screen)
