import  pyautogui, time, random, win32api, win32con, keyboard




row1 = 306
row2 = 379
row3 = 460
row4 = 555
y_axis = 500

def click(x, y):
	win32api.SetCursorPos((x, y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
	time.sleep(0.016)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

# win32api.SetCursorPos((row1, y_axis))
# time.sleep(1.5)
# win32api.SetCursorPos((row2, y_axis))
# time.sleep(1.5)
# win32api.SetCursorPos((row3, y_axis))
# time.sleep(1.5)
# win32api.SetCursorPos((row4, y_axis))

# input()
click(431, 435)

while keyboard.is_pressed('q') == False:
	if pyautogui.pixel(row1, y_axis)[0] == 0: 
		count = click(row1, y_axis)
	if pyautogui.pixel(row2, y_axis)[0] == 0: 
		count = click(row2, y_axis)
	if pyautogui.pixel(row3, y_axis)[0] == 0: 
		count = click(row3, y_axis)
	if pyautogui.pixel(row4, y_axis)[0] == 0: 
		count = click(row4, y_axis)

	


