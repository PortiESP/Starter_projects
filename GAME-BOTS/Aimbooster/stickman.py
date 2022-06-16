import pyautogui, time, keyboard, random, win32con, win32api


while not keyboard.is_pressed('q'):
	if pyautogui.locateOnScreen('stickman.png', grayscale=True,  confidence=0.9) != None:
		print('can see it')
		time.sleep(0.5)
	else:
		print('not seeing it')
		time.sleep(0.5)