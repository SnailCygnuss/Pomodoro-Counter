from plyer import notification
import os


def screen_notification(task):
    """Function to show on screen notification"""
    title_str = 'Pomodoro Timer'
    nxt_activity = "Next Activity"
    if task == "Pomodoro":
        nxt_activity = "Break"
    elif "Break" in task:
        nxt_activity = "Pomodoro"
    msg_str = f'End of {task}. Time for {nxt_activity}'
    notification.notify(
        title=title_str,
        message=msg_str,
        app_icon=icon_path(),
        timeout=3
    )
    return True


def icon_path():
    return os.path.join(os.path.dirname(__file__), 'tomato.ico')


if __name__ == "__main__":
    screen_notification("Pomodoro")
    screen_notification("Short Break")