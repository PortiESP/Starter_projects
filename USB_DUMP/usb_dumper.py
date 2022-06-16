from code import *
from sys import exit

if __name__ == '__main__':

	d = Dumper()
	print('Iniciando escaneo...')
	puertos_inicio = d.scan_ports()
	print('Esperando entrada...')
	while True:
		puertos_fin = d.scan_ports()
		if len(puertos_inicio) != len(puertos_fin):
			usb = d.get_drive(puertos_inicio, puertos_fin)
			print('Conectado con ' + usb + ':/')
			break

	print('Volcando datos...')
	newdir = d.dump_data(usb)
	print('Completado!!!')
	os.system('start DUMPS\\ explorer' )
	sys.exit()
