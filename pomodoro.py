from threading import Thread
import time
import gui as g
from nava import play

cnf_W = 25
cnf_SB = 5
cnf_LB = 10

POMODORO_COUNT = 0
WORK = cnf_W * 60
SHORT_BREAK = cnf_SB * 60
LONG_BREAK = cnf_LB * 60
SESSION = 'Work' # 'Work', 'Short Break', 'Long Break'

time_thread = None
isRunning = False
time_left = WORK
current_progress = 0

def update_config():
    global WORK, SHORT_BREAK, LONG_BREAK, time_left, SESSION, POMODORO_COUNT, current_progress
    WORK = cnf_W * 60
    SHORT_BREAK = cnf_SB * 60
    LONG_BREAK = cnf_LB * 60
    time_left = WORK
    SESSION = 'Work'
    POMODORO_COUNT = 0
    current_progress= 0
    g.window['-lblTimer-'].update(value=format_time(time_left))
    g.window['-ProgressBar-'].update(max=time_left, current_count=current_progress)
    g.window['-lblSession-'].update(value="Let's get work done!")
    g.window.refresh()

def start_timer():
    global time_left, SESSION, POMODORO_COUNT, isRunning, current_progress
    while isRunning:
        while time_left > 0 and isRunning:
            time_left -= 1
            current_progress += 1
            time.sleep(1)
            g.window['-lblTimer-'].update(value=format_time(time_left))
            g.window['-ProgressBar-'].update(current_count=current_progress)
            g.window['-lblSession-'].update(value=f"Current session: {SESSION}")
            g.window.refresh()
            
        if time_left == 0 and isRunning:
            play("audio.wav", async_mode=True)
            if SESSION == 'Work':
                POMODORO_COUNT += 1
                current_progress = 0
                SESSION = 'Long Break' if POMODORO_COUNT % 4 == 0 else 'Short Break'
                if SESSION == 'Long Break':
                    time_left = LONG_BREAK
                    g.window['-lblSession-'].update(value=f"Current session: {SESSION}")
                    current_progress=0
                    g.window['-ProgressBar-'].update(max=time_left, current_count=current_progress)
                    g.window.refresh()
                else:
                    time_left = SHORT_BREAK
                    g.window['-lblSession-'].update(value=f"Current session: {SESSION}")
                    current_progress=0
                    g.window['-ProgressBar-'].update(max=time_left, current_count=current_progress)
                    g.window.refresh()
            else:
                SESSION = 'Work'
                time_left = WORK
                g.window['-lblSession-'].update(value=f"Current session: {SESSION}")
                current_progress=0
                g.window['-ProgressBar-'].update(max=time_left, current_count=current_progress)
                g.window.refresh()

def start():
    global time_thread, isRunning
    if not isRunning:
        isRunning = True
        time_thread = Thread(None, start_timer)
        time_thread.start()
        
def format_time(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    return f'{minutes:02}:{secs:02}'

def stop():
    global isRunning
    isRunning = not isRunning

def restart():
    global time_left, SESSION, POMODORO_COUNT, isRunning
    isRunning = False
    update_config()
