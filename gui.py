import FreeSimpleGUI as sg
import pomodoro as m

def update_timer_display():
    window['-lblTimer-'].update(value=m.format_time(m.time_left))
    window['-ProgressBar-'].update(max=m.time_left, current_count=0)
    

sg.theme('Kayak')   # Add a touch of color

layoutTimer = [ [sg.Text("Let's get work done!", font=('Arial Bold', 10), key="-lblSession-", pad=(0,5)) ],
                [sg.Text('00:00', font=('Arial Bold', 30), key="-lblTimer-") ],
                [sg.ProgressBar(max_value=m.time_left, size=(30,10), key="-ProgressBar-", pad=(10,15))],
                [sg.Button('Start', key="-start-",pad=(15,10)), sg.Button('Stop',key="-stop-", pad=(15,10)), sg.Button('Restart',key="-restart-",pad=(15,10))]
        ] 
layoutConfig = [ [sg.Text('Work',pad=(15,10)), sg.Input(size=(5,5), default_text='25', key="-work-",pad=(15,10))],
                 [sg.Text('Short Break',pad=(15,10)), sg.Input(size=(5,5), default_text='5', key="-s_break-",pad=(15,10))],
                 [sg.Text('Long Break',pad=(15,10)), sg.Input(size=(5,5), default_text='10', key="-l_break-",pad=(15,10))],
                 [sg.Button('Apply', key='-config-',pad=(15,10))]
                ]

# All the stuff inside your window.
layout = [[sg.TabGroup([
            [sg.Tab('Timer', layout=layoutTimer, element_justification= "center")],
            [sg.Tab('Config', layout=layoutConfig, element_justification= "center")]
        ])
        ]]

# Create the Window
window = sg.Window('Pomodoro Timer', layout, finalize=True)

# Update timer display on startup
update_timer_display()
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    elif event == "-start-":
        m.start()
    elif event == "-stop-":
        m.stop()
    elif event == "-restart-":
        m.restart()
    elif event == "-config-":
        work, sbreak, lbreak = int(values['-work-']), int(values['-s_break-']), int(values['-l_break-'])
        m.cnf_W, m.cnf_SB, m.cnf_LB = work, sbreak, lbreak
        m.update_config()
        update_timer_display()
    

window.close()
