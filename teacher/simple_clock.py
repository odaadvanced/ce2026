import LCD1602
import time
from datetime import datetime

def main():
    LCD1602.init()
    show_colon = True
    LCD1602.init()

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        

        LCD1602.write(0, 0, 'Greetings!')
        LCD1602.write(1, 1, current_time)


def destroy():
	LCD1602.clear()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		destroy()
