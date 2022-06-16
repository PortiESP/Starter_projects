"""
	ERRORES
		- Cambia ruta para copiar los archivos, cambiar / por \
"""


import os
from datetime import *


class Dumper():

	def __init__(self):

		self.usb = None
		self.usbpath = None


	def scan_ports(self):

		drives_list = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 
				'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 
				'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
		connected_ports = list()
		for i in drives_list:
			if i == 'E':
				continue
			if os.path.exists(i + ':/'):
				connected_ports.append(i)
		

		return connected_ports




	def get_drive(self, inicio, fin):
		for drive in fin:
			if drive not in inicio:
				self.usb = drive
				self.usbpath = self.usb+'\\'
				return drive
		raise ValueError( 'Sin coincidencias' )


	def dump_data(self, drive):
		nombre = 'usb_' + datetime.now().strftime('%d-%m-%Y_%H.%M.%S')
		print(nombre)
		print('Copiando...')
		os.system(f'xcopy j:\\ DUMPS\\{nombre}\\{self.usb} /E/H/Y/Z/I/Q')

		return nombre

	



		




		
