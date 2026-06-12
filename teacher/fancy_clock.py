import LCD1602
import time, gpiozero
from datetime import datetime

def main():
    switch = gpiozero.Button(21, pull_up=True)
    show_colon = True
    time_mode, seconds_mode, date_mode = range(3)
    disp_mode = time_mode
    LCD1602.init()
    
    while True:
        if switch.is_pressed:
            disp_mode = disp_mode + 1
            if disp_mode > date_mode:
                disp_mode = time_mode
        if disp_mode == time_mode:
            display_time()
        elif disp_mode == seconds_mode:
            display_seconds()
        elif disp_mode == date_mode:
            display_date()
        time.sleep(0.5)
       

def display_time():
    LCD1602.clear()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    LCD1602.write(0, 0, 'Time:')
    LCD1602.write(1, 1, current_time)

def display_seconds():
    LCD1602.clear()
    now = datetime.now()
    current_seconds = now.strftime("  %S")
    LCD1602.write(0, 0, 'Seconds:')
    LCD1602.write(1, 1, current_seconds)

def display_date():
    LCD1602.clear()
    now = datetime.now()
    current_date = now.strftime("%m%d")
    LCD1602.write(0, 0, 'Date:')
    LCD1602.write(1, 1, current_date)

def destroy():
    LCD1602.clear()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        destroy()


