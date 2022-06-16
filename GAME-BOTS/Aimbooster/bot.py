import pyautogui, time, keyboard, random, win32con, win32api
# Color (255, 219, 195)

def click(x, y):
	print('click')
	win32api.SetCursorPos((x, y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
	time.sleep(0.17)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0 ,0)

print('Empezando')
if pyautogui.locateOnScreen('menu.png', confidence=0.9):
	click(523, 448)
else:
	click(702, 654)

while keyboard.is_pressed('q') == False:
	pic = pyautogui.screenshot(region=(382, 266, 592, 410))

	width, height = pic.size
	last = (0,0)
	for x in range(0, width, 7):
		for y in range(0, height, 7):

			rgb = pic.getpixel((x, y))
			if rgb == (255, 219, 195) and x > last[0] and y > last[1]:
				print('encotrado', rgb , x, y)
				last = (x+20, y+20)
				# Obtiene la region desde donde empieza el recuadro hasta donde ha detectado la coincidencia
				click(382+x, 266+y)
				break
				

				# Continua con el bucle for para no hacer click en el mismo sitio dos veces
				




