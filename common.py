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
    icon_file = os.path.join(os.path.dirname(__file__), 'tomato.ico')
    notification.notify(
        title=title_str,
        message=msg_str,
        app_icon=icon_file,
        timeout=3
    )
    return True


if __name__ == "__main__":
    screen_notification("Pomodoro")
    screen_notification("Short Break")