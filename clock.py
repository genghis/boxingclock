import PySimpleGUI as sg
from playsound import playsound
import time

# ----------------  Create Form  ----------------
sg.ChangeLookAndFeel('Black')
sg.SetOptions(element_padding=(0, 0))

layout = [[sg.Text('', size=(10, 1), font=('Helvetica', 40), justification='center', key='Round')],
          [sg.Text('', size=(10, 1), font=('Helvetica', 60),
                   justification='center', text_color='red', key='timer')],
          [sg.Text('Rounds:', pad=(5, 5), font=('Helvetica', 15),
                   justification='center'), sg.In('5', key='RoundEntry', size=(5, 30)),
           sg.Text('Length:', pad=(5, 5), font=('Helvetica', 15),
                   justification='center'), sg.In('3', key='LengthEntry', size=(5, 30)),
           sg.Text('Break Length:', pad=(5, 5), font=('Helvetica', 15),
                   justification='center'), sg.In('1', key='BreakEntry', size=(5, 30))],
          [sg.ReadButton('Go', pad=(3, 5), button_color=(
              'white', 'green'), key='Run', size=(0, 2)),
           sg.ReadButton('Pause', pad=(3, 5), key='Pause', size=(0, 2), button_color=(
               'white', '#001480'), disabled=True),
           sg.ReadButton('Reset', pad=(3, 5), size=(0, 2), button_color=(
               'white', '#007339'), key='Reset'),
           sg.Exit(button_color=('white', 'firebrick4'), pad=(3, 5), size=(0, 2), key='Exit')]]

window = sg.Window('Running Timer', auto_size_buttons=False,
                   keep_on_top=True, grab_anywhere=True, element_justification='c').Layout(layout)

# ----------------  main loop  ----------------

current_time = 0
current_round = 1
paused = True
start_time = int(round(time.time() * 100))
round_length = 1
round_number = 3
break_length = 1
countdown = 0
paused_time = 0
first_run = True
on_break = True

while (True):
    # --------- Read and update window --------
    if first_run:
        event, values = window.Read(timeout=10)  # run every 10 milliseconds
    elif not paused:
        event, values = window.Read(timeout=10)  # run every 10 milliseconds

        countdown = int(round(time.time() * 100)) - start_time
        current_time = (round_length * 60 * 100) - countdown
    else:
        event, values = window.Read(timeout=10)
    # --------- Check for events --------
    if event in (None, 'Exit'):        # ALWAYS give a way out of program
        break
    if event == 'Pause':
        paused = True
        paused_time = int(round(time.time() * 100))
        window.FindElement('Pause').Update(disabled=True)
        window.FindElement('Run').Update(disabled=False)
    if event == 'Run':
        round_number = int(values['RoundEntry'])
        round_length = int(values['LengthEntry'])
        break_length = int(values['BreakEntry'])

        if first_run:
            start_time = int(round(time.time() * 100))
            first_run = False
            window.FindElement('Round').Update(f'ROUND {current_round}')
            window.FindElement('Pause').Update(disabled=False)
            window.FindElement('Run').Update(disabled=True)
        elif paused:
            start_time = start_time + \
                int(round(time.time() * 100)) - paused_time
            window.FindElement('Pause').Update(disabled=False)
            window.FindElement('Run').Update(disabled=True)
        paused = not paused
    if event == 'Reset':
        current_time = 0
        current_round = 1
        paused = True
        start_time = int(round(time.time() * 100))
        countdown = 0
        paused_time = 0
        on_break = True
        first_run = True
        window.FindElement('Pause').Update(disabled=True)
        window.FindElement('Run').Update(disabled=False)

    if current_time < 0:
        current_time = 0

    if current_time == 0 and not paused:
        if round_number >= current_round:
            if not on_break:
                playsound('bell.mp3')
                on_break = True
                window.FindElement('Round').Update('BREAK')
                start_time = int(round(time.time() * 100))
                countdown = int(round(time.time() * 100)) - start_time
                current_time = (break_length * 60 * 100) - countdown
            elif on_break:
                playsound('bell.mp3')
                on_break = False
                window.FindElement('Round').Update(f'ROUND {current_round}')
                current_round += 1
                start_time = int(round(time.time() * 100))
                countdown = int(round(time.time() * 100)) - start_time
                current_time = (round_length * 60 * 100) - countdown

        elif round_number < current_round and not on_break:
            playsound('bell.mp3')
            paused = True

        # --------- Display timer in window --------
    window.FindElement('timer').Update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                                     (current_time //
                                                                      100) % 60,
                                                                     current_time % 100))
